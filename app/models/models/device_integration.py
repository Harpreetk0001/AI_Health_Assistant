from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from app.db.base_class import Base

class DeviceIntegration(Base):
    __tablename__ = "device_integrations"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    device_name = Column(String, nullable=False)
    device_type = Column(String)
    connected_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
