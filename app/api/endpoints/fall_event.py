from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.fall_event import FallEventBase, FallEventCreate, FallEventUpdate
from app.crud.fall_event import (
    create_fall_event,
    get_fall_event,
    update_fall_event,
    delete_fall_event,
)
from app.db.database import get_db # Import the database session dependency
router = APIRouter(prefix="/fall_events", tags=["Fall Events"]) # Create a router for all "fall event" related API endpoints
@router.post("/", response_model=FallEventBase)
def create_fall_event_endpoint(event: FallEventCreate, db: Session = Depends(get_db)):
    return create_fall_event(db=db, event=event)
@router.get("/{event_id}", response_model=FallEventBase) # Get details of a single fall event by its ID
def read_fall_event(event_id: str, db: Session = Depends(get_db)):
    db_event = get_fall_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Fall event not found !!")
    return db_event
@router.put("/{event_id}", response_model=FallEventBase) # Update details of an existing fall event
def update_fall_event_endpoint(event_id: str, event: FallEventUpdate, db: Session = Depends(get_db)):
    db_event = get_fall_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Fall event not found !!")
    updated_event = update_fall_event(db, db_event, event)
    return updated_event
@router.delete("/{event_id}") # Delete a fall event
def delete_fall_event_endpoint(event_id: str, db: Session = Depends(get_db)):
    db_event = get_fall_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Fall event not found !!")
    success = delete_fall_event(db, db_event=db_event)  # Try deleting the event
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete fall event!!")
    return {"ok": True}
