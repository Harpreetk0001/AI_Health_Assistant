from fastapi import HTTPException, status # Import HTTPException and status codes from FastAPI
class NotFoundException(HTTPException): # Define a custom error for "Not Found" situations
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
class UnauthorizedException(HTTPException): # Define a custom error for "Unauthorized" access
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
class BadRequestException(HTTPException): # Define a custom error for "Bad Request" errors
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
