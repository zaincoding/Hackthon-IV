"""
MCP (Model Context Protocol) Server for Todo Operations
This module implements an MCP-compliant server that exposes todo operations as tools
that can be called by the AI agent.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from .todo_tools import todo_tools, TodoToolResult
from ..config.settings import settings


class MCPCall(BaseModel):
    """Represents an MCP tool call."""
    tool_name: str
    arguments: Dict[str, Any]


class MCPResponse(BaseModel):
    """Represents an MCP response."""
    result: Any
    is_error: bool = False
    error_message: Optional[str] = None


class MCPServer:
    """
    MCP-compliant server that exposes todo operations as tools.
    This allows the AI agent to call these tools to perform todo operations.
    """

    def __init__(self):
        self.tools = {
            "add_todo": self._call_add_todo,
            "list_todos": self._call_list_todos,
            "edit_todo": self._call_edit_todo,
            "delete_todo": self._call_delete_todo,
            "complete_todo": self._call_complete_todo,
        }
        self.port = settings.MCP_SERVER_PORT

    def _call_add_todo(self, **kwargs) -> TodoToolResult:
        """Wrapper for the add_todo tool."""
        session_id = kwargs.get("session_id")
        title = kwargs.get("title")
        description = kwargs.get("description")
        due_date = kwargs.get("due_date")
        priority = kwargs.get("priority")
        category = kwargs.get("category")

        if not session_id or not title:
            return TodoToolResult(
                success=False,
                message="session_id and title are required",
                error="missing_required_parameters"
            )

        return todo_tools.add_todo_tool(
            session_id=session_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=category
        )

    def _call_list_todos(self, **kwargs) -> TodoToolResult:
        """Wrapper for the list_todos tool."""
        session_id = kwargs.get("session_id")
        status = kwargs.get("status")
        category = kwargs.get("category")
        limit = kwargs.get("limit")

        if not session_id:
            return TodoToolResult(
                success=False,
                message="session_id is required",
                error="missing_required_parameters"
            )

        return todo_tools.list_todos_tool(
            session_id=session_id,
            status=status,
            category=category,
            limit=limit
        )

    def _call_edit_todo(self, **kwargs) -> TodoToolResult:
        """Wrapper for the edit_todo tool."""
        session_id = kwargs.get("session_id")
        todo_id = kwargs.get("todo_id")

        if not session_id or not todo_id:
            return TodoToolResult(
                success=False,
                message="session_id and todo_id are required",
                error="missing_required_parameters"
            )

        # Extract optional parameters
        title = kwargs.get("title")
        description = kwargs.get("description")
        due_date = kwargs.get("due_date")
        priority = kwargs.get("priority")
        category = kwargs.get("category")
        status = kwargs.get("status")

        return todo_tools.edit_todo_tool(
            session_id=session_id,
            todo_id=todo_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=category,
            status=status
        )

    def _call_delete_todo(self, **kwargs) -> TodoToolResult:
        """Wrapper for the delete_todo tool."""
        session_id = kwargs.get("session_id")
        todo_id = kwargs.get("todo_id")

        if not session_id or not todo_id:
            return TodoToolResult(
                success=False,
                message="session_id and todo_id are required",
                error="missing_required_parameters"
            )

        return todo_tools.delete_todo_tool(
            session_id=session_id,
            todo_id=todo_id
        )

    def _call_complete_todo(self, **kwargs) -> TodoToolResult:
        """Wrapper for the complete_todo tool."""
        session_id = kwargs.get("session_id")
        todo_id = kwargs.get("todo_id")

        if not session_id or not todo_id:
            return TodoToolResult(
                success=False,
                message="session_id and todo_id are required",
                error="missing_required_parameters"
            )

        return todo_tools.complete_todo_tool(
            session_id=session_id,
            todo_id=todo_id
        )

    async def handle_request(self, request_data: Dict[str, Any]) -> MCPResponse:
        """
        Handle an incoming MCP request.

        Args:
            request_data: Dictionary containing the request information

        Returns:
            MCPResponse with the result of the operation
        """
        try:
            # Extract tool name and arguments
            tool_name = request_data.get("tool_name")
            arguments = request_data.get("arguments", {})

            if not tool_name:
                return MCPResponse(
                    result=None,
                    is_error=True,
                    error_message="Missing tool_name in request"
                )

            if tool_name not in self.tools:
                return MCPResponse(
                    result=None,
                    is_error=True,
                    error_message=f"Unknown tool: {tool_name}"
                )

            # Call the appropriate tool
            tool_func = self.tools[tool_name]
            result = tool_func(**arguments)

            # Check if the result is a TodoToolResult with errors
            is_error = False
            error_message = None

            if hasattr(result, 'success') and not result.success:
                is_error = True
                error_message = result.error or result.message or "Tool operation failed"

            return MCPResponse(
                result=result,
                is_error=is_error,
                error_message=error_message
            )

        except Exception as e:
            return MCPResponse(
                result=None,
                is_error=True,
                error_message=f"Error processing request: {str(e)}"
            )

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get a list of available tools with their descriptions.

        Returns:
            List of tool descriptions
        """
        return [
            {
                "name": "add_todo",
                "description": "Add a new todo to a session",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "The session ID"},
                        "title": {"type": "string", "description": "The todo title"},
                        "description": {"type": "string", "description": "Optional description"},
                        "due_date": {"type": "string", "description": "Optional due date in ISO format"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority level"},
                        "category": {"type": "string", "description": "Optional category"}
                    },
                    "required": ["session_id", "title"]
                }
            },
            {
                "name": "list_todos",
                "description": "List todos in a session with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "The session ID"},
                        "status": {"type": "string", "enum": ["pending", "in-progress", "completed", "cancelled"], "description": "Optional status filter"},
                        "category": {"type": "string", "description": "Optional category filter"},
                        "limit": {"type": "integer", "description": "Optional limit on number of results"}
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "edit_todo",
                "description": "Edit an existing todo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "The session ID"},
                        "todo_id": {"type": "string", "description": "The ID of the todo to edit"},
                        "title": {"type": "string", "description": "New title (optional)"},
                        "description": {"type": "string", "description": "New description (optional)"},
                        "due_date": {"type": "string", "description": "New due date (optional)"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority (optional)"},
                        "category": {"type": "string", "description": "New category (optional)"},
                        "status": {"type": "string", "enum": ["pending", "in-progress", "completed", "cancelled"], "description": "New status (optional)"}
                    },
                    "required": ["session_id", "todo_id"]
                }
            },
            {
                "name": "delete_todo",
                "description": "Delete a todo from a session",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "The session ID"},
                        "todo_id": {"type": "string", "description": "The ID of the todo to delete"}
                    },
                    "required": ["session_id", "todo_id"]
                }
            },
            {
                "name": "complete_todo",
                "description": "Mark a todo as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "The session ID"},
                        "todo_id": {"type": "string", "description": "The ID of the todo to complete"}
                    },
                    "required": ["session_id", "todo_id"]
                }
            }
        ]


# Global MCP server instance
mcp_server = MCPServer()