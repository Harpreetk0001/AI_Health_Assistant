from pydantic import BaseModel
from typing import Any

class UIPreferenceBase(BaseModel):
    preferences: dict[str, Any]

class UIPreferenceCreate(UIPreferenceBase):
    user_id: str

class UIPreferenceUpdate(BaseModel):
    preferences: dict[str, Any] | None = None

class UIPreference(UIPreferenceBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True

