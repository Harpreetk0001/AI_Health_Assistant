from typing import List
from datetime import datetime

class TaskObject:
    def __init__(self, dueDateTime: datetime, title: str, description: str = "", tag: str = "Exercise", status: str = "Incomplete"):
        self.dueDateTime = dueDateTime
        self.title = title
        self.description = description
        self.tag = tag
        self.status = status

class ToDoList:
    def __init__(self):
        self.tasks: List[TaskObject] = []

    def addTask(self, task: TaskObject):
        self.tasks.append(task)
        # TODO: persist to backend (call crud.create_task)

    def removeTask(self, task: TaskObject):
        if task in self.tasks:
            self.tasks.remove(task)
            # TODO: delete from backend

    def updateTask(self, task: TaskObject, attribute: str, new_value):
        if task in self.tasks:
            setattr(task, attribute, new_value)
            # TODO: update backend

    def displayAll(self):
        return self.tasks

    def displayIncomplete(self):
        return [t for t in self.tasks if t.status == "Incomplete"]

    def displayComplete(self):
        return [t for t in self.tasks if t.status == "Complete"]

    def displayByTag(self, selectedTag: str):
        return [t for t in self.tasks if t.tag == selectedTag]
