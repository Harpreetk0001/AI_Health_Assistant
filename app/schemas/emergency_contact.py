from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class EmergencyContactBase(BaseModel):
    name: str
    relationship: Optional[str] = None
    phone_number: str
    email: Optional[EmailStr] = None

class EmergencyContactCreate(EmergencyContactBase):
    user_id: UUID

class EmergencyContactUpdate(EmergencyContactBase):
    pass

class EmergencyContactRead(EmergencyContactBase):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True
