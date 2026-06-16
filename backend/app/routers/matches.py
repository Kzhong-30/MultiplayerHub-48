from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .. import schemas, models, auth, utils
from ..database import get_db

router = APIRouter(prefix="/matches", tags=["智能配对"])


@router.get("/recommendations", response_model=List[schemas.MatchResult])
def get_match_recommendations(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    user_pets = db.query(models.Pet).filter(models.Pet.owner_id == current_user.id).all()
    
    if not user_pets:
        raise HTTPException(status_code=400, detail="请先添加宠物档案")
    
    if current_user.latitude is None or current_user.longitude is None:
        raise HTTPException(status_code=400, detail="请先设置地理位置")
    
    other_users = db.query(models.User).filter(
        models.User.id != current_user.id
    ).all()
    
    results = []
    for target_user in other_users:
        target_pets = db.query(models.Pet).filter(models.Pet.owner_id == target_user.id).all()
        if not target_pets:
            continue
        
        if target_user.latitude is None or target_user.longitude is None:
            continue
        
        match_score, breed_compat, age_sim, dist_score = utils.calculate_match_score(
            user_pets, target_pets,
            current_user.latitude, current_user.longitude,
            target_user.latitude, target_user.longitude
        )
        
        if match_score > 30:
            distance = utils.calculate_distance(
                current_user.latitude, current_user.longitude,
                target_user.latitude, target_user.longitude
            )
            
            target_user_dict = schemas.UserWithDistance.model_validate(target_user)
            target_user_dict.distance = round(distance, 2)
            
            results.append(schemas.MatchResult(
                target_user=target_user_dict,
                target_pets=target_pets,
                match_score=round(match_score, 2),
                breed_compatibility=round(breed_compat * 100, 2),
                age_similarity=round(age_sim * 100, 2),
                distance_score=round(dist_score * 100, 2)
            ))
    
    results.sort(key=lambda x: x.match_score, reverse=True)
    return results[:10]


@router.post("", response_model=schemas.MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(
    match_data: schemas.MatchCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if match_data.target_user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能与自己配对")
    
    target_user = db.query(models.User).filter(models.User.id == match_data.target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="目标用户不存在")
    
    existing_match = db.query(models.Match).filter(
        ((models.Match.user_id == current_user.id) & (models.Match.target_user_id == match_data.target_user_id)) |
        ((models.Match.user_id == match_data.target_user_id) & (models.Match.target_user_id == current_user.id))
    ).first()
    
    if existing_match:
        raise HTTPException(status_code=400, detail="已存在配对请求")
    
    user_pets = db.query(models.Pet).filter(models.Pet.owner_id == current_user.id).all()
    target_pets = db.query(models.Pet).filter(models.Pet.owner_id == match_data.target_user_id).all()
    
    if current_user.latitude and current_user.longitude and target_user.latitude and target_user.longitude:
        match_score, breed_compat, age_sim, dist_score = utils.calculate_match_score(
            user_pets, target_pets,
            current_user.latitude, current_user.longitude,
            target_user.latitude, target_user.longitude
        )
    else:
        match_score, breed_compat, age_sim, dist_score = 50, 0.5, 0.5, 0.5
    
    db_match = models.Match(
        user_id=current_user.id,
        target_user_id=match_data.target_user_id,
        match_score=match_score,
        breed_compatibility=breed_compat * 100,
        age_similarity=age_sim * 100,
        distance_score=dist_score * 100,
        message=match_data.message
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.get("/sent", response_model=List[schemas.MatchResponse])
def get_sent_matches(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    matches = db.query(models.Match).filter(
        models.Match.user_id == current_user.id
    ).order_by(models.Match.created_at.desc()).all()
    return matches


@router.get("/received", response_model=List[schemas.MatchResponse])
def get_received_matches(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    matches = db.query(models.Match).filter(
        models.Match.target_user_id == current_user.id
    ).order_by(models.Match.created_at.desc()).all()
    return matches


@router.put("/{match_id}/accept", response_model=schemas.MatchResponse)
def accept_match(
    match_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="配对请求不存在")
    if match.target_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权处理此请求")
    
    match.status = "accepted"
    match.responded_at = datetime.utcnow()
    db.commit()
    db.refresh(match)
    return match


@router.put("/{match_id}/reject", response_model=schemas.MatchResponse)
def reject_match(
    match_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="配对请求不存在")
    if match.target_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权处理此请求")
    
    match.status = "rejected"
    match.responded_at = datetime.utcnow()
    db.commit()
    db.refresh(match)
    return match
