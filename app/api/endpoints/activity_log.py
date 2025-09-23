from fastapi import APIRouter, Depends, HTTPException  # Import FastAPI tools: APIRouter (for grouping routes), Depends (for dependencies), HTTPException (for errors)
from sqlalchemy.orm import Session  # Import Session so we can talk to the database
from uuid import UUID  # Import UUID type for unique activity IDs
from typing import List  # Import List type hint for returning multiple items
from app.db.session import get_db  # Get the database session dependency function
from app.crud import activity_log as crud  # Bring in the activity_log CRUD operations (create, read, update, delete)
# Import data validation schemas for activity logs
from app.schemas.activity_log import (
    ActivityLogCreate,  # Schema for creating an activity
    ActivityLogUpdate,  # Schema for updating an activity
    ActivityLog         # Schema for returning an activity
)
# Create a router just for "Activity Logs" related endpoints
router = APIRouter(
    prefix="/activity_logs",   # All routes here will start with /activity_logs
    tags=["Activity Logs"]     # Tag for grouping in API docs
)
# Endpoint: Create a new activity log
@router.post("/", response_model=ActivityLog)
def create_activity(
    activity: ActivityLogCreate,         # The new activity data from the request
    db: Session = Depends(get_db)        # Get a database session automatically
):
    return crud.create_activity(db=db, activity=activity)  # Save it to the database
# Endpoint: Get a list of all activity logs (with optional pagination)
@router.get("/", response_model=List[ActivityLog])
def read_activities(
    skip: int = 0,                        # How many items to skip (for pagination)
    limit: int = 100,                     # Max number of items to return
    db: Session = Depends(get_db)         # Database session
):
    return crud.get_activities(db=db, skip=skip, limit=limit)  # Get them from DB
# Endpoint: Get a single activity log by its ID
@router.get("/{activity_id}", response_model=ActivityLog)
def read_activity(
    activity_id: UUID,                    # The ID of the activity we want
    db: Session = Depends(get_db)         # Database session
):
    db_activity = crud.get_activity(db, activity_id=activity_id)  # Look it up in DB
    if not db_activity:                   # If it doesn’t exist, return 404 error
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity                    # Otherwise, return the activity
# Endpoint: Update an existing activity log
@router.put("/{activity_id}", response_model=ActivityLog)
def update_activity(
    activity_id: UUID,                    # The ID of the activity to update
    activity: ActivityLogUpdate,          # The updated data
    db: Session = Depends(get_db)         # Database session
):
    updated_activity = crud.update_activity(db, activity_id=activity_id, updates=activity)
    if not updated_activity:               # If not found, return 404
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated_activity                 # Return the updated record
# Endpoint: Delete an activity log
@router.delete("/{activity_id}")
def delete_activity(
    activity_id: UUID,                     # The ID of the activity to delete
    db: Session = Depends(get_db)          # Database session
):
    deleted_activity = crud.delete_activity(db, activity_id=activity_id)
    if not deleted_activity:                # If it doesn't exist, return 404
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"ok": True}                     # Confirm it was deleted
