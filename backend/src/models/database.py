from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Text, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from ..config.settings import settings
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class DBUser(Base):
    """Database User model for SQLAlchemy."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to todos
    todos = relationship("DBTodo", back_populates="user", cascade="all, delete-orphan")


class DBTodo(Base):
    """Database Todo model for SQLAlchemy."""

    __tablename__ = "todos"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    due_date = Column(String(30))  # ISO 8601 format
    priority = Column(String(10), default="medium")  # low, medium, high
    category = Column(String(50))
    status = Column(String(20), default="pending")  # pending, in-progress, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationship to user
    user = relationship("DBUser", back_populates="todos")


# Database engine and session setup
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)