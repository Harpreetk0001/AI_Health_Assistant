from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import MentalHealthLogs
from database import get_db
from schemas import MentalHealthLogCreate, MentalHealthLogOut
import uuid

router = APIRouter(prefix="/mental_health_logs", tags=["Mental Health Logs"])

@router.post("/", response_model=MentalHealthLogOut)
def create_log(data: MentalHealthLogCreate, db: Session = Depends(get_db)):
    log = MentalHealthLogs(**data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/{log_id}", response_model=MentalHealthLogOut)
def get_log(log_id: uuid.UUID, db: Session = Depends(get_db)):
    log = db.query(MentalHealthLogs).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Mental health log not found")
    return log

@router.put("/{log_id}", response_model=MentalHealthLogOut)
def update_log(log_id: uuid.UUID, data: MentalHealthLogCreate, db: Session = Depends(get_db)):
    log = db.query(MentalHealthLogs).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Mental health log not found")
    for key, value in data.dict().items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    return log

@router.delete("/{log_id}")
def delete_log(log_id: uuid.UUID, db: Session = Depends(get_db)):
    log = db.query(MentalHealthLogs).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Mental health log not found")
    db.delete(log)
    db.commit()
    return {"detail": "Mental health log deleted"}

