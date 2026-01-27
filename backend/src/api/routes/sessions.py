from fastapi import APIRouter, HTTPException
from typing import List
from ...models.session import Session, SessionCreateRequest, SessionResponse
from ...services.session_service import SessionService

router = APIRouter()
session_service = SessionService()


@router.post("/", response_model=Session)
async def create_session(session_data: SessionCreateRequest = None):
    """Create a new session."""
    session = session_service.create_session(session_data)
    return session


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Get session information."""
    session_response = session_service.get_session_response(session_id)
    if not session_response:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_response


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    success = session_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


@router.post("/{session_id}/cleanup")
async def cleanup_sessions():
    """Clean up expired sessions."""
    removed_count = session_service.cleanup_expired_sessions()
    return {"removed_sessions": removed_count, "message": "Expired sessions cleaned up"}