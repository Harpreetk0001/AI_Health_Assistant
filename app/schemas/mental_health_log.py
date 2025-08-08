from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
class MentalHealthLogBase(BaseModel):
    user_id: UUID
    mood: str
    notes: Optional[str]
    timestamp: datetime
class MentalHealthLogCreate(MentalHealthLogBase):
    pass
class MentalHealthLogUpdate(BaseModel):
    mood: Optional[str]
    notes: Optional[str]
    timestamp: Optional[datetime]
class MentalHealthLogResponse(MentalHealthLogBase):
    id: UUID
    recorded_at: datetime
    class Config:
        orm_mode = True
