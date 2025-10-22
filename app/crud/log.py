from sqlalchemy.orm import Session
from app.models.log import Log

def create_log(db: Session, user_id: int | None, action: str):
    l = Log(user_id=user_id, action=action)
    db.add(l); db.commit(); db.refresh(l)
    return l

def get_logs(db: Session, user_id: int | None = None):
    q = db.query(Log)
    if user_id:
        q = q.filter(Log.user_id == user_id)
    return q.order_by(Log.timestamp.desc()).all()
