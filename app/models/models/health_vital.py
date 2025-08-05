from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from db.base import Base

class HealthVital(Base):
    __tablename__ = "health_vitals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    blood_pressure = Column(String, nullable=True)
    heart_rate = Column(Float, nullable=True)
    hydration_level = Column(Float, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    steps = Column(Float, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
