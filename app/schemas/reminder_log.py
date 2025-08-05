from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ReminderLogBase(BaseModel):
    user_id: UUID
    reminder: str
    status: str

class ReminderLogCreate(ReminderLogBase):
    due_at: datetime

class ReminderLogUpdate(BaseModel):
    reminder: str
    status: str
    due_at: datetime

class ReminderLogResponse(ReminderLogBase):
    id: UUID
    due_at: datetime
    sent_at: datetime

    class Config:
        orm_mode = True
