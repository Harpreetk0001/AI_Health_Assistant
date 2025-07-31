import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Enum as PgEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserRole(Enum):
    elderly = "elderly"
    caregiver = "caregiver"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(PgEnum(UserRole), nullable=False)
    language_preference = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    preferences = relationship("UIPreference", back_populates="user", uselist=False)

class UIPreference(Base):
    __tablename__ = "ui_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    font_size = Column(String)
    contrast_mode = Column(Boolean, default=False)
    voice_control = Column(Boolean, default=False)

    user = relationship("User", back_populates="preferences")

