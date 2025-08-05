from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.MentalHealthLog)
def create_mental_health_log(log: schemas.MentalHealthLogCreate, db: Session = Depends(get_db)):
    return crud.create_mental_health_log(db=db, log=log)

@router.get("/{log_id}", response_model=schemas.MentalHealthLog)
def read_mental_health_log(log_id: str, db: Session = Depends(get_db)):
    db_log = crud.get_mental_health_log(db, log_id=log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Mental health log not found")
    return db_log

@router.put("/{log_id}", response_model=schemas.MentalHealthLog)
def update_mental_health_log(log_id: str, log: schemas.MentalHealthLogUpdate, db: Session = Depends(get_db)):
    return crud.update_mental_health_log(db, log_id, log)

@router.delete("/{log_id}")
def delete_mental_health_log(log_id: str, db: Session = Depends(get_db)):
    crud.delete_mental_health_log(db, log_id)
    return {"ok": True}
