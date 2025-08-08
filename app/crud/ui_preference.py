from sqlalchemy.orm import Session
from app.models.ui_preference import UIPreference
from app.schemas.ui_preference import UIPreferenceCreate, UIPreferenceUpdate
def create_ui_preference(db: Session, preference: UIPreferenceCreate):
    db_pref = UIPreference(**preference.model_dump())
    db.add(db_pref)
    db.commit()
    db.refresh(db_pref)
    return db_pref
def get_ui_preferences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UIPreference).offset(skip).limit(limit).all()
def get_ui_preference(db: Session, pref_id: str):
    return db.query(UIPreference).filter(UIPreference.id == pref_id).first()
def update_ui_preference(db: Session, pref_id: str, updates: UIPreferenceUpdate):
    db_pref = db.query(UIPreference).filter(UIPreference.id == pref_id).first()
    if db_pref:
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pref, field, value)
        db.commit()
        db.refresh(db_pref)
    return db_pref
def delete_ui_preference(db: Session, pref_id: str):
    db_pref = db.query(UIPreference).filter(UIPreference.id == pref_id).first()
    if db_pref:
        db.delete(db_pref)
        db.commit()
    return db_pref
