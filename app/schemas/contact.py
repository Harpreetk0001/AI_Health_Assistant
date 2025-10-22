from pydantic import BaseModel
from typing import Optional

class ContactIn(BaseModel):
    name: str
    relationship: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    profile: Optional[str] = None
    favourite: Optional[bool] = False

class ContactOut(ContactIn):
    id: int
    user_id: int
    class Config:
        orm_mode = True
