from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from db import get_db
from models import FallEvents
from schemas import FallEventCreate, FallEventUpdate

router = APIRouter(prefix="/fall_events", tags=["Fall Events"])

@router.post("/", response_model=FallEventCreate)
def create_fall_event(event: FallEventCreate, db: Session = Depends(get_db)):
    new_event = FallEvents(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/{event_id}", response_model=FallEventCreate)
def get_fall_event(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(FallEvents).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Fall event not found")
    return event

@router.put("/{event_id}", response_model=FallEventCreate)
def update_fall_event(event_id: UUID, event_update: FallEventUpdate, db: Session = Depends(get_db)):
    event = db.query(FallEvents).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Fall event not found")
    for key, value in event_update.dict(exclude_unset=True).items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_fall_event(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(FallEvents).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Fall event not found")
    db.delete(event)
    db.commit()
    return {"message": "Fall event deleted"}

