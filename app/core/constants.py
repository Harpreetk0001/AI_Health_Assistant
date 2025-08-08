from enum import Enum # Import Enum class to create a list of named constant values
class UserRole(str, Enum): # Define user roles in the system as a set of fixed options
    ELDERLY = "elderly"
    CAREGIVER = "caregiver"
    ADMIN = "admin"
