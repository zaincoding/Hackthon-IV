from datetime import datetime
from typing import List, Optional
from ..models.todo import Todo, TodoCreateRequest, TodoUpdateRequest, Status
from ..models.session import Session
from .storage import storage


class TodoService:
    """Service layer for todo operations."""

    def __init__(self):
        self.storage = storage

    def create_todo(self, session_id: str, todo_data: TodoCreateRequest) -> Optional[Todo]:
        """Create a new todo in the specified session."""
        session = self.storage.get_session(session_id)
        if not session:
            return None

        # Create new todo from request data
        todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            due_date=todo_data.due_date,
            priority=todo_data.priority or session.preferences.default_priority,
            category=todo_data.category or session.preferences.default_category,
        )

        session.add_todo(todo)
        self.storage.update_session(session)

        return todo

    def get_todo(self, session_id: str, todo_id: str) -> Optional[Todo]:
        """Get a specific todo from a session."""
        session = self.storage.get_session(session_id)
        if not session:
            return None

        return session.get_todo(todo_id)

    def get_todos(
        self,
        session_id: str,
        status: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Todo]:
        """Get todos from a session with optional filtering."""
        session = self.storage.get_session(session_id)
        if not session:
            return []

        todos = session.todos

        # Apply filters
        if status:
            todos = [todo for todo in todos if todo.status.value == status.lower()]
        if category:
            todos = [todo for todo in todos if todo.category and category.lower() in todo.category.lower()]

        # Apply limit
        if limit:
            todos = todos[:limit]

        return todos

    def update_todo(
        self,
        session_id: str,
        todo_id: str,
        todo_data: TodoUpdateRequest
    ) -> Optional[Todo]:
        """Update an existing todo."""
        session = self.storage.get_session(session_id)
        if not session:
            return None

        todo = session.get_todo(todo_id)
        if not todo:
            return None

        # Update fields if provided in the request
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        if todo_data.due_date is not None:
            todo.due_date = todo_data.due_date
        if todo_data.priority is not None:
            todo.priority = todo_data.priority
        if todo_data.category is not None:
            todo.category = todo_data.category
        if todo_data.status is not None:
            # Handle status transition logic
            old_status = todo.status
            todo.status = todo_data.status

            # Update completed_at if status changed to completed
            if todo.status == Status.COMPLETED and old_status != Status.COMPLETED:
                todo.completed_at = datetime.now().isoformat()
            elif todo.status != Status.COMPLETED:
                todo.completed_at = None

        todo.update_timestamp()
        self.storage.update_session(session)

        return todo

    def delete_todo(self, session_id: str, todo_id: str) -> bool:
        """Delete a todo from a session."""
        session = self.storage.get_session(session_id)
        if not session:
            return False

        return session.remove_todo(todo_id)

    def complete_todo(self, session_id: str, todo_id: str) -> Optional[Todo]:
        """Mark a todo as completed."""
        session = self.storage.get_session(session_id)
        if not session:
            return None

        todo = session.get_todo(todo_id)
        if not todo:
            return None

        todo.mark_completed()
        self.storage.update_session(session)

        return todo

    def get_statistics(self, session_id: str) -> dict:
        """Get statistics for todos in a session."""
        session = self.storage.get_session(session_id)
        if not session:
            return {}

        all_todos = session.todos
        completed_todos = [t for t in all_todos if t.status == Status.COMPLETED]
        pending_todos = [t for t in all_todos if t.status == Status.PENDING]
        in_progress_todos = [t for t in all_todos if t.status == Status.IN_PROGRESS]
        cancelled_todos = [t for t in all_todos if t.status == Status.CANCELLED]

        return {
            "total": len(all_todos),
            "completed": len(completed_todos),
            "pending": len(pending_todos),
            "in_progress": len(in_progress_todos),
            "cancelled": len(cancelled_todos),
            "completion_rate": len(completed_todos) / len(all_todos) if all_todos else 0
        }