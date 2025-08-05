from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ConversationLogBase(BaseModel):
    user_id: UUID
    content: str

class ConversationLogCreate(ConversationLogBase):
    pass

class ConversationLogUpdate(BaseModel):
    content: str

class ConversationLogResponse(ConversationLogBase):
    id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True
