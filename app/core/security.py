from passlib.context import CryptContext # Import CryptContext to handle password hashing securely
from datetime import datetime, timedelta, timezone # Import datetime tools to handle token expiry times
from jose import JWTError, jwt # Import tools to create and verify JWT tokens
from typing import Optional # Import Optional for typing when a value can be None
from .config import settings # Import app settings like SECRET_KEY from your config file
# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # Encode the token with secret key and chosen algorithm
    return encoded_jwt
def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload # Return the decoded token data if successful
    except JWTError:
        return None # Return None if token is invalid or expired
