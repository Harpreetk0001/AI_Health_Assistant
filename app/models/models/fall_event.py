from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from db.base import Base

class FallEvent(Base):
    __tablename__ = "fall_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow)
    location = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    sensor_data = Column(String, nullable=True)
