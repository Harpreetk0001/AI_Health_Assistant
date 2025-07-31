from sqlalchemy import Column, String, Time, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class MedicationSchedule(Base):
    __tablename__ = "medication_schedule"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    medication_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    time_of_day = Column(Time, nullable=False)
    active = Column(Boolean, default=True)
