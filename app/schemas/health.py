from pydantic import BaseModel
from datetime import datetime

class HealthBase(BaseModel):
    summary: str | None = None

class HealthCreate(HealthBase):
    user_id: str
    record_date: datetime

class HealthUpdate(BaseModel):
    summary: str | None = None

class Health(HealthBase):
    id: str
    user_id: str
    record_date: datetime

    class Config:
        orm_mode = True
