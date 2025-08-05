from sqlalchemy.orm import Session
from models import activity as models
from schemas import activity as schemas

def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activities(db: Session, skip=0, limit=100):
    return db.query(models.Activity).offset(skip).limit(limit).all()

def get_activity(db: Session, activity_id: str):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()

def update_activity(db: Session, activity_id: str, updates: schemas.ActivityUpdate):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_activity, field, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: str):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity
