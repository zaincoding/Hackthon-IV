"""
MCP-compliant tools for todo operations.
These tools allow the AI agent to interact with the todo management system.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from ..models.todo import TodoCreateRequest, TodoUpdateRequest, Status
from ..services.todo_service import TodoService
from ..services.session_service import SessionService


class TodoToolResult(BaseModel):
    """Standard result format for todo tool operations."""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None


class TodoTools:
    """Collection of MCP-compliant tools for todo operations."""

    def __init__(self):
        self.todo_service = TodoService()
        self.session_service = SessionService()

    def add_todo_tool(
        self,
        session_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = "medium",
        category: Optional[str] = None
    ) -> TodoToolResult:
        """
        Add a new todo to a session.

        Args:
            session_id: The session ID
            title: The todo title
            description: Optional description
            due_date: Optional due date in ISO format
            priority: Priority level (low, medium, high)
            category: Optional category

        Returns:
            TodoToolResult with the created todo
        """
        try:
            # Validate priority
            if priority and priority not in ["low", "medium", "high"]:
                return TodoToolResult(
                    success=False,
                    message="Invalid priority. Must be low, medium, or high.",
                    error="invalid_priority"
                )

            # Create todo data
            todo_data = TodoCreateRequest(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category=category
            )

            # Create the todo
            todo = self.todo_service.create_todo(session_id, todo_data)

            if not todo:
                return TodoToolResult(
                    success=False,
                    message="Session not found",
                    error="session_not_found"
                )

            return TodoToolResult(
                success=True,
                message=f"Todo '{todo.title}' added successfully",
                data=todo.dict()
            )
        except Exception as e:
            return TodoToolResult(
                success=False,
                message="Failed to add todo",
                error=str(e)
            )

    def list_todos_tool(
        self,
        session_id: str,
        status: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None
    ) -> TodoToolResult:
        """
        List todos in a session with optional filtering.

        Args:
            session_id: The session ID
            status: Optional status filter (pending, completed, etc.)
            category: Optional category filter
            limit: Optional limit on number of results

        Returns:
            TodoToolResult with list of todos
        """
        try:
            todos = self.todo_service.get_todos(session_id, status, category, limit)

            if todos is None:
                return TodoToolResult(
                    success=False,
                    message="Session not found",
                    error="session_not_found"
                )

            return TodoToolResult(
                success=True,
                message=f"Found {len(todos)} todos",
                data=[todo.dict() for todo in todos]
            )
        except Exception as e:
            return TodoToolResult(
                success=False,
                message="Failed to list todos",
                error=str(e)
            )

    def edit_todo_tool(
        self,
        session_id: str,
        todo_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> TodoToolResult:
        """
        Edit an existing todo.

        Args:
            session_id: The session ID
            todo_id: The ID of the todo to edit
            title: New title (optional)
            description: New description (optional)
            due_date: New due date (optional)
            priority: New priority (optional)
            category: New category (optional)
            status: New status (optional)

        Returns:
            TodoToolResult with updated todo
        """
        try:
            # Validate status if provided
            if status and status not in ["pending", "in-progress", "completed", "cancelled"]:
                return TodoToolResult(
                    success=False,
                    message="Invalid status. Must be pending, in-progress, completed, or cancelled.",
                    error="invalid_status"
                )

            # Validate priority if provided
            if priority and priority not in ["low", "medium", "high"]:
                return TodoToolResult(
                    success=False,
                    message="Invalid priority. Must be low, medium, or high.",
                    error="invalid_priority"
                )

            # Create update data
            update_data = TodoUpdateRequest(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category=category,
                status=status
            )

            # Update the todo
            updated_todo = self.todo_service.update_todo(session_id, todo_id, update_data)

            if not updated_todo:
                return TodoToolResult(
                    success=False,
                    message="Todo or session not found",
                    error="todo_or_session_not_found"
                )

            return TodoToolResult(
                success=True,
                message=f"Todo '{updated_todo.title}' updated successfully",
                data=updated_todo.dict()
            )
        except Exception as e:
            return TodoToolResult(
                success=False,
                message="Failed to edit todo",
                error=str(e)
            )

    def delete_todo_tool(
        self,
        session_id: str,
        todo_id: str
    ) -> TodoToolResult:
        """
        Delete a todo from a session.

        Args:
            session_id: The session ID
            todo_id: The ID of the todo to delete

        Returns:
            TodoToolResult with operation result
        """
        try:
            success = self.todo_service.delete_todo(session_id, todo_id)

            if not success:
                return TodoToolResult(
                    success=False,
                    message="Todo or session not found",
                    error="todo_or_session_not_found"
                )

            return TodoToolResult(
                success=True,
                message="Todo deleted successfully"
            )
        except Exception as e:
            return TodoToolResult(
                success=False,
                message="Failed to delete todo",
                error=str(e)
            )

    def complete_todo_tool(
        self,
        session_id: str,
        todo_id: str
    ) -> TodoToolResult:
        """
        Mark a todo as completed.

        Args:
            session_id: The session ID
            todo_id: The ID of the todo to complete

        Returns:
            TodoToolResult with updated todo
        """
        try:
            completed_todo = self.todo_service.complete_todo(session_id, todo_id)

            if not completed_todo:
                return TodoToolResult(
                    success=False,
                    message="Todo or session not found",
                    error="todo_or_session_not_found"
                )

            return TodoToolResult(
                success=True,
                message=f"Todo '{completed_todo.title}' marked as completed",
                data=completed_todo.dict()
            )
        except Exception as e:
            return TodoToolResult(
                success=False,
                message="Failed to complete todo",
                error=str(e)
            )


# Global instance of todo tools
todo_tools = TodoTools()