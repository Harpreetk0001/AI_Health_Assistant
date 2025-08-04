from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base_class import Base

class FallEvent(Base):
    __tablename__ = "fall_events"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    detected_at = Column(DateTime, nullable=False)
    severity = Column(String)
    location = Column(String)
