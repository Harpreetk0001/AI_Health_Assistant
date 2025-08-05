from sqlalchemy import Column, String, DateTime, UUID, ForeignKey
from db.base import Base
import uuid

class Medication(Base):
    __tablename__ = "medication"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    instructions = Column(String, nullable=True)
