from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from sqlalchemy.orm import Session

from ...services.ai_service import ai_service
from ...utils.auth import get_current_active_user
from ...models.user import User
from ...models.database import get_db

router = APIRouter()


@router.get("/capabilities")
async def get_ai_capabilities():
    """Get the AI processing capabilities."""
    return ai_service.get_capabilities()


@router.post("/process")
async def process_user_input(
    user_input: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Process user input through the AI system."""
    user_text = user_input.get("input", "")

    # Use the authenticated user ID as the session identifier for database operations
    # This allows the AI service to operate on the user's database-stored todos
    session_id = f"user_{current_user.id}"

    # Process the user input through the AI service
    result = await ai_service.process_user_input(user_text, session_id)
    return result