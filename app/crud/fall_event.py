from sqlalchemy.orm import Session
from app.models import fall_event
from app.schemas import fall_event as schemas
import uuid
def create_fall_event(db: Session, event: schemas.FallEventCreate):
    db_event = fall_event.FallEvent(
        id=str(uuid.uuid4()),
        **event.model_dump()
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
def get_fall_events(db: Session, user_id: str):
    return db.query(fall_event.FallEvent).filter(fall_event.FallEvent.user_id == user_id).all()
def get_fall_event(db: Session, event_id: str):
    return db.query(fall_event.FallEvent).filter(fall_event.FallEvent.id == event_id).first()
def update_fall_event(db: Session, db_event: fall_event.FallEvent, event: schemas.FallEventUpdate):
    updates = event.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event
def delete_fall_event(db: Session, db_event: fall_event.FallEvent):
    db.delete(db_event)
    db.commit()
