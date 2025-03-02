# src/utils/exceptions.py
from fastapi import HTTPException, status

class CustomAPIException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class CSVValidationError(CustomAPIException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ImageProcessingError(CustomAPIException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DatabaseError(CustomAPIException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)