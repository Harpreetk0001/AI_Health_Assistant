from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
class FallEventBase(BaseModel):
    location: Optional[str] = None
    severity: Optional[str] = None
    sensor_data: Optional[str] = None
class FallEventCreate(FallEventBase):
    user_id: UUID
class FallEventUpdate(FallEventBase):
    pass
class FallEventRead(FallEventBase):
    id: UUID
    user_id: UUID
    detected_at: datetime
    class Config:
        orm_mode = True
