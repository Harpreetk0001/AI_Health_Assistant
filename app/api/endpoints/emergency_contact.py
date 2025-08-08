from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.db.session import get_db
from app.crud.emergency_contact import (
    create_emergency_contact,
    get_emergency_contacts,
    get_emergency_contact,
    update_emergency_contact,
    delete_emergency_contact,
)
from app.schemas.emergency_contact import (
    EmergencyContactBase,
    EmergencyContactCreate,
    EmergencyContactUpdate,
)
router = APIRouter(
    prefix="/emergency_contacts",
    tags=["Emergency Contacts"]
)
@router.post("/", response_model=EmergencyContactBase)
def create(contact: EmergencyContactCreate, db: Session = Depends(get_db)):
    db_contact = create_emergency_contact(db=db, contact=contact)
    return db_contact
@router.get("/", response_model=List[EmergencyContactBase])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_emergency_contacts(db=db, skip=skip, limit=limit)
@router.get("/{contact_id}", response_model=EmergencyContactBase)
def read(contact_id: UUID, db: Session = Depends(get_db)):
    contact = get_emergency_contact(db=db, contact_id=str(contact_id))
    if not contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found !!")
    return contact
@router.put("/{contact_id}", response_model=EmergencyContactBase)
def update(contact_id: UUID, updates: EmergencyContactUpdate, db: Session = Depends(get_db)):
    updated_contact = update_emergency_contact(db=db, contact_id=str(contact_id), updates=updates)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found !!")
    return updated_contact
@router.delete("/{contact_id}")
def delete(contact_id: UUID, db: Session = Depends(get_db)):
    success = delete_emergency_contact(db=db, contact_id=str(contact_id))
    if not success:
        raise HTTPException(status_code=404, detail="Emergency contact not found !!")
    return {"ok": True}
