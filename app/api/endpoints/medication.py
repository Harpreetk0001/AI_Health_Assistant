from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Medication)
def create_medication(med: schemas.MedicationCreate, db: Session = Depends(get_db)):
    return crud.create_medication(db=db, med=med)

@router.get("/{med_id}", response_model=schemas.Medication)
def read_medication(med_id: str, db: Session = Depends(get_db)):
    db_med = crud.get_medication(db, med_id=med_id)
    if not db_med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return db_med

@router.put("/{med_id}", response_model=schemas.Medication)
def update_medication(med_id: str, med: schemas.MedicationUpdate, db: Session = Depends(get_db)):
    return crud.update_medication(db, med_id, med)

@router.delete("/{med_id}")
def delete_medication(med_id: str, db: Session = Depends(get_db)):
    crud.delete_medication(db, med_id)
    return {"ok": True}
