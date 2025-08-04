from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from app.db.base_class import Base

class HealthVital(Base):
    __tablename__ = "health_vitals"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    recorded_at = Column(DateTime, nullable=False)
    vital_type = Column(String, nullable=False)  # e.g., heart_rate
    value = Column(Float, nullable=False)
    unit = Column(String)
