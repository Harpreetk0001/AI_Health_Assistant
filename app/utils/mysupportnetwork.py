from typing import List, Optional, Any
from sqlalchemy.orm import Session

# Defensive imports
try:
    from app import crud
    from app import models
except Exception:
    crud = None
    models = None


class Contact:
    def __init__(self, name: str, relationship: str = "", phone_no: str = "", email: str = "", profile: str = "", favourite: bool = False, id: Optional[int] = None):
        self.name = name
        self.relationship = relationship
        self.phone_no = phone_no
        self.email = email
        self.profile = profile
        self.favourite = favourite
        self.id = id

    def as_dict(self):
        return {
            "name": self.name,
            "relationship": self.relationship,
            "phone": self.phone_no,
            "email": self.email,
            "profile": self.profile,
            "favourite": self.favourite
        }


class ContactList:
    def __init__(self, user_id: Optional[int] = None):
        self.contacts: List[Contact] = []
        self.emergencyContacts: List[Contact] = []
        self.user_id = user_id

    def addContact(self, db: Optional[Session], c: Contact) -> Optional[Any]:
        """Add to memory and persist"""
        self.contacts.append(c)
        if c.favourite:
            self.emergencyContacts.append(c)
        db_record = None
        if db is not None:
            try:
                if crud and hasattr(crud, "create_contact"):
                    db_record = crud.create_contact(db, self.user_id, type("X",(object,),{
                        "name": c.name, "relationship": c.relationship, "phone": c.phone_no,
                        "email": c.email, "profile": c.profile, "favourite": c.favourite
                    })())
                elif models and hasattr(models, "Contact"):
                    rec = models.Contact(
                        user_id=self.user_id,
                        name=c.name,
                        relationship=c.relationship,
                        phone=c.phone_no,
                        email=c.email,
                        profile=c.profile,
                        favourite=c.favourite
                    )
                    db.add(rec); db.commit(); db.refresh(rec)
                    db_record = rec
                if db_record and hasattr(db_record, "id"):
                    c.id = getattr(db_record, "id")
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass
                db_record = None
        return db_record

    def updateContact(self, db: Optional[Session], c: Contact, attribute: str, new_value) -> Optional[Any]:
        if c not in self.contacts:
            return None
        setattr(c, attribute, new_value)
        # refresh emergencyContacts
        self.emergencyContacts = [x for x in self.contacts if x.favourite]
        db_record = None
        if db is not None and c.id:
            try:
                if crud and hasattr(crud, "update_contact"):
                    db_record = crud.update_contact(db, c.id, **{attribute: new_value})
                elif models and hasattr(models, "Contact"):
                    rec = db.query(models.Contact).filter(models.Contact.id == c.id).first()
                    if rec:
                        setattr(rec, attribute, new_value)
                        db.commit(); db.refresh(rec)
                        db_record = rec
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass
                db_record = None
        return db_record

    def deleteContact(self, db: Optional[Session], c: Contact) -> bool:
        if c in self.contacts:
            self.contacts.remove(c)
        if c in self.emergencyContacts:
            self.emergencyContacts.remove(c)
        ok = True
        if db is not None and c.id:
            try:
                if crud and hasattr(crud, "delete_contact"):
                    ok = crud.delete_contact(db, c.id)
                elif models and hasattr(models, "Contact"):
                    rec = db.query(models.Contact).filter(models.Contact.id == c.id).first()
                    if rec:
                        db.delete(rec); db.commit()
                        ok = True
                    else:
                        ok = False
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass
                ok = False
        return ok

    def listContacts(self) -> List[Contact]:
        return list(self.contacts)

    def listEmergencyContacts(self) -> List[Contact]:
        return list(self.emergencyContacts)
