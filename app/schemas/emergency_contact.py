from pydantic import BaseModel

class EmergencyContactBase(BaseModel):
    name: str
    phone: str
    relationship: str | None = None

class EmergencyContactCreate(EmergencyContactBase):
    user_id: str

class EmergencyContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    relationship: str | None = None

class EmergencyContact(EmergencyContactBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True

