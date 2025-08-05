from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ActivityLogBase(BaseModel):
    user_id: UUID
    activity: str

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogUpdate(BaseModel):
    activity: str

class ActivityLogResponse(ActivityLogBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
