from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.base import Base

class HealthData(Base):
    __tablename__ = "health_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    blood_pressure = Column(String)
    heartbeat = Column(Integer)
    hydration = Column(Float)
    sleep_hours = Column(Float)
    steps = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.UTCnow)

