import json
import numpy as np
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class ToDoList:
    def __init__(self, tasks = [], complete = [], incomplete = []):
        self.tasks = tasks
        self.complete = complete
        self.incomplete = incomplete

    def addTask(self, Task):
        self.checkTaskStatus(Task)
        self.tasks.append(Task)

        #add to DB

    def removeTask(self, Task):
        for t in self.tasks:
            if Task in self.tasks:
                self.tasks.remove(Task)
                #remove from DB
            
            if Task in self.complete:
                self.complete.remove(Task)
            if Task in self.incomplete:
                self.incomplete.remove(Task)

    def updateTask(self, Task, attribute, new_value):
        if attribute == "title":
            Task.title = new_value
        elif attribute == "description":
            Task.description = new_value
        elif attribute == "dueDateTime":
            new_time = datetime.strptime(new_value, "%Y-%m-%d %H:%M")
            Task.dueDateTime = new_time.strftime("%I:%M %p, %d %B %Y").lstrip("0").replace(" 0", " ")
        elif attribute == "tag":
            Task.tag = new_value
        elif attribute == "status":
            Task.status = new_value
            self.checkTaskStatus(Task)
            
        #update the task with all attributes in the backend

    def checkTaskStatus(self, Task):
        if Task.status == "Complete":
            self.complete.append(Task)
            if Task in self.incomplete:
                self.incomplete.remove(Task)
            
        elif Task.status == "Incomplete":
            self.incomplete.append(Task)
            if Task in self.complete:
                self.complete.remove(Task)

    def displayList(self):
        print("TO DO LIST\n")
        for e in self.tasks:
            Task.getTask(e)
            print()

    def displayCompleteList(self):
        print("COMPLETE LIST\n")
        for c in self.complete:
            Task.getTask(c)
            print()

    def displayIncompleteList(self):
        print("INCOMPLETE LIST\n")
        for i in self.incomplete:
            Task.getTask(i)
            print()

    def displayByTag(self, selectedTag):
        #print("FILTERED LIST\n")

        filteredList = []
        
        for f in self.tasks:
            if f.tag == selectedTag:
                filteredList.append(f)
                #Task.getTask(f)

        return filteredList
        
class Task:
    def __init__(self, dueDateTime, title, description, tag, status): #if needed add index=None
        time = datetime.strptime(dueDateTime, "%Y-%m-%d %H:%M")
        self.dueDateTime = time.strftime("%I:%M %p, %d %B %Y").lstrip("0").replace(" 0", " ")
        self.title = title
        self.description = description
        self.tag = tag
        self.status = status

        #if needed, add an index attribute

    def getTask(self):
        
        task_str = f"Task name: {self.title} \nDescription: {self.description} \nTag: {self.tag} \nDue date and time: {self.dueDateTime} \nStatus: {self.status}"

        #print(task_str)

        return task_str
            

##TESTING##

TDL = ToDoList()

#load data into TDL

#task 1#
t1 = Task("2025-03-04 12:00", "BP Tablet", "must have with a glass of water", "Medication", "Incomplete")
TDL.addTask(t1)

#task 2#
t2 = Task("2025-03-04 09:00", "Walk", "meet Mary-Anne at the park", "Exercise", "Complete")
TDL.addTask(t2)

#task 3#
t3 = Task("2025-03-04 16:00", "Nap", "with whale sounds", "Sleep", "Incomplete")
TDL.addTask(t3)

#display to do list
TDL.displayList()
TDL.displayCompleteList()
TDL.displayIncompleteList()

#update task
TDL.updateTask(t1, "dueDateTime", "2025-03-04 11:00")
TDL.updateTask(t3, "status", "Complete")

#display modified lists with removed items
TDL.displayList()
TDL.displayCompleteList()
TDL.displayIncompleteList()

#display modified lists with removed items
TDL.displayList()
TDL.displayCompleteList()
TDL.displayIncompleteList()
