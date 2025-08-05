from sqlalchemy.orm import Session
from models import fall_event as models
from schemas import fall_event as schemas
import uuid

def create_fall_event(db: Session, event: schemas.FallEventCreate):
    db_event = models.FallEvent(id=str(uuid.uuid4()), **event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_fall_events(db: Session, user_id: str):
    return db.query(models.FallEvent).filter(models.FallEvent.user_id == user_id).all()

def get_fall_event(db: Session, event_id: str):
    return db.query(models.FallEvent).filter(models.FallEvent.id == event_id).first()

def update_fall_event(db: Session, db_event: models.FallEvent, event: schemas.FallEventUpdate):
    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_fall_event(db: Session, db_event: models.FallEvent):
    db.delete(db_event)
    db.commit()
