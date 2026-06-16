from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["动态广场"])


@router.post("", response_model=schemas.PostWithDetails, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if post.pet_id:
        pet = db.query(models.Pet).filter(
            models.Pet.id == post.pet_id,
            models.Pet.owner_id == current_user.id
        ).first()
        if not pet:
            raise HTTPException(status_code=404, detail="宠物不存在或无权访问")
    
    db_post = models.Post(**post.model_dump(), author_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("", response_model=List[schemas.PostWithDetails])
def read_posts(
    skip: int = 0,
    limit: int = 20,
    tag: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)
    
    if tag:
        query = query.filter(models.Post.tags.contains([tag]))
    
    posts = query.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    
    liked_post_ids = db.query(models.Like.post_id).filter(
        models.Like.user_id == current_user.id
    ).all()
    liked_ids = {pid[0] for pid in liked_post_ids}
    
    for post in posts:
        post.is_liked = post.id in liked_ids
    
    return posts


@router.get("/{post_id}", response_model=schemas.PostWithDetails)
def read_post(
    post_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    is_liked = db.query(models.Like).filter(
        models.Like.post_id == post_id,
        models.Like.user_id == current_user.id
    ).first() is not None
    
    post.is_liked = is_liked
    return post


@router.put("/{post_id}", response_model=schemas.PostWithDetails)
def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此动态")
    
    for field, value in post_update.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此动态")
    
    db.delete(post)
    db.commit()
    return None


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
def like_post(
    post_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    existing_like = db.query(models.Like).filter(
        models.Like.post_id == post_id,
        models.Like.user_id == current_user.id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        post.likes_count -= 1
        db.commit()
        return {"liked": False, "likes_count": post.likes_count}
    else:
        like = models.Like(post_id=post_id, user_id=current_user.id)
        db.add(like)
        post.likes_count += 1
        db.commit()
        return {"liked": True, "likes_count": post.likes_count}


@router.get("/user/{user_id}", response_model=List[schemas.PostWithDetails])
def read_user_posts(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    posts = db.query(models.Post).filter(
        models.Post.author_id == user_id
    ).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    
    liked_post_ids = db.query(models.Like.post_id).filter(
        models.Like.user_id == current_user.id
    ).all()
    liked_ids = {pid[0] for pid in liked_post_ids}
    
    for post in posts:
        post.is_liked = post.id in liked_ids
    
    return posts
