from datetime import datetime

from pydantic import BaseModel


class HealthBase(BaseModel):
    user_id: str
    blood_pressure: str
    heartbeat: int
    hydration: float
    sleep_hours: float
    steps: int

class HealthCreate(HealthBase):
    pass

class HealthRead(HealthBase):
    id: int
    recorded_at: datetime

    class Config:
        orm_mode = True
