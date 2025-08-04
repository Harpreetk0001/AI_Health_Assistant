from sqlalchemy import Column, String, ForeignKey
from app.db.base_class import Base

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    relationship = Column(String)
