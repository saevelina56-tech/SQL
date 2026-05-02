from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Car, Client
from app.schemas import CarCreate, CarResponse

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/", response_model=List[CarResponse])
def get_all_cars(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    cars = db.query(Car).offset(skip).limit(limit).all()
    return cars


@router.get("/{car_id}", response_model=CarResponse)
def get_car(
    car_id: int,
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    return car


@router.get("/by-client/{client_id}", response_model=List[CarResponse])
def get_cars_by_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    cars = db.query(Car).filter(Car.client_id == client_id).all()
    return cars


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(
    car: CarCreate,
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == car.client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@router.put("/{car_id}", response_model=CarResponse)
def update_car(
    car_id: int,
    car_update: CarCreate,
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    for key, value in car_update.model_dump().items():
        setattr(car, key, value)
    
    db.commit()
    db.refresh(car)
    return car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: int,
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    db.delete(car)
    db.commit()