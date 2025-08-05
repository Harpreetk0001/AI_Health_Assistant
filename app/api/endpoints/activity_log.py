from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
import crud.activity as crud
import schemas.activity as schemas

router = APIRouter(prefix="/activity_logs", tags=["Activity Logs"])

@router.post("/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return crud.create_activity(db=db, activity=activity)

@router.get("/", response_model=list[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_activities(db=db, skip=skip, limit=limit)

@router.get("/{activity_id}", response_model=schemas.Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = crud.get_activity(db, activity_id=activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.put("/{activity_id}", response_model=schemas.Activity)
def update_activity(activity_id: int, activity: schemas.ActivityUpdate, db: Session = Depends(get_db)):
    return crud.update_activity(db, activity_id=activity_id, activity=activity)

@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    crud.delete_activity(db, activity_id=activity_id)
    return {"ok": True}
