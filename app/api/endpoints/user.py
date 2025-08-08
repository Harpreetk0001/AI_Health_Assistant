from fastapi import APIRouter, HTTPException, Depends  # Import FastAPI router, exceptions, and dependency injection
from sqlalchemy.orm import Session                     # Import database session management from SQLAlchemy
from typing import List                                # Import typing List for response models
from app.db.database import get_db                      # Function to get a DB session (dependency)
from app.schemas.user import UserCreate, UserUpdate, UserRead  # User data models for validation and response
from app.crud.user import (                             # Import user CRUD functions
    create_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user,
    delete_user,
)
import bcrypt                                          # Import bcrypt library for password hashing

# Create a router for all user-related API routes, prefix all with /users and tag them as "Users"
router = APIRouter(prefix="/users", tags=["Users"])

# Define POST endpoint to create a new user, returning the created user data
@router.post("/", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user with this email already exists in the database
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        # If email is taken, raise HTTP 400 error with a message
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the user’s password securely before saving it
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create a new user object with all info including hashed password
    user_data = UserCreate(
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        language_preference=user.language_preference,
        password=hashed_password
    )

    # Call the CRUD function to add this new user to the database and return the created user
    return create_user(db=db, user=user_data)

# Define GET endpoint to retrieve a list of users with pagination support
@router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Get users from the database, skipping and limiting results as requested
    return get_users(db, skip=skip, limit=limit)

# Define GET endpoint to retrieve a single user by their user_id
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: str, db: Session = Depends(get_db)):
    # Fetch user from DB by id
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        # If user not found, raise 404 error with message
        raise HTTPException(status_code=404, detail="User not found !!")
    return db_user

# Define PUT endpoint to update a user’s information by user_id
@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    # First, check if the user exists
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        # If not found, raise 404 error
        raise HTTPException(status_code=404, detail="User not found !!")
    # Update user with new data and return updated user info
    return update_user(db=db, db_user=db_user, user=user)

# Define DELETE endpoint to remove a user by user_id
@router.delete("/{user_id}")
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found !!")
    delete_user(db=db, db_user=db_user)
    return {"User deleted successfully !!"}
