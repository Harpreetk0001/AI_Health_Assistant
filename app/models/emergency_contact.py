from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base
class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    relationship = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)