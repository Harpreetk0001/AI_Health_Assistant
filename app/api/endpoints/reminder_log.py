from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import reminder_log as schemas
from crud import reminder_log as crud

router = APIRouter()

@router.post("/", response_model=schemas.ReminderLog)
def create_reminder_log(reminder_log: schemas.ReminderLogCreate, db: Session = Depends(get_db)):
    return crud.create_reminder_log(db=db, reminder_log=reminder_log)

@router.get("/{reminder_log_id}", response_model=schemas.ReminderLog)
def read_reminder_log(reminder_log_id: int, db: Session = Depends(get_db)):
    db_reminder_log = crud.get_reminder_log(db, reminder_log_id=reminder_log_id)
    if db_reminder_log is None:
        raise HTTPException(status_code=404, detail="Reminder log not found")
    return db_reminder_log

@router.get("/", response_model=list[schemas.ReminderLog])
def read_reminder_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reminder_logs(db, skip=skip, limit=limit)

@router.put("/{reminder_log_id}", response_model=schemas.ReminderLog)
def update_reminder_log(reminder_log_id: int, reminder_log: schemas.ReminderLogUpdate, db: Session = Depends(get_db)):
    updated = crud.update_reminder_log(db, reminder_log_id=reminder_log_id, reminder_log=reminder_log)
    if updated is None:
        raise HTTPException(status_code=404, detail="Reminder log not found")
    return updated

@router.delete("/{reminder_log_id}")
def delete_reminder_log(reminder_log_id: int, db: Session = Depends(get_db)):
    success = crud.delete_reminder_log(db, reminder_log_id=reminder_log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder log not found")
    return {"message": "Reminder log deleted successfully"}
