from sqlalchemy.orm import Session
from ..models.database import DBUser, DBTodo
from ..models.user import UserCreateRequest
from ..utils.auth import get_password_hash
from typing import Optional


class UserService:
    """Service class for user operations."""

    def __init__(self):
        pass

    def create_user(self, db: Session, user_data: UserCreateRequest):
        """Create a new user."""
        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create the database user object
        db_user = DBUser(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        # Add to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def get_user_by_username(self, db: Session, username: str) -> Optional[DBUser]:
        """Get a user by username."""
        return db.query(DBUser).filter(DBUser.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[DBUser]:
        """Get a user by email."""
        return db.query(DBUser).filter(DBUser.email == email).first()

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[DBUser]:
        """Get a user by ID."""
        return db.query(DBUser).filter(DBUser.id == user_id).first()

    def update_user(self, db: Session, user_id: str, **kwargs):
        """Update a user."""
        db_user = self.get_user_by_id(db, user_id)
        if not db_user:
            return None

        for key, value in kwargs.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: str) -> bool:
        """Delete a user."""
        db_user = self.get_user_by_id(db, user_id)
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        return True