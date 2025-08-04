from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.db.base_class import Base

class Suggestion(Base):
    __tablename__ = "suggestions"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    suggestion_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
