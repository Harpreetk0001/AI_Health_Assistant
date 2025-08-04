from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base_class import Base

class Medication(Base):
    __tablename__ = "medications"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    dosage = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
