from fastapi import APIRouter, HTTPException, Depends # Import FastAPI tools for routing, error handling, and dependency injection
from sqlalchemy.orm import Session # Import SQLAlchemy session for database interaction
from app.db.database import get_db # Import function to get the database session from app's database module
from app.schemas.suggestion import SuggestionCreate, SuggestionUpdate, SuggestionResponse # Import data models (schemas) for creating, updating, and responding with suggestions
from app.crud import suggestion as crud # Import the suggestion-related database functions (CRUD operations)
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
# Define a route to delete a suggestion by ID (DELETE /suggestions/{suggestion_id})
@router.delete("/{suggestion_id}", response_model=dict)
def delete_suggestion_endpoint(
    suggestion_id: str,
    db: Session = Depends(get_db)
):
    success = crud.delete_suggestion(db=db, suggestion_id=suggestion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Suggestion not found !!")
    return {"Suggestion deleted successfully !!"}
