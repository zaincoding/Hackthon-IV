from typing import List, Optional
from ..models.session import Session, SessionCreateRequest, SessionResponse, Preferences
from .storage import storage


class SessionService:
    """Service layer for session management."""

    def __init__(self):
        self.storage = storage

    def create_session(self, session_data: Optional[SessionCreateRequest] = None) -> Session:
        """Create a new session."""
        if session_data:
            session = Session(
                user_id=session_data.user_id,
                preferences=session_data.preferences or Preferences()
            )
        else:
            session = Session()

        return self.storage.add_session(session)

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        return self.storage.get_session(session_id)

    def get_session_response(self, session_id: str) -> Optional[SessionResponse]:
        """Get a session response with summary information."""
        session = self.storage.get_session(session_id)
        if not session:
            return None

        # Count todos
        todo_count = len(session.todos)
        active_todos = [t for t in session.todos if t.status != 'completed']
        completed_todos = [t for t in session.todos if t.status == 'completed']

        return SessionResponse(
            session_id=session.session_id,
            user_id=session.user_id,
            todo_count=todo_count,
            active_todo_count=len(active_todos),
            completed_todo_count=len(completed_todos),
            last_interaction=session.last_interaction,
            created_at=session.created_at
        )

    def update_preferences(self, session_id: str, preferences: Preferences) -> bool:
        """Update session preferences."""
        session = self.storage.get_session(session_id)
        if not session:
            return False

        session.preferences = preferences
        session.update_last_interaction()
        return self.storage.update_session(session)

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        return self.storage.remove_session(session_id)

    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        return self.storage.cleanup_expired_sessions()

    def get_all_sessions(self) -> List[Session]:
        """Get all sessions."""
        return self.storage.get_all_sessions()

    def get_memory_usage(self) -> dict:
        """Get memory usage statistics."""
        return self.storage.get_memory_usage()