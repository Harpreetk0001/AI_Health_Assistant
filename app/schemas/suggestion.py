from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
class SuggestionBase(BaseModel):
    user_id: UUID
    suggestion_text: str
class SuggestionCreate(SuggestionBase):
    pass
class SuggestionUpdate(BaseModel):
    suggestion_text: str
class SuggestionResponse(SuggestionBase):
    id: UUID
    created_at: datetime
    class Config:
        orm_mode = True
