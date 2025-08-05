from sqlalchemy.orm import Session
from models import conversation as models
from schemas import conversation as schemas

def create_conversation(db: Session, convo: schemas.ConversationCreate):
    db_convo = models.Conversation(**convo.dict())
    db.add(db_convo)
    db.commit()
    db.refresh(db_convo)
    return db_convo

def get_conversations(db: Session, skip=0, limit=100):
    return db.query(models.Conversation).offset(skip).limit(limit).all()

def get_conversation(db: Session, convo_id: str):
    return db.query(models.Conversation).filter(models.Conversation.id == convo_id).first()

def update_conversation(db: Session, convo_id: str, updates: schemas.ConversationUpdate):
    db_convo = db.query(models.Conversation).filter(models.Conversation.id == convo_id).first()
    if db_convo:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_convo, field, value)
        db.commit()
        db.refresh(db_convo)
    return db_convo

def delete_conversation(db: Session, convo_id: str):
    db_convo = db.query(models.Conversation).filter(models.Conversation.id == convo_id).first()
    if db_convo:
        db.delete(db_convo)
        db.commit()
    return db_convo

