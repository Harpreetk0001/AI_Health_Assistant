from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
import crud.conversation as crud
import schemas.conversation as schemas

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/", response_model=schemas.Conversation)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    return crud.create_conversation(db=db, conversation=conversation)

@router.get("/", response_model=list[schemas.Conversation])
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_conversations(db=db, skip=skip, limit=limit)

@router.get("/{conversation_id}", response_model=schemas.Conversation)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = crud.get_conversation(db, conversation_id=conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.put("/{conversation_id}", response_model=schemas.Conversation)
def update_conversation(conversation_id: int, conversation: schemas.ConversationUpdate, db: Session = Depends(get_db)):
    return crud.update_conversation(db, conversation_id=conversation_id, conversation=conversation)

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    crud.delete_conversation(db, conversation_id=conversation_id)
    return {"ok": True}
