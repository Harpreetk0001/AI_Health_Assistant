from sqlalchemy.orm import Session
from models import user as models
from schemas import user as schemas
import uuid

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        id=str(uuid.uuid4()),
        full_name=user.full_name,
        email=user.email,
        hashed_password=user.hashed_password,
        role=user.role,
        language_preference=user.language_preference
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, db_user: models.User, user: schemas.UserUpdate):
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()
