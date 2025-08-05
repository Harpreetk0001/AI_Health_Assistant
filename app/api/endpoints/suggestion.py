from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import suggestion as schemas
from crud import suggestion as crud

router = APIRouter()

@router.post("/", response_model=schemas.Suggestion)
def create_suggestion(suggestion: schemas.SuggestionCreate, db: Session = Depends(get_db)):
    return crud.create_suggestion(db=db, suggestion=suggestion)

@router.get("/{suggestion_id}", response_model=schemas.Suggestion)
def read_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    db_suggestion = crud.get_suggestion(db, suggestion_id=suggestion_id)
    if db_suggestion is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return db_suggestion

@router.get("/", response_model=list[schemas.Suggestion])
def read_suggestions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_suggestions(db, skip=skip, limit=limit)

@router.put("/{suggestion_id}", response_model=schemas.Suggestion)
def update_suggestion(suggestion_id: int, suggestion: schemas.SuggestionUpdate, db: Session = Depends(get_db)):
    updated = crud.update_suggestion(db, suggestion_id=suggestion_id, suggestion=suggestion)
    if updated is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return updated

@router.delete("/{suggestion_id}")
def delete_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    success = crud.delete_suggestion(db, suggestion_id=suggestion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return {"message": "Suggestion deleted successfully"}
