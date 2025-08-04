from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base_class import Base

class Activity(Base):
    __tablename__ = "activity_logs"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    activity_type = Column(String, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, nullable=False)
