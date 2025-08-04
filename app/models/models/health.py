from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base_class import Base

class Health(Base):
    __tablename__ = "health_records"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    record_date = Column(DateTime, nullable=False)
    summary = Column(String)
