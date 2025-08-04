from sqlalchemy import Column, String, DateTime, Enum
from app.db.base_class import Base
import enum

class UserRole(enum.Enum):
    elderly = "elderly"
    caregiver = "caregiver"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.elderly, nullable=False)
    language_preference = Column(String)
    created_at = Column(DateTime, nullable=False)
