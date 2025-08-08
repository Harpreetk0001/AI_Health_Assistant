from fastapi import APIRouter, HTTPException, Depends # Import tools from FastAPI for creating routes, handling errors, and managing dependencies
from sqlalchemy.orm import Session
from app.db.database import get_db # Import function to get a database connection
# Import the data shapes (schemas) for creating, updating, and returning reminder logs
from app.schemas.reminder_log import (
    ReminderLogCreate,
    ReminderLogUpdate,
    ReminderLogResponse,
)
from app.crud import reminder_log as crud

router = APIRouter(
    prefix="/reminder_logs",
    tags=["Reminder Logs"]
)
@router.post("/", response_model=ReminderLogResponse)
def create_reminder_log(reminder_data: ReminderLogCreate, db: Session = Depends(get_db)):
    return crud.create_reminder(db=db, reminder=reminder_data)
@router.get("/{reminder_id}", response_model=ReminderLogResponse)
def get_reminder_log(reminder_id: str, db: Session = Depends(get_db)):
    db_log = crud.get_reminder(db=db, reminder_id=reminder_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Reminder log not found !!")
    return db_log
# Get a list of reminder logs (with optional skip/limit for pagination)
@router.get("/", response_model=list[ReminderLogResponse])
def list_reminder_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reminders(db=db, skip=skip, limit=limit)
@router.put("/{reminder_id}", response_model=ReminderLogResponse)
def update_reminder_log(reminder_id: str, update_data: ReminderLogUpdate, db: Session = Depends(get_db)):
    updated_log = crud.update_reminder(db=db, reminder_id=reminder_id, updates=update_data)
    if updated_log is None:
        raise HTTPException(status_code=404, detail="Reminder log not found !!")
    return updated_log
@router.delete("/{reminder_id}", response_model=dict) # Delete a reminder log
def delete_reminder_log(reminder_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_reminder(db=db, reminder_id=reminder_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reminder log not found !!")
    return {"Reminder log deleted successfully !!"}
