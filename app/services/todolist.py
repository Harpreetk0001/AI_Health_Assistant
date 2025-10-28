from typing import List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session

# Defensive imports
try:
    from app import crud
    from app import models
except Exception:
    crud = None
    models = None


class TaskObject:
    def __init__(self, dueDateTime: datetime, title: str, description: str = "", tag: str = "Exercise", status: str = "Incomplete", id: Optional[int] = None):
        self.dueDateTime = dueDateTime
        self.title = title
        self.description = description
        self.tag = tag
        self.status = status
        self.id = id

    def as_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "tag": self.tag,
            "status": self.status,
            "due_datetime": self.dueDateTime
        }


class ToDoList:
    def __init__(self, user_id: Optional[int] = None):
        self.tasks: List[TaskObject] = []
        self.user_id = user_id

    def addTask(self, db: Optional[Session], task: TaskObject) -> Optional[Any]:
        """
        Adds task to in-memory list and persists to DB if db session provided.
        Returns DB record (or None).
        """
        self.tasks.append(task)
        db_record = None
        if db is not None:
            try:
                if crud and hasattr(crud, "create_task"):
                    db_record = crud.create_task(db, self.user_id, type("X",(object,),{"title":task.title,"description":task.description,"tag":task.tag,"status":task.status,"due_datetime":task.dueDateTime})())
                elif models and hasattr(models, "Task"):
                    t = models.Task(
                        user_id=self.user_id,
                        title=task.title,
                        description=task.description,
                        tag=task.tag,
                        status=task.status,
                        due_datetime=task.dueDateTime
                    )
                    db.add(t); db.commit(); db.refresh(t)
                    db_record = t
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass
                db_record = None

            # store DB id in in-memory object if available
            if db_record and hasattr(db_record, "id"):
                task.id = getattr(db_record, "id")
        return db_record

    def removeTask(self, db: Optional[Session], task: TaskObject) -> bool:
        """Remove from memory and DB (if db)"""
        if task in self.tasks:
            self.tasks.remove(task)
        ok = True
        if db is not None and task.id:
            try:
                if crud and hasattr(crud, "delete_task"):
                    ok = crud.delete_task(db, task.id)
                elif models and hasattr(models, "Task"):
                    rec = db.query(models.Task).filter(models.Task.id == task.id).first()
                    if rec:
                        db.delete(rec); db.commit()
                        ok = True
                    else:
                        ok = False
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass
                ok = False
        return ok

    def updateTask(self, db: Optional[Session], task: TaskObject, attribute: str, new_value) -> Optional[Any]:
        """Update in-memory object and persist change"""
        if task not in self.tasks:
            return None
        setattr(task, attribute, new_value)
        db_record = None
        if db is not None and task.id:
            try:
                if crud and hasattr(crud, "update_task"):
                    db_record = crud.update_task(db, task.id, **{attribute: new_value})
                elif models and hasattr(models, "Task"):
                    rec = db.query(models.Task).filter(models.Task.id == task.id).first()
                    if rec:
                        setattr(rec, attribute, new_value)
                        db.commit(); db.refresh(rec)
                        db_record = rec
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass
                db_record = None
        return db_record

    def displayAll(self) -> List[TaskObject]:
        return list(self.tasks)

    def displayIncomplete(self) -> List[TaskObject]:
        return [t for t in self.tasks if t.status == "Incomplete"]

    def displayComplete(self) -> List[TaskObject]:
        return [t for t in self.tasks if t.status == "Complete"]

    def displayByTag(self, selectedTag: str) -> List[TaskObject]:
        return [t for t in self.tasks if t.tag == selectedTag]
