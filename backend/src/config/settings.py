import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    APP_NAME: str = "AI-Powered Todo Chatbot"
    APP_DESCRIPTION: str = "An intelligent todo management system with natural language processing"
    APP_VERSION: str = "1.0.0"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"

    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")  # Default to SQLite for backward compatibility

    # Session settings
    SESSION_TIMEOUT_HOURS: int = int(os.getenv("SESSION_TIMEOUT_HOURS", 24))
    MAX_TODOS_PER_SESSION: int = int(os.getenv("MAX_TODOS_PER_SESSION", 1000))
    MAX_SESSION_MEMORY_MB: float = float(os.getenv("MAX_SESSION_MEMORY_MB", 5.0))

    # MCP settings
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", 3001))


settings = Settings()