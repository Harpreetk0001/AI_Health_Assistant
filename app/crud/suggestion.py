from sqlalchemy.orm import Session
from models import suggestion as models
from schemas import suggestion as schemas

def create_suggestion(db: Session, suggestion: schemas.SuggestionCreate):
    db_suggestion = models.Suggestion(**suggestion.dict())
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion

def get_suggestions(db: Session, skip=0, limit=100):
    return db.query(models.Suggestion).offset(skip).limit(limit).all()

def get_suggestion(db: Session, suggestion_id: str):
    return db.query(models.Suggestion).filter(models.Suggestion.id == suggestion_id).first()

def update_suggestion(db: Session, suggestion_id: str, updates: schemas.SuggestionUpdate):
    db_suggestion = db.query(models.Suggestion).filter(models.Suggestion.id == suggestion_id).first()
    if db_suggestion:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_suggestion, field, value)
        db.commit()
        db.refresh(db_suggestion)
    return db_suggestion

def delete_suggestion(db: Session, suggestion_id: str):
    db_suggestion = db.query(models.Suggestion).filter(models.Suggestion.id == suggestion_id).first()
    if db_suggestion:
        db.delete(db_suggestion)
        db.commit()
    return db_suggestion
