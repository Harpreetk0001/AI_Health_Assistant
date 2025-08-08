from .config import settings # Import the app settings like database URL and secret keys
# Import security functions for password handling and token management
from .security import (
    verify_password,      # Check if a plain password matches the hashed one
    get_password_hash,    # Convert a password into a secure hashed version
    create_access_token,  # Make a new token for user authentication
    decode_access_token,  # Read and verify the token to get user info
)
from .constants import UserRole # Import user roles like admin, caregiver, or elderly
from .logging import logger # Import the logger to print messages and keep track of app events
from .utils import generate_uuid # Import a helper function to create unique IDs
