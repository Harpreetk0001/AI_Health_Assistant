from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import ui_preference as schemas
from crud import ui_preference as crud

router = APIRouter()

@router.post("/", response_model=schemas.UIPreference)
def create_ui_preference(ui_preference: schemas.UIPreferenceCreate, db: Session = Depends(get_db)):
    return crud.create_ui_preference(db=db, ui_preference=ui_preference)

@router.get("/{ui_preference_id}", response_model=schemas.UIPreference)
def read_ui_preference(ui_preference_id: int, db: Session = Depends(get_db)):
    db_ui_preference = crud.get_ui_preference(db, ui_preference_id=ui_preference_id)
    if db_ui_preference is None:
        raise HTTPException(status_code=404, detail="UI preference not found")
    return db_ui_preference

@router.get("/", response_model=list[schemas.UIPreference])
def read_ui_preferences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_ui_preferences(db, skip=skip, limit=limit)

@router.put("/{ui_preference_id}", response_model=schemas.UIPreference)
def update_ui_preference(ui_preference_id: int, ui_preference: schemas.UIPreferenceUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ui_preference(db, ui_preference_id=ui_preference_id, ui_preference=ui_preference)
    if updated is None:
        raise HTTPException(status_code=404, detail="UI preference not found")
    return updated

@router.delete("/{ui_preference_id}")
def delete_ui_preference(ui_preference_id: int, db: Session = Depends(get_db)):
    success = crud.delete_ui_preference(db, ui_preference_id=ui_preference_id)
    if not success:
        raise HTTPException(status_code=404, detail="UI preference not found")
    return {"message": "UI preference deleted successfully"}
