from sqlalchemy.orm import Session
from app.models.mental_health_log import MentalHealthLog
from app.schemas.mental_health_log import MentalHealthLogCreate, MentalHealthLogUpdate
def create_mental_health_log(db: Session, log_data: MentalHealthLogCreate):
    db_log = MentalHealthLog(**log_data.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
def get_mental_health_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MentalHealthLog).offset(skip).limit(limit).all()
def get_mental_health_log(db: Session, log_id: str):
    return db.query(MentalHealthLog).filter(MentalHealthLog.id == log_id).first()
def update_mental_health_log(db: Session, log_id: str, updates: MentalHealthLogUpdate):
    db_log = db.query(MentalHealthLog).filter(MentalHealthLog.id == log_id).first()
    if db_log:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_log, field, value)
        db.commit()
        db.refresh(db_log)
    return db_log
def delete_mental_health_log(db: Session, log_id: str):
    db_log = db.query(MentalHealthLog).filter(MentalHealthLog.id == log_id).first()
    if db_log:
        db.delete(db_log)
        db.commit()
    return db_log
