from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .. import schemas, models, auth, utils
from ..database import get_db

router = APIRouter(prefix="/services", tags=["服务导航"])


@router.get("", response_model=List[schemas.Service])
def get_services(
    category: Optional[str] = None,
    radius_km: float = Query(10.0, ge=0.1, le=100),
    min_rating: float = Query(0.0, ge=0.0, le=5.0),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.latitude is None or current_user.longitude is None:
        raise HTTPException(status_code=400, detail="请先设置您的地理位置")
    
    query = db.query(models.Service)
    
    if category:
        query = query.filter(models.Service.category == category)
    if min_rating > 0:
        query = query.filter(models.Service.rating >= min_rating)
    
    services = query.all()
    
    results = []
    for service in services:
        distance = utils.calculate_distance(
            current_user.latitude, current_user.longitude,
            service.latitude, service.longitude
        )
        
        if distance <= radius_km:
            service_dict = schemas.Service.model_validate(service)
            service_dict.distance = round(distance, 2)
            results.append(service_dict)
    
    results.sort(key=lambda x: x.distance)
    return results


@router.get("/categories")
def get_service_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Service.category).distinct().all()
    return [c[0] for c in categories]


@router.get("/{service_id}", response_model=schemas.Service)
def get_service_detail(
    service_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="服务机构不存在")
    
    if current_user.latitude and current_user.longitude:
        distance = utils.calculate_distance(
            current_user.latitude, current_user.longitude,
            service.latitude, service.longitude
        )
        service.distance = round(distance, 2)
    
    return service


@router.post("", response_model=schemas.Service, status_code=status.HTTP_201_CREATED)
def create_service(
    service: schemas.ServiceCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.post("/seed", status_code=status.HTTP_201_CREATED)
def seed_services(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    existing = db.query(models.Service).count()
    if existing > 0:
        return {"message": "已有数据，跳过初始化"}
    
    seed_data = [
        {
            "name": "爱宠动物医院",
            "category": "医院",
            "address": "北京市朝阳区建国路88号",
            "phone": "010-12345678",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "rating": 4.8,
            "review_count": 256,
            "business_hours": {
                "周一至周五": "09:00-21:00",
                "周六至周日": "10:00-18:00"
            },
            "description": "专业24小时宠物医院，配备先进医疗设备",
            "image_url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400"
        },
        {
            "name": "萌宠之家美容会所",
            "category": "美容",
            "address": "北京市朝阳区国贸商圈",
            "phone": "010-87654321",
            "latitude": 39.9142,
            "longitude": 116.4174,
            "rating": 4.9,
            "review_count": 189,
            "business_hours": {
                "周一至周日": "10:00-20:00"
            },
            "description": "专业宠物美容、SPA、造型设计",
            "image_url": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=400"
        },
        {
            "name": "爱心宠物寄养中心",
            "category": "寄养",
            "address": "北京市海淀区中关村大街1号",
            "phone": "010-55667788",
            "latitude": 39.9842,
            "longitude": 116.3074,
            "rating": 4.7,
            "review_count": 312,
            "business_hours": {
                "周一至周日": "08:00-22:00"
            },
            "description": "温馨家庭式寄养，24小时专人照顾",
            "image_url": "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=400"
        },
        {
            "name": "宠物乐园训练学校",
            "category": "训练",
            "address": "北京市通州区宠物文化园",
            "phone": "010-33445566",
            "latitude": 39.9092,
            "longitude": 116.6074,
            "rating": 4.6,
            "review_count": 145,
            "business_hours": {
                "周二至周日": "09:00-18:00"
            },
            "description": "专业训犬师，提供 obedience、敏捷训练课程",
            "image_url": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400"
        },
        {
            "name": "喵星人宠物用品店",
            "category": "用品",
            "address": "北京市西城区西单北大街",
            "phone": "010-99887766",
            "latitude": 39.9142,
            "longitude": 116.3674,
            "rating": 4.8,
            "review_count": 423,
            "business_hours": {
                "周一至周日": "10:00-21:00"
            },
            "description": "全品类宠物用品，进口食品、玩具、窝具",
            "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400"
        }
    ]
    
    for data in seed_data:
        db_service = models.Service(**data)
        db.add(db_service)
    
    db.commit()
    return {"message": f"成功添加 {len(seed_data)} 条服务数据"}
