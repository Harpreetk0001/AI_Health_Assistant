from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactIn, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.create_contact(db, current_user.id, contact)

@router.get("/", response_model=List[schemas.ContactOut])
def get_contacts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.get_contacts(db, current_user.id)

@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, contact: schemas.ContactIn, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    updated = crud.update_contact(db, contact_id, name=contact.name, relationship=contact.relationship, phone=contact.phone, email=contact.email, profile=contact.profile, favourite=contact.favourite)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ok = crud.delete_contact(db, contact_id)
    return {"success": ok}
