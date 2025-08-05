from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from db.base import Base

class Health(Base):
    __tablename__ = "health"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    summary = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
