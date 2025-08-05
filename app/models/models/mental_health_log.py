from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, Integer
from db.base import Base
import uuid

class MentalHealthLog(Base):
    __tablename__ = "mental_health_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    mood = Column(String, nullable=False)
    anxiety_level = Column(Integer, nullable=True)
    stress_level = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    logged_at = Column(DateTime, nullable=False)
