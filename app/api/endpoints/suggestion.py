from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.suggestion import SuggestionCreate, SuggestionUpdate, SuggestionResponse
from app.crud import suggestion as crud
router = APIRouter(
    prefix="/suggestions",
    tags=["Suggestions"]
)
@router.post("/", response_model=SuggestionResponse)
def create_suggestion_endpoint(
    suggestion: SuggestionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_suggestion(db=db, suggestion_data=suggestion)
@router.get("/{suggestion_id}", response_model=SuggestionResponse)
def read_suggestion(
    suggestion_id: str,
    db: Session = Depends(get_db)
):
    db_suggestion = crud.get_suggestion(db=db, suggestion_id=suggestion_id)
    if db_suggestion is None:
        raise HTTPException(status_code=404, detail="Suggestion not found !!")
    return db_suggestion
@router.get("/", response_model=list[SuggestionResponse])
def read_suggestions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_suggestions(db=db, skip=skip, limit=limit)
@router.put("/{suggestion_id}", response_model=SuggestionResponse)
def update_suggestion_endpoint(
    suggestion_id: str,
    updates: SuggestionUpdate,
    db: Session = Depends(get_db)
):
    updated_suggestion = crud.update_suggestion(db=db, suggestion_id=suggestion_id, updates=updates)
    if updated_suggestion is None:
        raise HTTPException(status_code=404, detail="Suggestion not found !!")
    return updated_suggestion
@router.delete("/{suggestion_id}", response_model=dict)
def delete_suggestion_endpoint(
    suggestion_id: str,
    db: Session = Depends(get_db)
):
    success = crud.delete_suggestion(db=db, suggestion_id=suggestion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Suggestion not found !!")
    return {"Suggestion deleted successfully !!"}
