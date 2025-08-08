from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime, timezone
from app.db.base_class import Base
class FallEvent(Base):
    __tablename__ = "fall_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    location = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    sensor_data = Column(String, nullable=True)