from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class HealthBase(BaseModel):
    summary: Optional[str] = None
    notes: Optional[str] = None

class HealthCreate(HealthBase):
    user_id: UUID

class HealthUpdate(HealthBase):
    pass

class HealthRead(HealthBase):
    id: UUID
    user_id: UUID
    recorded_at: datetime

    class Config:
        orm_mode = True
