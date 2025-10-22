from sqlalchemy.orm import Session
from app.models.vital import Vitals
from app.schemas.vital import VitalsIn
import datetime

def create_vitals(db: Session, user_id: int, vitals_in: VitalsIn):
    db_v = Vitals(
        user_id=user_id,
        hydration=vitals_in.hydration,
        sleep=vitals_in.sleep,
        heartbeat=vitals_in.heartbeat,
        bp_systolic=vitals_in.bp_systolic,
        bp_diastolic=vitals_in.bp_diastolic,
        steps=vitals_in.steps,
        timestamp=vitals_in.timestamp or datetime.datetime.utcnow()
    )
    db.add(db_v)
    db.commit()
    db.refresh(db_v)
    return db_v

def get_vitals_for_user(db: Session, user_id: int):
    return db.query(Vitals).filter(Vitals.user_id == user_id).order_by(Vitals.timestamp).all()
