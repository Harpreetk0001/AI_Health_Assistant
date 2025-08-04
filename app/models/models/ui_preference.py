from sqlalchemy import Column, String, ForeignKey, JSON
from app.db.base_class import Base

class UIPreference(Base):
    __tablename__ = "ui_preferences"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    preferences = Column(JSON, nullable=False)  # e.g., { "theme": "dark" }
