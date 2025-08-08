from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
class MedicationBase(BaseModel):
    name: str
    dosage: str
    start_date: datetime
    end_date: Optional[datetime] = None
    instructions: Optional[str] = None
class MedicationCreate(MedicationBase):
    pass
class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    instructions: Optional[str] = None
class Medication(MedicationBase):
    id: UUID
    user_id: UUID
    class Config:
        orm_mode = True
