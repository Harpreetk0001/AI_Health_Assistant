from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.health import HealthCreate, HealthRead
from app.crud import health as crud_health
from app.db.session import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=HealthRead)
def create_health_entry(health: HealthCreate, db: Session = Depends(get_db)):
    return crud_health.create_health_data(db, health)

@router.get("/{user_id}", response_model=List[HealthRead])
def read_user_health_data(user_id: str, db: Session = Depends(get_db)):
    data = crud_health.get_health_data(db, user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Health data not found")
    return data

