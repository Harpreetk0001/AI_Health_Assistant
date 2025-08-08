from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.session import get_db
from app.crud import conversation_log as crud
from app.schemas import conversation_log as schemas
router = APIRouter(prefix="/conversations", tags=["Conversations"])
@router.post("/", response_model=schemas.ConversationLogBase)
def create_conversation(
    conversation: schemas.ConversationLogCreate,
    db: Session = Depends(get_db)
):
    return crud.create_conversation(db=db, convo=conversation)
@router.get("/", response_model=List[schemas.ConversationLogBase])
def read_conversations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_conversations(db=db, skip=skip, limit=limit)
@router.get("/{conversation_id}", response_model=schemas.ConversationLogBase)
def read_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    db_conversation = crud.get_conversation(db, convo_id=str(conversation_id))  # To convert UUID to str
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation
@router.put("/{conversation_id}", response_model=schemas.ConversationLogBase)
def update_conversation(
    conversation_id: UUID,
    conversation: schemas.ConversationLogUpdate,
    db: Session = Depends(get_db)
):
    updated_convo = crud.update_conversation(db, convo_id=str(conversation_id), updates=conversation)  # To convert UUID to str
    if not updated_convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return updated_convo
@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    deleted_convo = crud.delete_conversation(db, convo_id=str(conversation_id))  # To convert UUID to str
    if not deleted_convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"ok": True}
