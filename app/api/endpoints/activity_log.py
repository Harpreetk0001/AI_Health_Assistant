from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.db.session import get_db
from app.crud import activity_log as crud
from app.schemas.activity_log import (
    ActivityLogCreate,
    ActivityLogUpdate,
    ActivityLog
)
router = APIRouter(
    prefix="/activity_logs",
    tags=["Activity Logs"]
)
@router.post("/", response_model=ActivityLog)
def create_activity(
    activity: ActivityLogCreate,
    db: Session = Depends(get_db)
):
    return crud.create_activity(db=db, activity=activity)
@router.get("/", response_model=List[ActivityLog])
def read_activities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_activities(db=db, skip=skip, limit=limit)
@router.get("/{activity_id}", response_model=ActivityLog)
def read_activity(
    activity_id: UUID,
    db: Session = Depends(get_db)
):
    db_activity = crud.get_activity(db, activity_id=activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity
@router.put("/{activity_id}", response_model=ActivityLog)
def update_activity(
    activity_id: UUID,
    activity: ActivityLogUpdate,
    db: Session = Depends(get_db)
):
    updated_activity = crud.update_activity(db, activity_id=activity_id, updates=activity)
    if not updated_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated_activity
@router.delete("/{activity_id}")
def delete_activity(
    activity_id: UUID,
    db: Session = Depends(get_db)
):
    deleted_activity = crud.delete_activity(db, activity_id=activity_id)
    if not deleted_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"ok": True}
