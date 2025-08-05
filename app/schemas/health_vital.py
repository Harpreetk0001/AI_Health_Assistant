from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class HealthVitalBase(BaseModel):
    blood_pressure: Optional[str] = None
    heart_rate: Optional[float] = None
    hydration_level: Optional[float] = None
    sleep_hours: Optional[float] = None
    steps: Optional[float] = None

class HealthVitalCreate(HealthVitalBase):
    user_id: UUID

class HealthVitalUpdate(HealthVitalBase):
    pass

class HealthVitalRead(HealthVitalBase):
    id: UUID
    user_id: UUID
    recorded_at: datetime

    class Config:
        orm_mode = True
