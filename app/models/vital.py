from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Vitals(Base):
    __tablename__ = "vitals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hydration = Column(Float)
    sleep = Column(Float)
    heartbeat = Column(Float)
    bp_systolic = Column(Float)
    bp_diastolic = Column(Float)
    steps = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
