# schemas/health.py

from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import List, Optional

class EmergencyContactBase(BaseModel):
    name: str
    phone: str

class EmergencyContactCreate(EmergencyContactBase):
    pass

class EmergencyContact(EmergencyContactBase):
    id: UUID

    class Config:
        orm_mode = True

class HealthRecordBase(BaseModel):
    name: str
    dob: date

class HealthRecordCreate(HealthRecordBase):
    emergency_contacts: Optional[List[EmergencyContactCreate]] = []

class HealthRecord(HealthRecordBase):
    id: UUID
    emergency_contacts: List[EmergencyContact] = []

    class Config:
        orm_mode = True
