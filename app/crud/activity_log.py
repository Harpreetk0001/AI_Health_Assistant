from sqlalchemy.orm import Session
from uuid import UUID
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate, ActivityLogUpdate
def create_activity(db: Session, activity: ActivityLogCreate):
    db_activity = ActivityLog(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity
def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ActivityLog).offset(skip).limit(limit).all()
def get_activity(db: Session, activity_id: UUID):
    return db.query(ActivityLog).filter(ActivityLog.id == activity_id).first()
def update_activity(db: Session, activity_id: UUID, updates: ActivityLogUpdate):
    db_activity = db.query(ActivityLog).filter(ActivityLog.id == activity_id).first()
    if db_activity:
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_activity, field, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity
def delete_activity(db: Session, activity_id: UUID):
    db_activity = db.query(ActivityLog).filter(ActivityLog.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity
