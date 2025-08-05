from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, Boolean
from db.base import Base
import uuid

class ReminderLog(Base):
    __tablename__ = "reminder_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reminder_type = Column(String, nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    acknowledged = Column(Boolean, default=False)
    notes = Column(String, nullable=True)
