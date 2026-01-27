from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from enum import Enum


class ContextType(Enum):
    """Types of conversation contexts."""
    NUMBER_SELECTION = "number_selection"
    CONFIRMATION_REQUEST = "confirmation_request"
    FOLLOW_UP_QUESTION = "follow_up_question"


class ConversationContext(BaseModel):
    """Represents the context of a conversation session."""
    session_id: str
    context_type: ContextType
    timestamp: str
    options: List[Dict[str, Any]]  # List of options that were presented
    original_request: str  # The original request that led to the options
    expires_at: Optional[str] = None  # When this context expires


class ContextManager:
    """Manages conversation contexts for sessions."""

    def __init__(self):
        self._contexts: Dict[str, ConversationContext] = {}

    def store_context(self, context: ConversationContext):
        """Store a conversation context."""
        self._contexts[context.session_id] = context

    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        """Retrieve a conversation context."""
        return self._contexts.get(session_id)

    def clear_context(self, session_id: str) -> bool:
        """Clear a conversation context."""
        if session_id in self._contexts:
            del self._contexts[session_id]
            return True
        return False

    def cleanup_expired_contexts(self):
        """Remove expired contexts."""
        current_time = datetime.now().isoformat()
        expired_sessions = []

        for session_id, context in self._contexts.items():
            if context.expires_at and context.expires_at < current_time:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self._contexts[session_id]


# Global context manager instance
context_manager = ContextManager()