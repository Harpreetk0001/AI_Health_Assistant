from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.health import HealthRecord, HealthRecordCreate
from app.crud import health as crud_health
from typing import List

router = APIRouter()

@router.post("/health_records/", response_model=HealthRecord)
def create_record(record: HealthRecordCreate, db: Session = Depends(get_db)):
    return crud_health.create_health_record(db=db, health=record)

@router.get("/health_records/", response_model=List[HealthRecord])
def read_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_health.get_health_records(db, skip=skip, limit=limit)
