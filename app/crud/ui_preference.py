from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import UIPreferences
from database import get_db
from schemas import UIPreferenceCreate, UIPreferenceOut
import uuid

router = APIRouter(prefix="/ui_preferences", tags=["UI Preferences"])

@router.post("/", response_model=UIPreferenceOut)
def create_ui_pref(data: UIPreferenceCreate, db: Session = Depends(get_db)):
    pref = UIPreferences(**data.dict())
    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref

@router.get("/{pref_id}", response_model=UIPreferenceOut)
def get_ui_pref(pref_id: uuid.UUID, db: Session = Depends(get_db)):
    pref = db.query(UIPreferences).get(pref_id)
    if not pref:
        raise HTTPException(status_code=404, detail="UI preference not found")
    return pref

@router.put("/{pref_id}", response_model=UIPreferenceOut)
def update_ui_pref(pref_id: uuid.UUID, data: UIPreferenceCreate, db: Session = Depends(get_db)):
    pref = db.query(UIPreferences).get(pref_id)
    if not pref:
        raise HTTPException(status_code=404, detail="UI preference not found")
    for key, value in data.dict().items():
        setattr(pref, key, value)
    db.commit()
    db.refresh(pref)
    return pref

@router.delete("/{pref_id}")
def delete_ui_pref(pref_id: uuid.UUID, db: Session = Depends(get_db)):
    pref = db.query(UIPreferences).get(pref_id)
    if not pref:
        raise HTTPException(status_code=404, detail="UI preference not found")
    db.delete(pref)
    db.commit()
    return {"detail": "UI preference deleted"}

