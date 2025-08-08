from sqlalchemy.orm import Session
from app.models import health_vital
from app.schemas import health_vital as schemas
import uuid
def create_health_vital(db: Session, hv: schemas.HealthVitalCreate):
    db_hv = health_vital.HealthVital(
        id=str(uuid.uuid4()),
        **hv.model_dump()
    )
    db.add(db_hv)
    db.commit()
    db.refresh(db_hv)
    return db_hv
def get_health_vitals(db: Session, user_id: str):
    return db.query(health_vital.HealthVital).filter(health_vital.HealthVital.user_id == user_id).all()
def get_health_vital(db: Session, hv_id: str):
    return db.query(health_vital.HealthVital).filter(health_vital.HealthVital.id == hv_id).first()
def update_health_vital(db: Session, db_hv: health_vital.HealthVital, hv: schemas.HealthVitalUpdate):
    updates = hv.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(db_hv, key, value)
    db.commit()
    db.refresh(db_hv)
    return db_hv
def delete_health_vital(db: Session, db_hv: health_vital.HealthVital):
    db.delete(db_hv)
    db.commit()
