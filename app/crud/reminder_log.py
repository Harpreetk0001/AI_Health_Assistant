from app.models import ReminderLog
from app.db.session import db

def create_reminder_log(reminder):
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_reminder_log_by_id(reminder_id):
    return db.query(ReminderLog).filter(ReminderLog.id == reminder_id).first()
