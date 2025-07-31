from sqlalchemy import Column, Enum, Boolean, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base import Base

class FallSeverityEnum(str, enum.Enum):
    low = "low"
    moderate = "moderate"
    severe = "severe"

class FallEvent(Base):
    __tablename__ = "fall_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity = Column(Enum(FallSeverityEnum), nullable=False)
    video_snapshot = Column(String, nullable=True)
    escalated = Column(Boolean, default=False)
