from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    elderly = "elderly"
    caregiver = "caregiver"
    admin = "admin"

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole
    language_preference: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    language_preference: str | None = None

class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

