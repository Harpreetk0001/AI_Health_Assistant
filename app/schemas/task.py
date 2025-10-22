from pydantic import BaseModel, Field
from typing import Optional
import datetime

class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    tag: Optional[str] = Field(None, regex="^(Exercise|Hydration|Sleep|Medication)$")
    status: Optional[str] = Field("Incomplete", regex="^(Complete|Incomplete)$")
    due_datetime: Optional[datetime.datetime] = None

class TaskOut(TaskIn):
    id: int
    user_id: int
    class Config:
        orm_mode = True
