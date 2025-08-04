from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.db.base_class import Base

class MentalHealthLog(Base):
    __tablename__ = "mental_health_logs"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    mood = Column(String)
    note = Column(Text)
    logged_at = Column(DateTime, nullable=False)
