from pydantic import BaseModel
from datetime import datetime

class MentalHealthLogBase(BaseModel):
    mood: str | None = None
    note: str | None = None

class MentalHealthLogCreate(MentalHealthLogBase):
    user_id: str
    logged_at: datetime

class MentalHealthLogUpdate(BaseModel):
    mood: str | None = None
    note: str | None = None

class MentalHealthLog(MentalHealthLogBase):
    id: str
    user_id: str
    logged_at: datetime

    class Config:
        orm_mode = True

