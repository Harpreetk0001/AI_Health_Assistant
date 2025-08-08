from enum import Enum
class UserRole(str, Enum):
    ELDERLY = "elderly"
    CAREGIVER = "caregiver"
    ADMIN = "admin"
