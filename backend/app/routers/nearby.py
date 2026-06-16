from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from .. import schemas, models, auth, utils
from ..database import get_db

router = APIRouter(prefix="/nearby", tags=["附近宠物"])


@router.get("/pets", response_model=List[dict])
def get_nearby_pets(
    radius_km: float = Query(5.0, ge=0.1, le=50),
    species: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.latitude is None or current_user.longitude is None:
        raise HTTPException(status_code=400, detail="请先设置您的地理位置")
    
    users = db.query(models.User).filter(
        models.User.id != current_user.id,
        models.User.latitude.isnot(None),
        models.User.longitude.isnot(None)
    ).all()
    
    results = []
    for user in users:
        distance = utils.calculate_distance(
            current_user.latitude, current_user.longitude,
            user.latitude, user.longitude
        )
        
        if distance <= radius_km:
            pets = db.query(models.Pet).filter(models.Pet.owner_id == user.id).all()
            if species:
                pets = [p for p in pets if p.species == species]
            
            if pets:
                results.append({
                    "user": schemas.UserWithDistance(
                        **schemas.User.model_validate(user).model_dump(),
                        distance=round(distance, 2)
                    ),
                    "pets": pets,
                    "distance": round(distance, 2)
                })
    
    results.sort(key=lambda x: x["distance"])
    return results


@router.get("/meetups", response_model=List[schemas.Meetup])
def get_nearby_meetups(
    radius_km: float = Query(10.0, ge=0.1, le=100),
    status: Optional[str] = "upcoming",
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.latitude is None or current_user.longitude is None:
        raise HTTPException(status_code=400, detail="请先设置您的地理位置")
    
    meetups = db.query(models.Meetup).filter(models.Meetup.status == status).all()
    
    results = []
    for meetup in meetups:
        distance = utils.calculate_distance(
            current_user.latitude, current_user.longitude,
            meetup.latitude, meetup.longitude
        )
        
        if distance <= radius_km:
            results.append(meetup)
    
    results.sort(key=lambda m: utils.calculate_distance(
        current_user.latitude, current_user.longitude,
        m.latitude, m.longitude
    ))
    
    return results


@router.post("/meetups", response_model=schemas.Meetup, status_code=status.HTTP_201_CREATED)
def create_meetup(
    meetup: schemas.MeetupCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_meetup = models.Meetup(
        **meetup.model_dump(),
        organizer_id=current_user.id
    )
    db.add(db_meetup)
    db.flush()
    
    participant = models.MeetupParticipant(
        meetup_id=db_meetup.id,
        user_id=current_user.id
    )
    db.add(participant)
    db.commit()
    db.refresh(db_meetup)
    return db_meetup


@router.get("/meetups/{meetup_id}", response_model=schemas.Meetup)
def get_meetup_detail(
    meetup_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    meetup = db.query(models.Meetup).filter(models.Meetup.id == meetup_id).first()
    if not meetup:
        raise HTTPException(status_code=404, detail="聚会不存在")
    return meetup


@router.post("/meetups/{meetup_id}/join", status_code=status.HTTP_201_CREATED)
def join_meetup(
    meetup_id: int,
    pet_id: Optional[int] = None,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    meetup = db.query(models.Meetup).filter(models.Meetup.id == meetup_id).first()
    if not meetup:
        raise HTTPException(status_code=404, detail="聚会不存在")
    
    if meetup.status != "upcoming":
        raise HTTPException(status_code=400, detail="此聚会已结束或取消")
    
    if meetup.current_participants >= meetup.max_participants:
        raise HTTPException(status_code=400, detail="聚会人数已满")
    
    existing = db.query(models.MeetupParticipant).filter(
        models.MeetupParticipant.meetup_id == meetup_id,
        models.MeetupParticipant.user_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="您已报名此聚会")
    
    if pet_id:
        pet = db.query(models.Pet).filter(
            models.Pet.id == pet_id,
            models.Pet.owner_id == current_user.id
        ).first()
        if not pet:
            raise HTTPException(status_code=404, detail="宠物不存在")
    
    participant = models.MeetupParticipant(
        meetup_id=meetup_id,
        user_id=current_user.id,
        pet_id=pet_id
    )
    db.add(participant)
    meetup.current_participants += 1
    db.commit()
    
    return {"message": "报名成功", "current_participants": meetup.current_participants}


@router.delete("/meetups/{meetup_id}/join", status_code=status.HTTP_204_NO_CONTENT)
def leave_meetup(
    meetup_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    meetup = db.query(models.Meetup).filter(models.Meetup.id == meetup_id).first()
    if not meetup:
        raise HTTPException(status_code=404, detail="聚会不存在")
    
    participant = db.query(models.MeetupParticipant).filter(
        models.MeetupParticipant.meetup_id == meetup_id,
        models.MeetupParticipant.user_id == current_user.id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=400, detail="您未报名此聚会")
    
    db.delete(participant)
    if meetup.current_participants > 0:
        meetup.current_participants -= 1
    db.commit()
    
    return None
