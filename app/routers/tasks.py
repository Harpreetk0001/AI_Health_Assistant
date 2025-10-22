from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskIn, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.create_task(db, current_user.id, task)

@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.get_tasks(db, current_user.id)

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskIn, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    updated = crud.update_task(db, task_id, title=task.title, description=task.description, tag=task.tag, status=task.status, due_datetime=task.due_datetime)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ok = crud.delete_task(db, task_id)
    return {"success": ok}
