from pydantic import BaseModel
from datetime import datetime

class ReminderLogBase(BaseModel):
    message: str
    remind_at: datetime
    completed: bool | None = False

class ReminderLogCreate(ReminderLogBase):
    user_id: str

class ReminderLogUpdate(BaseModel):
    message: str | None = None
    remind_at: datetime | None = None
    completed: bool | None = None

class ReminderLog(ReminderLogBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True

