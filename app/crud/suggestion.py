from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Suggestions
from database import get_db
from schemas import SuggestionCreate, SuggestionOut
import uuid

router = APIRouter(prefix="/suggestions", tags=["Suggestions"])

@router.post("/", response_model=SuggestionOut)
def create_suggestion(data: SuggestionCreate, db: Session = Depends(get_db)):
    suggestion = Suggestions(**data.dict())
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion

@router.get("/{suggestion_id}", response_model=SuggestionOut)
def get_suggestion(suggestion_id: uuid.UUID, db: Session = Depends(get_db)):
    suggestion = db.query(Suggestions).get(suggestion_id)
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return suggestion

@router.put("/{suggestion_id}", response_model=SuggestionOut)
def update_suggestion(suggestion_id: uuid.UUID, data: SuggestionCreate, db: Session = Depends(get_db)):
    suggestion = db.query(Suggestions).get(suggestion_id)
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    for key, value in data.dict().items():
        setattr(suggestion, key, value)
    db.commit()
    db.refresh(suggestion)
    return suggestion

@router.delete("/{suggestion_id}")
def delete_suggestion(suggestion_id: uuid.UUID, db: Session = Depends(get_db)):
    suggestion = db.query(Suggestions).get(suggestion_id)
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    db.delete(suggestion)
    db.commit()
    return {"detail": "Suggestion deleted"}

