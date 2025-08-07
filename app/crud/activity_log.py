from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog as ModelActivityLog
from app.schemas.activity_log import ActivityLogCreate, ActivityLogUpdate

def create_activity(db: Session, activity: ActivityLogCreate):
    db_activity = ModelActivityLog(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activities(db: Session, skip=0, limit=100):
    return db.query(ModelActivityLog).offset(skip).limit(limit).all()

def get_activity(db: Session, activity_id: str):
    return db.query(ModelActivityLog).filter(ModelActivityLog.id == activity_id).first()

def update_activity(db: Session, activity_id: str, updates: ActivityLogUpdate):
    db_activity = db.query(ModelActivityLog).filter(ModelActivityLog.id == activity_id).first()
    if db_activity:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_activity, field, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: str):
    db_activity = db.query(ModelActivityLog).filter(ModelActivityLog.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity
