from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from app.db.base_class import Base

class ReminderLog(Base):
    __tablename__ = "reminder_logs"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)
