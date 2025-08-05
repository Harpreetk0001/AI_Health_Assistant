from sqlalchemy import Column, String, UUID, ForeignKey, Boolean, DateTime
from db.base import Base
import uuid

class UIPreference(Base):
    __tablename__ = "ui_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    theme = Column(String, nullable=True)  # e.g., "dark", "light"
    language = Column(String, nullable=True)
    font_size = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=False)
