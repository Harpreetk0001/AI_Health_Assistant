from sqlalchemy.orm import Session
from models import emergency_contact as models
from schemas import emergency_contact as schemas
import uuid

def create_emergency_contact(db: Session, contact: schemas.EmergencyContactCreate):
    db_contact = models.EmergencyContact(id=str(uuid.uuid4()), **contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_emergency_contacts(db: Session, user_id: str):
    return db.query(models.EmergencyContact).filter(models.EmergencyContact.user_id == user_id).all()

def get_emergency_contact(db: Session, contact_id: str):
    return db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id).first()

def update_emergency_contact(db: Session, db_contact: models.EmergencyContact, contact: schemas.EmergencyContactUpdate):
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_emergency_contact(db: Session, db_contact: models.EmergencyContact):
    db.delete(db_contact)
    db.commit()
