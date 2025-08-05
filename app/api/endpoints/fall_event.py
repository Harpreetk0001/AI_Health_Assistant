from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.FallEvent)
def create_fall_event(event: schemas.FallEventCreate, db: Session = Depends(get_db)):
    return crud.create_fall_event(db=db, event=event)

@router.get("/{event_id}", response_model=schemas.FallEvent)
def read_fall_event(event_id: str, db: Session = Depends(get_db)):
    db_event = crud.get_fall_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Fall event not found")
    return db_event

@router.put("/{event_id}", response_model=schemas.FallEvent)
def update_fall_event(event_id: str, event: schemas.FallEventUpdate, db: Session = Depends(get_db)):
    return crud.update_fall_event(db, event_id, event)

@router.delete("/{event_id}")
def delete_fall_event(event_id: str, db: Session = Depends(get_db)):
    crud.delete_fall_event(db, event_id)
    return {"ok": True}
