from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MedicationBase(BaseModel):
    user_id: UUID
    name: str
    dosage: str
    frequency: str

class MedicationCreate(MedicationBase):
    start_date: datetime
    end_date: datetime

class MedicationUpdate(BaseModel):
    name: str
    dosage: str
    frequency: str
    start_date: datetime
    end_date: datetime

class MedicationResponse(MedicationBase):
    id: UUID
    start_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True
