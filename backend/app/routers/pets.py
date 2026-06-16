from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/pets", tags=["宠物档案"])


@router.post("", response_model=schemas.Pet, status_code=status.HTTP_201_CREATED)
def create_pet(
    pet: schemas.PetCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_pet = models.Pet(**pet.model_dump(), owner_id=current_user.id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


@router.get("", response_model=List[schemas.Pet])
def read_pets(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pets = db.query(models.Pet).filter(models.Pet.owner_id == current_user.id).all()
    return pets


@router.get("/{pet_id}", response_model=schemas.Pet)
def read_pet(
    pet_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此宠物档案")
    return pet


@router.put("/{pet_id}", response_model=schemas.Pet)
def update_pet(
    pet_id: int,
    pet_update: schemas.PetUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此宠物档案")
    
    for field, value in pet_update.model_dump(exclude_unset=True).items():
        setattr(pet, field, value)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(
    pet_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此宠物档案")
    
    db.delete(pet)
    db.commit()
    return None


@router.post("/{pet_id}/weight", response_model=schemas.WeightRecord)
def add_weight_record(
    pet_id: int,
    record: schemas.WeightRecordCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此宠物档案")
    
    db_record = models.WeightRecord(**record.model_dump(), pet_id=pet_id)
    db.add(db_record)
    pet.weight = record.weight
    db.commit()
    db.refresh(db_record)
    return db_record


@router.post("/{pet_id}/vaccine", response_model=schemas.VaccineRecord)
def add_vaccine_record(
    pet_id: int,
    record: schemas.VaccineRecordCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此宠物档案")
    
    db_record = models.VaccineRecord(**record.model_dump(), pet_id=pet_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.post("/{pet_id}/photos", response_model=schemas.PetPhoto)
def add_photo(
    pet_id: int,
    photo: schemas.PetPhotoCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此宠物档案")
    
    if photo.is_avatar:
        db.query(models.PetPhoto).filter(
            models.PetPhoto.pet_id == pet_id,
            models.PetPhoto.is_avatar == True
        ).update({"is_avatar": False})
    
    db_photo = models.PetPhoto(**photo.model_dump(), pet_id=pet_id)
    db.add(db_photo)
    
    if photo.is_avatar:
        pet.avatar = photo.url
    
    db.commit()
    db.refresh(db_photo)
    return db_photo


@router.delete("/{pet_id}/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(
    pet_id: int,
    photo_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此宠物档案")
    
    photo = db.query(models.PetPhoto).filter(
        models.PetPhoto.id == photo_id,
        models.PetPhoto.pet_id == pet_id
    ).first()
    if not photo:
        raise HTTPException(status_code=404, detail="照片不存在")
    
    db.delete(photo)
    db.commit()
    return None
