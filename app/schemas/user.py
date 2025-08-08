from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str  # role as elderly, caregiver, admin
    language_preference: Optional[str] = None
class UserCreate(UserBase):
    password: str
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    language_preference: Optional[str] = None
class UserRead(UserBase):
    id: UUID
    created_at: datetime
    class Config:
        orm_mode = True
