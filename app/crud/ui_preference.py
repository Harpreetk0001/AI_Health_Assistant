from sqlalchemy.orm import Session
from models import ui_preference as models
from schemas import ui_preference as schemas

def create_ui_preference(db: Session, preference: schemas.UIPreferenceCreate):
    db_pref = models.UIPreference(**preference.dict())
    db.add(db_pref)
    db.commit()
    db.refresh(db_pref)
    return db_pref

def get_ui_preferences(db: Session, skip=0, limit=100):
    return db.query(models.UIPreference).offset(skip).limit(limit).all()

def get_ui_preference(db: Session, pref_id: str):
    return db.query(models.UIPreference).filter(models.UIPreference.id == pref_id).first()

def update_ui_preference(db: Session, pref_id: str, updates: schemas.UIPreferenceUpdate):
    db_pref = db.query(models.UIPreference).filter(models.UIPreference.id == pref_id).first()
    if db_pref:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_pref, field, value)
        db.commit()
        db.refresh(db_pref)
    return db_pref

def delete_ui_preference(db: Session, pref_id: str):
    db_pref = db.query(models.UIPreference).filter(models.UIPreference.id == pref_id).first()
    if db_pref:
        db.delete(db_pref)
        db.commit()
    return db_pref


