from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.HealthVital)
def create_health_vital(vital: schemas.HealthVitalCreate, db: Session = Depends(get_db)):
    return crud.create_health_vital(db=db, vital=vital)

@router.get("/{vital_id}", response_model=schemas.HealthVital)
def read_health_vital(vital_id: str, db: Session = Depends(get_db)):
    db_vital = crud.get_health_vital(db, vital_id=vital_id)
    if not db_vital:
        raise HTTPException(status_code=404, detail="Health vital not found")
    return db_vital

@router.put("/{vital_id}", response_model=schemas.HealthVital)
def update_health_vital(vital_id: str, vital: schemas.HealthVitalUpdate, db: Session = Depends(get_db)):
    return crud.update_health_vital(db, vital_id, vital)

@router.delete("/{vital_id}")
def delete_health_vital(vital_id: str, db: Session = Depends(get_db)):
    crud.delete_health_vital(db, vital_id)
    return {"ok": True}
