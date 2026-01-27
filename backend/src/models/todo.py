from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field, validator


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Todo(BaseModel):
    """Todo model representing a single todo item."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    due_date: Optional[str] = None  # ISO 8601 format
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = Field(None, max_length=50)
    status: Status = Status.PENDING
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    @validator('due_date')
    def validate_due_date(cls, v):
        if v:
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Due date must be in ISO 8601 format')
        return v

    @validator('completed_at')
    def validate_completed_at(cls, v, values):
        if v and values.get('status') != Status.COMPLETED:
            raise ValueError('completed_at can only be set when status is completed')
        if v:
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Completed at must be in ISO 8601 format')
        return v

    def mark_completed(self):
        """Mark the todo as completed and update timestamps."""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now().isoformat()


class TodoCreateRequest(BaseModel):
    """Request model for creating a new todo."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[Priority] = Priority.MEDIUM
    category: Optional[str] = Field(None, max_length=50)


class TodoUpdateRequest(BaseModel):
    """Request model for updating an existing todo."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[Priority] = None
    category: Optional[str] = Field(None, max_length=50)
    status: Optional[Status] = None