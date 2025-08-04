from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base_class import Base

class Conversation(Base):
    __tablename__ = "conversation_logs"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    sender = Column(String, nullable=False)  # user or assistant
    timestamp = Column(DateTime, nullable=False)
