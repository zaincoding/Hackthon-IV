from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ...models.todo import Todo, TodoCreateRequest, TodoUpdateRequest
from ...services.todo_service import TodoService
from ...utils.security import security_validator

router = APIRouter()
todo_service = TodoService()


@router.post("/", response_model=Todo)
async def create_todo(session_id: str, todo_data: TodoCreateRequest):
    """Create a new todo in the specified session."""
    # Validate session ID
    if not security_validator.is_valid_uuid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    # Validate and sanitize input data
    try:
        validated_data = security_validator.validate_todo_input(todo_data.dict())
        # Update the todo_data with validated values
        for key, value in validated_data.items():
            setattr(todo_data, key, value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    todo = todo_service.create_todo(session_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Session not found")
    return todo


@router.get("/", response_model=List[Todo])
async def get_todos(
    session_id: str,
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of results")
):
    """Get todos from the specified session with optional filtering."""
    # Validate session ID
    if not security_validator.is_valid_uuid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    # Validate query parameters
    if status and status not in ['pending', 'in-progress', 'completed', 'cancelled']:
        raise HTTPException(status_code=400, detail="Invalid status filter")

    if category:
        sanitized_category = security_validator.sanitize_input(category)
        category = sanitized_category

    todos = todo_service.get_todos(session_id, status, category, limit)
    if todos is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return todos


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(session_id: str, todo_id: str):
    """Get a specific todo by ID."""
    # Validate session ID
    if not security_validator.is_valid_uuid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    # Validate todo ID
    if not security_validator.is_valid_uuid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    todo = todo_service.get_todo(session_id, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo or session not found")
    return todo


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(session_id: str, todo_id: str, todo_data: TodoUpdateRequest):
    """Update an existing todo."""
    # Validate session ID
    if not security_validator.is_valid_uuid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    # Validate todo ID
    if not security_validator.is_valid_uuid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    # Validate and sanitize input data
    try:
        validated_data = security_validator.validate_todo_input(todo_data.dict(exclude_unset=True))
        # Update the todo_data with validated values
        for key, value in validated_data.items():
            setattr(todo_data, key, value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    todo = todo_service.update_todo(session_id, todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo or session not found")
    return todo


@router.delete("/{todo_id}")
async def delete_todo(session_id: str, todo_id: str):
    """Delete a todo."""
    # Validate session ID
    if not security_validator.is_valid_uuid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    # Validate todo ID
    if not security_validator.is_valid_uuid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    success = todo_service.delete_todo(session_id, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo or session not found")
    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/complete", response_model=Todo)
async def complete_todo(session_id: str, todo_id: str):
    """Mark a todo as completed."""
    # Validate session ID
    if not security_validator.is_valid_uuid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    # Validate todo ID
    if not security_validator.is_valid_uuid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    todo = todo_service.complete_todo(session_id, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo or session not found")
    return todo