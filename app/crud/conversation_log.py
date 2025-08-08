from sqlalchemy.orm import Session
from app.models.conversation_log import ConversationLog
from app.schemas.conversation_log import ConversationLogCreate, ConversationLogUpdate
def create_conversation(db: Session, convo: ConversationLogCreate):
    db_convo = ConversationLog(**convo.model_dump())
    db.add(db_convo)
    db.commit()
    db.refresh(db_convo)
    return db_convo
def get_conversations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ConversationLog).offset(skip).limit(limit).all()
def get_conversation(db: Session, convo_id: str):
    return db.query(ConversationLog).filter(ConversationLog.id == convo_id).first()
def update_conversation(db: Session, convo_id: str, updates: ConversationLogUpdate):
    db_convo = db.query(ConversationLog).filter(ConversationLog.id == convo_id).first()
    if db_convo:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_convo, field, value)
        db.commit()
        db.refresh(db_convo)
    return db_convo
def delete_conversation(db: Session, convo_id: str):
    db_convo = db.query(ConversationLog).filter(ConversationLog.id == convo_id).first()
    if db_convo:
        db.delete(db_convo)
        db.commit()
    return db_convo
