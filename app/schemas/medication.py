from pydantic import BaseModel
from datetime import datetime

class MedicationBase(BaseModel):
    name: str
    dosage: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

class MedicationCreate(MedicationBase):
    user_id: str

class MedicationUpdate(BaseModel):
    name: str | None = None
    dosage: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

class Medication(MedicationBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True

