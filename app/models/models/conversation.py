from sqlalchemy import Column, DateTime, Text, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base import Base

class ConversationLog(Base):
    __tablename__ = "conversation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    language = Column(String, nullable=True)
