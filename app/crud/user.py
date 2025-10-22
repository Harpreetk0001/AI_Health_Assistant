from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, email: str, hashed_password: str):
    u = User(email=email, hashed_password=hashed_password)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
