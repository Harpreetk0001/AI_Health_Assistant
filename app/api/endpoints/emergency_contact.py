from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.EmergencyContact)
def create_emergency_contact(contact: schemas.EmergencyContactCreate, db: Session = Depends(get_db)):
    return crud.create_emergency_contact(db=db, contact=contact)

@router.get("/{contact_id}", response_model=schemas.EmergencyContact)
def read_emergency_contact(contact_id: str, db: Session = Depends(get_db)):
    db_contact = crud.get_emergency_contact(db, contact_id=contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=schemas.EmergencyContact)
def update_emergency_contact(contact_id: str, contact: schemas.EmergencyContactUpdate, db: Session = Depends(get_db)):
    return crud.update_emergency_contact(db, contact_id, contact)

@router.delete("/{contact_id}")
def delete_emergency_contact(contact_id: str, db: Session = Depends(get_db)):
    crud.delete_emergency_contact(db, contact_id)
    return {"ok": True}
