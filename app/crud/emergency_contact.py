from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import EmergencyContacts
from database import get_db
from schemas import EmergencyContactCreate, EmergencyContactUpdate, EmergencyContactOut
import uuid

router = APIRouter(prefix="/emergency_contacts", tags=["Emergency Contacts"])

@router.post("/", response_model=EmergencyContactOut)
def create_contact(contact: EmergencyContactCreate, db: Session = Depends(get_db)):
    new_contact = EmergencyContacts(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@router.get("/{contact_id}", response_model=EmergencyContactOut)
def get_contact(contact_id: uuid.UUID, db: Session = Depends(get_db)):
    contact = db.query(EmergencyContacts).get(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=EmergencyContactOut)
def update_contact(contact_id: uuid.UUID, updated: EmergencyContactUpdate, db: Session = Depends(get_db)):
    contact = db.query(EmergencyContacts).get(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: uuid.UUID, db: Session = Depends(get_db)):
    contact = db.query(EmergencyContacts).get(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"ok": True}

