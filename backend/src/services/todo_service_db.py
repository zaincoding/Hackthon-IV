from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from ..models.database import DBTodo
from ..models.todo import TodoCreateRequest, TodoUpdateRequest


class TodoService:
    """Service class for todo operations with database storage."""

    def __init__(self):
        pass

    def create_todo(self, db: Session, user_id: str, todo_data: TodoCreateRequest):
        """Create a new todo for a user."""
        db_todo = DBTodo(
            user_id=user_id,
            title=todo_data.title,
            description=todo_data.description,
            due_date=todo_data.due_date,
            priority=todo_data.priority.value if todo_data.priority else "medium",
            category=todo_data.category,
            status="pending"
        )

        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)

        return db_todo

    def get_todos_by_user(self, db: Session, user_id: str) -> List[DBTodo]:
        """Get all todos for a user."""
        return db.query(DBTodo).filter(DBTodo.user_id == user_id).all()

    def get_todo_by_id(self, db: Session, todo_id: str, user_id: str) -> Optional[DBTodo]:
        """Get a specific todo by ID for a user."""
        return db.query(DBTodo).filter(
            DBTodo.id == todo_id,
            DBTodo.user_id == user_id
        ).first()

    def update_todo(self, db: Session, todo_id: str, user_id: str, todo_data: TodoUpdateRequest):
        """Update a todo."""
        db_todo = self.get_todo_by_id(db, todo_id, user_id)
        if not db_todo:
            return None

        # Update fields that were provided
        if todo_data.title is not None:
            db_todo.title = todo_data.title
        if todo_data.description is not None:
            db_todo.description = todo_data.description
        if todo_data.due_date is not None:
            db_todo.due_date = todo_data.due_date
        if todo_data.priority is not None:
            db_todo.priority = todo_data.priority.value
        if todo_data.category is not None:
            db_todo.category = todo_data.category
        if todo_data.status is not None:
            db_todo.status = todo_data.status.value
            if todo_data.status.value == "completed":
                db_todo.completed_at = datetime.utcnow()

        db_todo.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_todo)
        return db_todo

    def delete_todo(self, db: Session, todo_id: str, user_id: str) -> bool:
        """Delete a todo."""
        db_todo = self.get_todo_by_id(db, todo_id, user_id)
        if not db_todo:
            return False

        db.delete(db_todo)
        db.commit()
        return True

    def toggle_todo_completion(self, db: Session, todo_id: str, user_id: str) -> Optional[DBTodo]:
        """Toggle a todo's completion status."""
        db_todo = self.get_todo_by_id(db, todo_id, user_id)
        if not db_todo:
            return None

        if db_todo.status == "completed":
            db_todo.status = "pending"
            db_todo.completed_at = None
        else:
            db_todo.status = "completed"
            db_todo.completed_at = datetime.utcnow()

        db_todo.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_todo)
        return db_todo