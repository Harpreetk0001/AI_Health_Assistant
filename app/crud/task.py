from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskIn

def create_task(db: Session, user_id: int, task_in: TaskIn):
    t = Task(
        user_id=user_id,
        title=task_in.title,
        description=task_in.description,
        tag=task_in.tag,
        status=task_in.status,
        due_datetime=task_in.due_datetime
    )
    db.add(t); db.commit(); db.refresh(t)
    return t

def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

def update_task(db: Session, task_id: int, **kwargs):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        return None
    for k, v in kwargs.items():
        if hasattr(t, k):
            setattr(t, k, v)
    db.commit(); db.refresh(t)
    return t

def delete_task(db: Session, task_id: int):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t: return False
    db.delete(t); db.commit()
    return True
