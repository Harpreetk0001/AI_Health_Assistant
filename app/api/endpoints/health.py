from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Health)
def create_health_record(health: schemas.HealthCreate, db: Session = Depends(get_db)):
    return crud.create_health_record(db=db, health=health)

@router.get("/{health_id}", response_model=schemas.Health)
def read_health_record(health_id: str, db: Session = Depends(get_db)):
    db_health = crud.get_health_record(db, health_id=health_id)
    if not db_health:
        raise HTTPException(status_code=404, detail="Health record not found")
    return db_health

@router.put("/{health_id}", response_model=schemas.Health)
def update_health_record(health_id: str, health: schemas.HealthUpdate, db: Session = Depends(get_db)):
    return crud.update_health_record(db, health_id, health)

@router.delete("/{health_id}")
def delete_health_record(health_id: str, db: Session = Depends(get_db)):
    crud.delete_health_record(db, health_id)
    return {"ok": True}
