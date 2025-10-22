from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactIn

def create_contact(db: Session, user_id: int, contact_in: ContactIn):
    c = Contact(
        user_id=user_id,
        name=contact_in.name,
        relationship=contact_in.relationship,
        phone=contact_in.phone,
        email=contact_in.email,
        profile=contact_in.profile,
        favourite=contact_in.favourite
    )
    db.add(c); db.commit(); db.refresh(c)
    return c

def get_contacts(db: Session, user_id: int):
    return db.query(Contact).filter(Contact.user_id == user_id).all()

def update_contact(db: Session, contact_id: int, **kwargs):
    c = db.query(Contact).filter(Contact.id == contact_id).first()
    if not c: return None
    for k, v in kwargs.items():
        if hasattr(c, k):
            setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c

def delete_contact(db: Session, contact_id: int):
    c = db.query(Contact).filter(Contact.id == contact_id).first()
    if not c: return False
    db.delete(c); db.commit()
    return True
