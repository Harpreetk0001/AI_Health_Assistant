from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.crud.user import (
    create_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user,
    delete_user,
)
import bcrypt
router = APIRouter(prefix="/users", tags=["Users"])
@router.post("/", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
# Hash password before passing to create_user
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
# To create a new UserCreate-like dict with hashed password
    user_data = UserCreate(
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        language_preference=user.language_preference,
        password=hashed_password
    )
    return create_user(db=db, user=user_data)
@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found !!")
    return db_user
@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found !!")
    return update_user(db=db, db_user=db_user, user=user)
@router.delete("/{user_id}")
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found !!")
    delete_user(db=db, db_user=db_user)
    return {"User deleted successfully !!"}
