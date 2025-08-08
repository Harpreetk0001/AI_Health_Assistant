from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
# Import Pydantic models for UI preference data validation and responses
from app.schemas.ui_preference import (
    UIPreferenceCreate,    # Model for creating a new UI preference
    UIPreferenceUpdate,    # Model for updating an existing UI preference
    UIPreferenceResponse,  # Model used to return UI preference data in responses
)
from app.crud import ui_preference as crud
router = APIRouter(
    prefix="/ui_preferences",
    tags=["UI Preferences"]
)
@router.post("/", response_model=UIPreferenceResponse)
def create_ui_preference_endpoint(
    preference_data: UIPreferenceCreate,  # Data sent by client to create a preference
    db: Session = Depends(get_db)         # Inject database session automatically
):
    return crud.create_ui_preference(db=db, preference=preference_data)
@router.get("/{ui_preference_id}", response_model=UIPreferenceResponse)
def read_ui_preference(
    ui_preference_id: str,
    db: Session = Depends(get_db)
):
    db_pref = crud.get_ui_preference(db, pref_id=ui_preference_id)
    if db_pref is None:
        raise HTTPException(status_code=404, detail="UI preference not found !!")
    return db_pref
@router.get("/", response_model=list[UIPreferenceResponse])
def read_ui_preferences(
    skip: int = 0,        # How many records to skip (for paging)
    limit: int = 100,     # Maximum number of records to return
    db: Session = Depends(get_db)
):
    return crud.get_ui_preferences(db, skip=skip, limit=limit)
@router.put("/{ui_preference_id}", response_model=UIPreferenceResponse)
def update_ui_preference_endpoint(
    ui_preference_id: str,
    updates: UIPreferenceUpdate,
    db: Session = Depends(get_db)
):
    updated_pref = crud.update_ui_preference(db, pref_id=ui_preference_id, updates=updates)
    if updated_pref is None:
        raise HTTPException(status_code=404, detail="UI preference not found !!")
    return updated_pref
@router.delete("/{ui_preference_id}", response_model=dict)
def delete_ui_preference_endpoint(
    ui_preference_id: str,
    db: Session = Depends(get_db)
):
    deleted_pref = crud.delete_ui_preference(db, pref_id=ui_preference_id)
    if deleted_pref is None:
        raise HTTPException(status_code=404, detail="UI preference not found !!")
    return {"UI preference deleted successfully !!"}
