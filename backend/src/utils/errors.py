from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    details: Optional[str] = None


class TodoException(Exception):
    """Base exception for todo-related errors."""
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class SessionNotFoundException(TodoException):
    """Raised when a session is not found."""
    pass


class TodoNotFoundException(TodoException):
    """Raised when a todo is not found."""
    pass


class ValidationError(TodoException):
    """Raised when validation fails."""
    pass


def handle_exception(exception: Exception, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """Convert exceptions to HTTP responses."""
    if isinstance(exception, TodoException):
        return HTTPException(
            status_code=status_code,
            detail={
                "error": exception.__class__.__name__,
                "message": exception.message,
                "details": exception.details
            }
        )
    elif isinstance(exception, HTTPException):
        return exception
    else:
        return HTTPException(
            status_code=status_code,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "details": str(exception) if hasattr(exception, '__str__') else "Unknown error"
            }
        )