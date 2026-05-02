from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Service
from app.schemas import ServiceCreate, ServiceResponse

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=List[ServiceResponse])
def get_all_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    services = db.query(Service).offset(skip).limit(limit).all()
    return services


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return service


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    db_service = Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service_update: ServiceCreate,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    for key, value in service_update.model_dump().items():
        setattr(service, key, value)
    
    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    db.delete(service)
    db.commit()