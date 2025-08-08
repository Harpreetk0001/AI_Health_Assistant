from fastapi import APIRouter, Depends, HTTPException # Import tools from FastAPI for creating routes, handling dependencies, and raising errors
from sqlalchemy.orm import Session # Import Session from SQLAlchemy to talk to the database
# Import Pydantic schemas for mental health logs 
from app.schemas.mental_health_log import (
    MentalHealthLogBase,
    MentalHealthLogCreate,
    MentalHealthLogUpdate,
)
# Import database functions for mental health logs (CRUD = Create, Read, Update, Delete)
from app.crud.mental_health_log import (
    create_mental_health_log,
    get_mental_health_log,
    update_mental_health_log,
    delete_mental_health_log,
)
from app.db.database import get_db # Import the function to get a database connection
router = APIRouter(prefix="/mental-health-logs", tags=["Mental Health Logs"])
@router.post("/", response_model=MentalHealthLogBase)
def create_log_endpoint(
    log_data: MentalHealthLogCreate, db: Session = Depends(get_db)
):
    return create_mental_health_log(db=db, log_data=log_data)
@router.get("/{log_id}", response_model=MentalHealthLogBase)
def read_log_endpoint(log_id: str, db: Session = Depends(get_db)):
    db_log = get_mental_health_log(db=db, log_id=log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Mental health log not found !!")
    return db_log
@router.put("/{log_id}", response_model=MentalHealthLogBase)
def update_log_endpoint(
    log_id: str, updates: MentalHealthLogUpdate, db: Session = Depends(get_db)
):
    updated_log = update_mental_health_log(db=db, log_id=log_id, updates=updates)
    if updated_log is None:
        raise HTTPException(status_code=404, detail="Mental health log not found !!")
    return updated_log
@router.delete("/{log_id}")
def delete_log_endpoint(log_id: str, db: Session = Depends(get_db)):
    success = delete_mental_health_log(db=db, log_id=log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mental health log not found !!")
    return {"ok": True}
