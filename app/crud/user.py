import uuid
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
def create_user(db: Session, user: UserCreate):
    db_user = User()  # To create an empty instance
    db_user.id = str(uuid.uuid4())
    db_user.full_name = user.full_name
    db_user.email = user.email
    db_user.hashed_password = user.hashed_password
    db_user.role = user.role
    db_user.language_preference = user.language_preference
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
def update_user(db: Session, db_user: User, user: UserUpdate):
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
