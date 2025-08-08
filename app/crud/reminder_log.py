from sqlalchemy.orm import Session
from app.models.reminder_log import ReminderLog
from app.schemas.reminder_log import ReminderLogCreate, ReminderLogUpdate
def create_reminder(db: Session, reminder: ReminderLogCreate):
    db_reminder = ReminderLog(**reminder.model_dump())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder
def get_reminders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ReminderLog).offset(skip).limit(limit).all()
def get_reminder(db: Session, reminder_id: str):
    return db.query(ReminderLog).filter(ReminderLog.id == reminder_id).first()
def update_reminder(db: Session, reminder_id: str, updates: ReminderLogUpdate):
    db_reminder = db.query(ReminderLog).filter(ReminderLog.id == reminder_id).first()
    if db_reminder:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_reminder, field, value)
        db.commit()
        db.refresh(db_reminder)
    return db_reminder
def delete_reminder(db: Session, reminder_id: str):
    db_reminder = db.query(ReminderLog).filter(ReminderLog.id == reminder_id).first()
    if db_reminder:
        db.delete(db_reminder)
        db.commit()
    return db_reminder
