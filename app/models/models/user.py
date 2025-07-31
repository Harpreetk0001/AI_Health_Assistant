from sqlalchemy import Column, String, Enum as SqlEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from enum import Enum
from app.db.base_class import Base

class UserRole(str, Enum):
    elderly = "elderly"
    caregiver = "caregiver"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False)
    language_preference = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
