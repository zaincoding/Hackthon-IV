from datetime import datetime
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator
from passlib.context import CryptContext
import re


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """User model representing a registered user."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    hashed_password: str
    is_active: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_ -]+$', v):
            raise ValueError('Username must contain only letters, numbers, underscores, hyphens, or spaces')
        return v.strip()  # Return stripped value to handle any accidental trailing spaces

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Invalid email format')
        return v


class UserCreateRequest(BaseModel):
    """Request model for creating a new user."""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=6)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_ -]+$', v):
            raise ValueError('Username must contain only letters, numbers, underscores, hyphens, or spaces')
        return v.strip()  # Return stripped value to handle any accidental trailing spaces

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Invalid email format')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserLoginRequest(BaseModel):
    """Request model for user login."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """Response model for user data (without sensitive information)."""

    id: str
    username: str
    email: str
    is_active: bool
    created_at: str
    updated_at: str


class Token(BaseModel):
    """Token model for authentication."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data model containing user information."""

    username: Optional[str] = None