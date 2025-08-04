from pydantic import BaseModel
from datetime import datetime

class HealthVitalBase(BaseModel):
    vital_type: str
    value: float
    unit: str | None = None

class HealthVitalCreate(HealthVitalBase):
    user_id: str
    recorded_at: datetime

class HealthVitalUpdate(BaseModel):
    vital_type: str | None = None
    value: float | None = None
    unit: str | None = None

class HealthVital(HealthVitalBase):
    id: str
    user_id: str
    recorded_at: datetime

    class Config:
        orm_mode = True

