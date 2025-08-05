from sqlalchemy.orm import Session
from models import health_vital as models
from schemas import health_vital as schemas
import uuid

def create_health_vital(db: Session, hv: schemas.HealthVitalCreate):
    db_hv = models.HealthVital(id=str(uuid.uuid4()), **hv.dict())
    db.add(db_hv)
    db.commit()
    db.refresh(db_hv)
    return db_hv

def get_health_vitals(db: Session, user_id: str):
    return db.query(models.HealthVital).filter(models.HealthVital.user_id == user_id).all()

def get_health_vital(db: Session, hv_id: str):
    return db.query(models.HealthVital).filter(models.HealthVital.id == hv_id).first()

def update_health_vital(db: Session, db_hv: models.HealthVital, hv: schemas.HealthVitalUpdate):
    for key, value in hv.dict(exclude_unset=True).items():
        setattr(db_hv, key, value)
    db.commit()
    db.refresh(db_hv)
    return db_hv

def delete_health_vital(db: Session, db_hv: models.HealthVital):
    db.delete(db_hv)
    db.commit()
