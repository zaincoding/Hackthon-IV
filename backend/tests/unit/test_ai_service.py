"""
Unit tests for the AIService class.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.services.ai_service import AIService


class TestAIService:
    """Test cases for AIService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.ai_service = AIService()

    @pytest.mark.asyncio
    async def test_extract_intent_and_entities_add_todo(self):
        """Test extracting add_todo intent and entities."""
        # Arrange
        user_input = "Add buy groceries to my todos"

        # Act
        intent, entities = self.ai_service._extract_intent_and_entities(user_input)

        # Assert
        assert intent == "add_todo"
        assert "title" in entities
        assert entities["title"] == "buy groceries"

    @pytest.mark.asyncio
    async def test_extract_intent_and_entities_view_todos(self):
        """Test extracting view_todos intent and entities."""
        # Arrange
        user_input = "Show me my pending todos"

        # Act
        intent, entities = self.ai_service._extract_intent_and_entities(user_input)

        # Assert
        assert intent == "view_todos"
        assert "status" in entities
        assert entities["status"] == "pending"

    @pytest.mark.asyncio
    async def test_extract_intent_and_entities_complete_todo(self):
        """Test extracting complete_todo intent and entities."""
        # Arrange
        user_input = "Complete task #3"

        # Act
        intent, entities = self.ai_service._extract_intent_and_entities(user_input)

        # Assert
        assert intent == "complete_todo"
        assert "todo_id" in entities
        assert entities["todo_id"] == "3"

    @pytest.mark.asyncio
    async def test_extract_intent_and_entities_unknown(self):
        """Test extracting unknown intent."""
        # Arrange
        user_input = "This is not a recognized command"

        # Act
        intent, entities = self.ai_service._extract_intent_and_entities(user_input)

        # Assert
        assert intent == "unknown"
        assert "original_input" in entities
        assert entities["original_input"] == user_input

    @pytest.mark.asyncio
    async def test_process_user_input_add_todo(self):
        """Test processing user input for adding a todo."""
        # Arrange
        user_input = "Add buy groceries to my todos"
        session_id = "session-123"

        # Mock the MCP server response
        with patch.object(self.ai_service, '_call_mcp_tool') as mock_call:
            mock_call.return_value = {
                "success": True,
                "data": {"title": "buy groceries", "id": "todo-123"}
            }

            # Act
            result = await self.ai_service.process_user_input(user_input, session_id)

            # Assert
            assert result["intent"] == "add_todo"
            assert "buy groceries" in result["response_text"]

    @pytest.mark.asyncio
    async def test_process_user_input_view_todos(self):
        """Test processing user input for viewing todos."""
        # Arrange
        user_input = "Show me my pending todos"
        session_id = "session-123"

        # Mock the MCP server response
        with patch.object(self.ai_service, '_call_mcp_tool') as mock_call:
            mock_call.return_value = {
                "success": True,
                "data": [
                    {"title": "buy groceries", "status": "pending", "id": "todo-123"},
                    {"title": "walk the dog", "status": "pending", "id": "todo-124"}
                ]
            }

            # Act
            result = await self.ai_service.process_user_input(user_input, session_id)

            # Assert
            assert result["intent"] == "view_todos"
            assert "2 todos" in result["response_text"]

    @pytest.mark.asyncio
    async def test_get_capabilities(self):
        """Test getting AI capabilities."""
        # Act
        result = self.ai_service.get_capabilities()

        # Assert
        assert "supported_intents" in result
        assert "entity_types" in result
        assert "max_tokens" in result
        assert "supported_commands" in result
        assert "add_todo" in result["supported_intents"]