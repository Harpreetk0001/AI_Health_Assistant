from pydantic import BaseModel
from datetime import datetime

class FallEventBase(BaseModel):
    severity: str | None = None
    location: str | None = None

class FallEventCreate(FallEventBase):
    user_id: str
    detected_at: datetime

class FallEventUpdate(BaseModel):
    severity: str | None = None
    location: str | None = None

class FallEvent(FallEventBase):
    id: str
    user_id: str
    detected_at: datetime

    class Config:
        orm_mode = True
