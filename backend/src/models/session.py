from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field
from .todo import Todo, Priority


class Preferences(BaseModel):
    """User preferences model."""
    default_priority: Priority = Priority.MEDIUM
    default_category: Optional[str] = None
    date_format: str = "MM/DD/YYYY"  # Enum in real implementation
    notification_enabled: bool = True
    theme: str = "auto"  # light, dark, auto


class Session(BaseModel):
    """Session model representing a user's session with their todos."""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    todos: List[Todo] = Field(default_factory=list)
    preferences: Preferences = Field(default_factory=Preferences)
    last_interaction: str = Field(default_factory=lambda: datetime.now().isoformat())
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def add_todo(self, todo: Todo):
        """Add a todo to the session."""
        self.todos.append(todo)
        self.update_last_interaction()

    def remove_todo(self, todo_id: str) -> bool:
        """Remove a todo from the session by ID."""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                self.update_last_interaction()
                return True
        return False

    def get_todo(self, todo_id: str) -> Optional[Todo]:
        """Get a todo by ID."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_last_interaction(self):
        """Update the last interaction timestamp."""
        self.last_interaction = datetime.now().isoformat()

    def get_active_todos(self) -> List[Todo]:
        """Get all active (non-completed) todos."""
        return [todo for todo in self.todos if todo.status != 'completed']

    def get_completed_todos(self) -> List[Todo]:
        """Get all completed todos."""
        return [todo for todo in self.todos if todo.status == 'completed']


class SessionCreateRequest(BaseModel):
    """Request model for creating a new session."""
    user_id: Optional[str] = None
    preferences: Optional[Preferences] = None


class SessionResponse(BaseModel):
    """Response model for session data."""
    session_id: str
    user_id: Optional[str]
    todo_count: int
    active_todo_count: int
    completed_todo_count: int
    last_interaction: str
    created_at: str