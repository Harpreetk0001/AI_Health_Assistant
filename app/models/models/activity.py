from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, Integer
from db.base import Base
import uuid

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    steps_count = Column(Integer, nullable=True)
    calories_burned = Column(Integer, nullable=True)
    logged_at = Column(DateTime, nullable=False)
