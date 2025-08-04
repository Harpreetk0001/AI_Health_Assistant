from app.models import ConversationLog
from app.db.session import db

def create_conversation_log(conversation_log):
    db.add(conversation_log)
    db.commit()
    db.refresh(conversation_log)
    return conversation_log

def get_conversation_log_by_id(conversation_log_id):
    return db.query(ConversationLog).filter(ConversationLog.id == conversation_log_id).first()
