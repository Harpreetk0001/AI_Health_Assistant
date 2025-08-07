from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ActivityLogBase(BaseModel):
    user_id: UUID
    activity_type: str
    duration_minutes: Optional[int] = None
    steps_count: Optional[int] = None
    calories_burned: Optional[int] = None
    logged_at: datetime

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogUpdate(BaseModel):
    activity_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    steps_count: Optional[int] = None
    calories_burned: Optional[int] = None
    logged_at: Optional[datetime] = None

class ActivityLog(ActivityLogBase):
    id: UUID

    class Config:
        orm_mode = True
