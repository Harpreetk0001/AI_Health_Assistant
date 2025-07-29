# models/health.py

from sqlalchemy import Column, String, Date, UUID, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.base import Base

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)

    # One health record has many emergency contacts
    emergency_contacts = relationship("EmergencyContact", back_populates="health_record")
