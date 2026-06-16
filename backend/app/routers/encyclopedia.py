from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/encyclopedia", tags=["宠物百科"])


@router.get("/breeds", response_model=List[schemas.BreedEncyclopedia])
def get_breeds(
    species: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(models.BreedEncyclopedia)
    
    if species:
        query = query.filter(models.BreedEncyclopedia.species == species)
    if search:
        query = query.filter(models.BreedEncyclopedia.name.contains(search))
    
    return query.order_by(models.BreedEncyclopedia.name).offset(skip).limit(limit).all()


@router.get("/breeds/{breed_id}", response_model=schemas.BreedEncyclopedia)
def get_breed_detail(breed_id: int, db: Session = Depends(get_db)):
    breed = db.query(models.BreedEncyclopedia).filter(models.BreedEncyclopedia.id == breed_id).first()
    if not breed:
        raise HTTPException(status_code=404, detail="品种不存在")
    return breed


@router.post("/breeds", response_model=schemas.BreedEncyclopedia, status_code=status.HTTP_201_CREATED)
def create_breed(
    breed: schemas.BreedEncyclopediaCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_breed = models.BreedEncyclopedia(**breed.model_dump())
    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed


@router.get("/diseases", response_model=List[schemas.DiseaseGuide])
def get_diseases(
    species: Optional[str] = None,
    severity: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(models.DiseaseGuide)
    
    if species:
        query = query.filter(models.DiseaseGuide.species.contains(species))
    if severity:
        query = query.filter(models.DiseaseGuide.severity == severity)
    if search:
        query = query.filter(
            (models.DiseaseGuide.name.contains(search)) |
            (models.DiseaseGuide.symptoms.contains(search))
        )
    
    return query.order_by(models.DiseaseGuide.name).offset(skip).limit(limit).all()


@router.get("/diseases/{disease_id}", response_model=schemas.DiseaseGuide)
def get_disease_detail(disease_id: int, db: Session = Depends(get_db)):
    disease = db.query(models.DiseaseGuide).filter(models.DiseaseGuide.id == disease_id).first()
    if not disease:
        raise HTTPException(status_code=404, detail="疾病信息不存在")
    return disease


@router.post("/diseases", response_model=schemas.DiseaseGuide, status_code=status.HTTP_201_CREATED)
def create_disease(
    disease: schemas.DiseaseGuideCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_disease = models.DiseaseGuide(**disease.model_dump())
    db.add(db_disease)
    db.commit()
    db.refresh(db_disease)
    return db_disease
