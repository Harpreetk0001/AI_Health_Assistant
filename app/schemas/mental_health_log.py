from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MentalHealthLogBase(BaseModel):
    user_id: UUID
    mood: str
    notes: str

class MentalHealthLogCreate(MentalHealthLogBase):
    pass

class MentalHealthLogUpdate(BaseModel):
    mood: str
    notes: str

class MentalHealthLogResponse(MentalHealthLogBase):
    id: UUID
    recorded_at: datetime

    class Config:
        orm_mode = True
