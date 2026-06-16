from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/comments", tags=["评论"])


@router.post("", response_model=schemas.CommentWithAuthor, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: schemas.CommentCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    db_comment = models.Comment(
        **comment.model_dump(),
        author_id=current_user.id
    )
    db.add(db_comment)
    post.comments_count += 1
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/post/{post_id}", response_model=List[schemas.CommentWithAuthor])
def read_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    comments = db.query(models.Comment).filter(
        models.Comment.post_id == post_id,
        models.Comment.parent_id.is_(None)
    ).order_by(models.Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    return comments


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此评论")
    
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if post:
        post.comments_count -= 1
    
    db.delete(comment)
    db.commit()
    return None
