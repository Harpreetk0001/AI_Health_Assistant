from app.models import ActivityLog
from app.db.session import db

def create_activity_log(activity_log):
    db.add(activity_log)
    db.commit()
    db.refresh(activity_log)
    return activity_log

def get_activity_log_by_id(activity_log_id):
    return db.query(ActivityLog).filter(ActivityLog.id == activity_log_id).first()
