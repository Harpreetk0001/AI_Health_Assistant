from pydantic import BaseModel
from datetime import datetime

class ConversationBase(BaseModel):
    message: str
    sender: str

class ConversationCreate(ConversationBase):
    user_id: str

class ConversationUpdate(BaseModel):
    message: str | None = None
    sender: str | None = None

class Conversation(ConversationBase):
    id: str
    user_id: str
    timestamp: datetime

    class Config:
        orm_mode = True
