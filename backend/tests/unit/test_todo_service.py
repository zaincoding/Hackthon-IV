"""
Unit tests for the TodoService class.
"""

import pytest
from unittest.mock import Mock, patch
from src.models.todo import TodoCreateRequest, TodoUpdateRequest, Priority, Status
from src.services.todo_service import TodoService
from src.models.session import Session


class TestTodoService:
    """Test cases for TodoService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.todo_service = TodoService()

        # Mock storage for testing
        self.mock_storage = Mock()
        self.todo_service.storage = self.mock_storage

    def test_create_todo_success(self):
        """Test creating a new todo successfully."""
        # Arrange
        session_id = "session-123"
        todo_data = TodoCreateRequest(
            title="Test todo",
            description="Test description",
            priority=Priority.MEDIUM
        )

        mock_session = Mock(spec=Session)
        mock_session.session_id = session_id
        self.mock_storage.get_session.return_value = mock_session

        # Act
        result = self.todo_service.create_todo(session_id, todo_data)

        # Assert
        assert result is not None
        assert result.title == "Test todo"
        assert result.description == "Test description"
        assert result.priority == Priority.MEDIUM
        self.mock_storage.get_session.assert_called_once_with(session_id)
        mock_session.add_todo.assert_called_once()

    def test_create_todo_session_not_found(self):
        """Test creating a todo when session doesn't exist."""
        # Arrange
        session_id = "nonexistent-session"
        todo_data = TodoCreateRequest(
            title="Test todo",
            description="Test description",
            priority=Priority.MEDIUM
        )

        self.mock_storage.get_session.return_value = None

        # Act
        result = self.todo_service.create_todo(session_id, todo_data)

        # Assert
        assert result is None
        self.mock_storage.get_session.assert_called_once_with(session_id)

    def test_get_todo_success(self):
        """Test getting a specific todo."""
        # Arrange
        session_id = "session-123"
        todo_id = "todo-123"
        mock_session = Mock(spec=Session)
        mock_session.get_todo.return_value = Mock()
        self.mock_storage.get_session.return_value = mock_session

        # Act
        result = self.todo_service.get_todo(session_id, todo_id)

        # Assert
        assert result is not None
        self.mock_storage.get_session.assert_called_once_with(session_id)
        mock_session.get_todo.assert_called_once_with(todo_id)

    def test_get_todo_not_found(self):
        """Test getting a todo that doesn't exist."""
        # Arrange
        session_id = "session-123"
        todo_id = "nonexistent-todo"
        mock_session = Mock(spec=Session)
        mock_session.get_todo.return_value = None
        self.mock_storage.get_session.return_value = mock_session

        # Act
        result = self.todo_service.get_todo(session_id, todo_id)

        # Assert
        assert result is None
        self.mock_storage.get_session.assert_called_once_with(session_id)
        mock_session.get_todo.assert_called_once_with(todo_id)

    def test_update_todo_success(self):
        """Test updating an existing todo."""
        # Arrange
        session_id = "session-123"
        todo_id = "todo-123"
        update_data = TodoUpdateRequest(title="Updated title")

        mock_todo = Mock()
        mock_todo.title = "Old title"
        mock_todo.status = Status.PENDING

        mock_session = Mock(spec=Session)
        mock_session.get_todo.return_value = mock_todo
        self.mock_storage.get_session.return_value = mock_session

        # Act
        result = self.todo_service.update_todo(session_id, todo_id, update_data)

        # Assert
        assert result is not None
        assert result.title == "Updated title"
        self.mock_storage.get_session.assert_called_once_with(session_id)
        mock_session.get_todo.assert_called_once_with(todo_id)
        self.mock_storage.update_session.assert_called_once_with(mock_session)

    def test_delete_todo_success(self):
        """Test deleting an existing todo."""
        # Arrange
        session_id = "session-123"
        todo_id = "todo-123"

        mock_session = Mock(spec=Session)
        mock_session.remove_todo.return_value = True
        self.mock_storage.get_session.return_value = mock_session

        # Act
        result = self.todo_service.delete_todo(session_id, todo_id)

        # Assert
        assert result is True
        self.mock_storage.get_session.assert_called_once_with(session_id)
        mock_session.remove_todo.assert_called_once_with(todo_id)

    def test_complete_todo_success(self):
        """Test completing an existing todo."""
        # Arrange
        session_id = "session-123"
        todo_id = "todo-123"

        mock_todo = Mock()
        mock_todo.title = "Test todo"
        mock_todo.status = Status.PENDING

        mock_session = Mock(spec=Session)
        mock_session.get_todo.return_value = mock_todo
        self.mock_storage.get_session.return_value = mock_session

        # Act
        result = self.todo_service.complete_todo(session_id, todo_id)

        # Assert
        assert result is not None
        assert result.status == Status.COMPLETED
        self.mock_storage.get_session.assert_called_once_with(session_id)
        mock_session.get_todo.assert_called_once_with(todo_id)
        self.mock_storage.update_session.assert_called_once_with(mock_session)

    def test_get_statistics(self):
        """Test getting todo statistics."""
        # Arrange
        session_id = "session-123"

        mock_todo_pending = Mock()
        mock_todo_pending.status = Status.PENDING

        mock_todo_completed = Mock()
        mock_todo_completed.status = Status.COMPLETED

        mock_session = Mock(spec=Session)
        mock_session.todos = [mock_todo_pending, mock_todo_completed]
        self.mock_storage.get_session.return_value = mock_session

        # Act
        result = self.todo_service.get_statistics(session_id)

        # Assert
        assert result is not None
        assert result["total"] == 2
        assert result["pending"] == 1
        assert result["completed"] == 1
        assert result["completion_rate"] == 0.5
        self.mock_storage.get_session.assert_called_once_with(session_id)