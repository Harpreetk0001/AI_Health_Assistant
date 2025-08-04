from pydantic import BaseModel
from datetime import datetime

class SuggestionBase(BaseModel):
    suggestion_text: str

class SuggestionCreate(SuggestionBase):
    user_id: str
    created_at: datetime

class SuggestionUpdate(BaseModel):
    suggestion_text: str | None = None

class Suggestion(SuggestionBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

