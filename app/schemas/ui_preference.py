from pydantic import BaseModel
from uuid import UUID

class UIPreferenceBase(BaseModel):
    user_id: UUID
    theme: str
    font_size: str
    language: str

class UIPreferenceCreate(UIPreferenceBase):
    pass

class UIPreferenceUpdate(BaseModel):
    theme: str
    font_size: str
    language: str

class UIPreferenceResponse(UIPreferenceBase):
    id: UUID

    class Config:
        orm_mode = True
