from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session
from ...models.todo import Todo, TodoCreateRequest, TodoUpdateRequest
from ...models.database import get_db, DBTodo
from ...services.todo_service_db import TodoService
from ...utils.auth import get_current_active_user
from ...models.user import User
from datetime import datetime


router = APIRouter()
todo_service = TodoService()


def convert_db_todo_to_pydantic(db_todo: DBTodo) -> Todo:
    """Convert a database Todo to a Pydantic Todo model."""
    return Todo(
        id=db_todo.id,
        title=db_todo.title,
        description=db_todo.description,
        due_date=db_todo.due_date,
        priority=db_todo.priority,
        category=db_todo.category,
        status=db_todo.status,
        created_at=db_todo.created_at.isoformat() if db_todo.created_at else datetime.utcnow().isoformat(),
        updated_at=db_todo.updated_at.isoformat() if db_todo.updated_at else datetime.utcnow().isoformat(),
        completed_at=db_todo.completed_at.isoformat() if db_todo.completed_at else None
    )


@router.post("/", response_model=Todo)
async def create_todo(
    todo_data: TodoCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new todo for the authenticated user."""
    # Validate and sanitize input data (using existing validation logic)
    # In a real implementation, we'd have proper sanitization here

    db_todo = todo_service.create_todo(db, current_user.id, todo_data)
    return convert_db_todo_to_pydantic(db_todo)


@router.get("/", response_model=List[Todo])
async def get_todos(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of results")
):
    """Get todos for the authenticated user with optional filtering."""
    # Validate query parameters
    if status and status not in ['pending', 'in-progress', 'completed', 'cancelled']:
        raise HTTPException(status_code=400, detail="Invalid status filter")

    db_todos = todo_service.get_todos_by_user(db, current_user.id)

    # Apply filters
    if status:
        db_todos = [todo for todo in db_todos if todo.status == status.lower()]
    if category:
        db_todos = [todo for todo in db_todos if todo.category and category.lower() in todo.category.lower()]

    # Apply limit
    if limit:
        db_todos = db_todos[:limit]

    # Convert to Pydantic models
    return [convert_db_todo_to_pydantic(todo) for todo in db_todos]


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific todo by ID for the authenticated user."""
    db_todo = todo_service.get_todo_by_id(db, todo_id, current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return convert_db_todo_to_pydantic(db_todo)


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: str,
    todo_data: TodoUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an existing todo for the authenticated user."""
    # Validate and sanitize input data (using existing validation logic)
    # In a real implementation, we'd have proper sanitization here

    db_todo = todo_service.update_todo(db, todo_id, current_user.id, todo_data)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return convert_db_todo_to_pydantic(db_todo)


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a todo for the authenticated user."""
    success = todo_service.delete_todo(db, todo_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/complete", response_model=Todo)
async def complete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a todo as completed for the authenticated user."""
    db_todo = todo_service.toggle_todo_completion(db, todo_id, current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return convert_db_todo_to_pydantic(db_todo)