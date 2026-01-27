from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ...services.ai_service import ai_service

router = APIRouter()


@router.get("/capabilities")
async def get_ai_capabilities():
    """Get the AI processing capabilities."""
    return ai_service.get_capabilities()


@router.post("/process")
async def process_user_input(user_input: Dict[str, Any]):
    """Process user input through the AI system."""
    session_id = user_input.get("session_id")
    user_text = user_input.get("input", "")

    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")

    # Process the user input through the AI service
    result = await ai_service.process_user_input(user_text, session_id)
    return result