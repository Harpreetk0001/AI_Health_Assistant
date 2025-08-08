from sqlalchemy.orm import Session
from app.models.emergency_contact import EmergencyContact
from app.schemas.emergency_contact import EmergencyContactCreate, EmergencyContactUpdate
from typing import List, Optional
import uuid
def create_emergency_contact(db: Session, contact: EmergencyContactCreate) -> EmergencyContact:
    db_contact = EmergencyContact(
        id=str(uuid.uuid4()),
        **contact.model_dump()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
def get_emergency_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[EmergencyContact]:
    return db.query(EmergencyContact).offset(skip).limit(limit).all()
def get_emergency_contact(db: Session, contact_id: str) -> Optional[EmergencyContact]:
    return db.query(EmergencyContact).filter(EmergencyContact.id == contact_id).first()
def update_emergency_contact(
    db: Session,
    contact_id: str,
    updates: EmergencyContactUpdate
) -> Optional[EmergencyContact]:
    db_contact = get_emergency_contact(db, contact_id)
    if not db_contact:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact
def delete_emergency_contact(db: Session, contact_id: str) -> bool:
    db_contact = get_emergency_contact(db, contact_id)
    if not db_contact:
        return False
    db.delete(db_contact)
    db.commit()
    return True
