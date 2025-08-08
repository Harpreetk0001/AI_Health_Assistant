from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.suggestion import Suggestion
from app.schemas.suggestion import SuggestionCreate, SuggestionUpdate
def create_suggestion(db: Session, suggestion_data: SuggestionCreate) -> Suggestion:
    db_suggestion = Suggestion(**suggestion_data.model_dump())
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion
def get_suggestions(db: Session, skip: int = 0, limit: int = 100) -> List[Suggestion]:
    return db.query(Suggestion).offset(skip).limit(limit).all()
def get_suggestion(db: Session, suggestion_id: str) -> Optional[Suggestion]:
    return db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
def update_suggestion(db: Session, suggestion_id: str, updates: SuggestionUpdate) -> Optional[Suggestion]:
    db_suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if db_suggestion:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_suggestion, field, value)
        db.commit()
        db.refresh(db_suggestion)
    return db_suggestion
def delete_suggestion(db: Session, suggestion_id: str) -> Optional[Suggestion]:
    db_suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if db_suggestion:
        db.delete(db_suggestion)
        db.commit()
    return db_suggestion
