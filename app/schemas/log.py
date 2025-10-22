from pydantic import BaseModel
from typing import Optional
import datetime

class LogOut(BaseModel):
    id: int
    user_id: Optional[int]
    action: Optional[str]
    timestamp: Optional[datetime.datetime]
    class Config:
        orm_mode = True
