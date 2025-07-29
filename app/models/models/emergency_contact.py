# models/emergency_contact.py

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.base import Base

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    health_record_id = Column(UUID(as_uuid=True), ForeignKey("health_records.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # Link back to health record
    health_record = relationship("HealthRecord", back_populates="emergency_contacts")
