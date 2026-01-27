import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from threading import Lock
from ..models.session import Session
from ..models.context import context_manager


class InMemoryStorage:
    """
    In-memory storage for managing sessions and todos.
    Implements the privacy-first principle with optional persistence.
    """

    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        self._lock = Lock()  # Thread-safe access
        self._cleanup_task = None

    def add_session(self, session: Session) -> Session:
        """Add a new session to storage."""
        with self._lock:
            self._sessions[session.session_id] = session
            return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve a session by ID."""
        with self._lock:
            return self._sessions.get(session_id)

    def update_session(self, session: Session) -> bool:
        """Update an existing session."""
        with self._lock:
            if session.session_id in self._sessions:
                self._sessions[session.session_id] = session
                return True
            return False

    def remove_session(self, session_id: str) -> bool:
        """Remove a session by ID."""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

    def get_all_sessions(self) -> List[Session]:
        """Get all sessions."""
        with self._lock:
            return list(self._sessions.values())

    def cleanup_expired_sessions(self) -> int:
        """
        Remove sessions that have exceeded the timeout period.
        Returns the number of sessions removed.
        """
        with self._lock:
            current_time = datetime.now()
            removed_count = 0

            # Convert dict_keys to list to avoid dictionary changed size during iteration
            session_ids = list(self._sessions.keys())

            for session_id in session_ids:
                session = self._sessions[session_id]
                last_interaction = datetime.fromisoformat(session.last_interaction.replace('Z', '+00:00'))

                # Calculate timeout based on settings (default 24 hours)
                from ..config.settings import settings
                timeout_hours = settings.SESSION_TIMEOUT_HOURS
                timeout_period = timedelta(hours=timeout_hours)

                if current_time - last_interaction > timeout_period:
                    del self._sessions[session_id]
                    removed_count += 1

            return removed_count

    def get_memory_usage(self) -> Dict[str, int]:
        """Get memory usage statistics."""
        with self._lock:
            session_count = len(self._sessions)
            total_todos = sum(len(session.todos) for session in self._sessions.values())
            return {
                "session_count": session_count,
                "total_todos": total_todos,
                "active_todos": sum(
                    len([t for t in session.todos if t.status != 'completed'])
                    for session in self._sessions.values()
                )
            }


# Global storage instance
storage = InMemoryStorage()