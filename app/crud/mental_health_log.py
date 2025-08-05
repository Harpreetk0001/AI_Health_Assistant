from sqlalchemy.orm import Session
from models import mental_health_log as models
from schemas import mental_health_log as schemas

def create_mental_health_log(db: Session, log: schemas.MentalHealthLogCreate):
    db_log = models.MentalHealthLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_mental_health_logs(db: Session, skip=0, limit=100):
    return db.query(models.MentalHealthLog).offset(skip).limit(limit).all()

def get_mental_health_log(db: Session, log_id: str):
    return db.query(models.MentalHealthLog).filter(models.MentalHealthLog.id == log_id).first()

def update_mental_health_log(db: Session, log_id: str, updates: schemas.MentalHealthLogUpdate):
    db_log = db.query(models.MentalHealthLog).filter(models.MentalHealthLog.id == log_id).first()
    if db_log:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_log, field, value)
        db.commit()
        db.refresh(db_log)
    return db_log

def delete_mental_health_log(db: Session, log_id: str):
    db_log = db.query(models.MentalHealthLog).filter(models.MentalHealthLog.id == log_id).first()
    if db_log:
        db.delete(db_log)
        db.commit()
    return db_log


