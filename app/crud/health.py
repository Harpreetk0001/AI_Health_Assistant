from sqlalchemy.orm import Session
from app.models.health import HealthData
from app.schemas.health import HealthCreate

def create_health_data(db: Session, health: HealthCreate):
    db_health = HealthData(**health.dict())
    db.add(db_health)
    db.commit()
    db.refresh(db_health)
    return db_health

def get_health_data(db: Session, user_id: str):
    return db.query(HealthData).filter(HealthData.user_id == user_id).all()
