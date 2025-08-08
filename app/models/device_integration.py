from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
import uuid
class DeviceIntegration(Base):
    __tablename__ = "device_integrations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    integration_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)