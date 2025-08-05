from sqlalchemy.orm import Session
from models import reminder_log as models
from schemas import reminder_log as schemas

def create_reminder(db: Session, reminder: schemas.ReminderLogCreate):
    db_reminder = models.ReminderLog(**reminder.dict())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

def get_reminders(db: Session, skip=0, limit=100):
    return db.query(models.ReminderLog).offset(skip).limit(limit).all()

def get_reminder(db: Session, reminder_id: str):
    return db.query(models.ReminderLog).filter(models.ReminderLog.id == reminder_id).first()

def update_reminder(db: Session, reminder_id: str, updates: schemas.ReminderLogUpdate):
    db_reminder = db.query(models.ReminderLog).filter(models.ReminderLog.id == reminder_id).first()
    if db_reminder:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_reminder, field, value)
        db.commit()
        db.refresh(db_reminder)
    return db_reminder

def delete_reminder(db: Session, reminder_id: str):
    db_reminder = db.query(models.ReminderLog).filter(models.ReminderLog.id == reminder_id).first()
    if db_reminder:
        db.delete(db_reminder)
        db.commit()
    return db_reminder

