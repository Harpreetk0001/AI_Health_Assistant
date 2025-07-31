from sqlalchemy import Column, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base import Base

class HealthVitals(Base):
    __tablename__ = "health_vitals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    heart_rate = Column(Float)
    bp_systolic = Column(Float)
    bp_diastolic = Column(Float)
    temperature = Column(Float)
    spo2 = Column(Float)
    fall_detected = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
