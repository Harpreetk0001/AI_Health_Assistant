from pydantic import BaseModel
from typing import Optional
import datetime

class VitalsIn(BaseModel):
    hydration: Optional[float] = None
    sleep: Optional[float] = None
    heartbeat: Optional[float] = None
    bp_systolic: Optional[float] = None
    bp_diastolic: Optional[float] = None
    steps: Optional[int] = None
    timestamp: Optional[datetime.datetime] = None

class VitalsOut(VitalsIn):
    id: int
    user_id: int
    class Config:
        orm_mode = True
