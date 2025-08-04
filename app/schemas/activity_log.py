from pydantic import BaseModel
from datetime import datetime

class ActivityBase(BaseModel):
    activity_type: str
    description: str | None = None

class ActivityCreate(ActivityBase):
    user_id: str

class ActivityUpdate(BaseModel):
    activity_type: str | None = None
    description: str | None = None

class Activity(ActivityBase):
    id: str
    user_id: str
    timestamp: datetime

    class Config:
        orm_mode = True
