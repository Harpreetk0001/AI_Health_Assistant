from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.medication import Medication, MedicationCreate, MedicationUpdate
from app.crud.medication import (
    create_medication,
    get_medication,
    update_medication,
    delete_medication,
)
from app.db.database import get_db
router = APIRouter(prefix="/medications", tags=["Medications"])
@router.post("/", response_model=Medication)
def create_medication_endpoint(
    med: MedicationCreate, db: Session = Depends(get_db)
):
    created = create_medication(db=db, med=med)
    return created.model_dump()
@router.get("/{med_id}", response_model=Medication)
def read_medication(med_id: UUID, db: Session = Depends(get_db)):
    db_med = get_medication(db, med_id=med_id)
    if db_med is None:
        raise HTTPException(status_code=404, detail="Medication not found !!")
    return db_med.model_dump()
@router.put("/{med_id}", response_model=Medication)
def update_medication_endpoint(
    med_id: UUID, med: MedicationUpdate, db: Session = Depends(get_db)
):
    updated_med = update_medication(db=db, med_id=med_id, med=med)
    if updated_med is None:
        raise HTTPException(status_code=404, detail="Medication not found !!")
    return updated_med.model_dump()
@router.delete("/{med_id}")
def delete_medication_endpoint(med_id: UUID, db: Session = Depends(get_db)):
    result = delete_medication(db, med_id)
    if not result:
        raise HTTPException(status_code=404, detail="Medication not found !!")
    return {"ok": True}
