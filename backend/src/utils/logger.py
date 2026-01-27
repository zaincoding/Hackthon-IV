import logging
import sys
from datetime import datetime
from typing import Any, Dict
from ..config.settings import settings


class Logger:
    """Custom logger for the application."""

    def __init__(self, name: str = "todo_chatbot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

        # Prevent adding multiple handlers if logger already has handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _log(self, level: int, message: str, extra: Dict[str, Any] = None):
        """Internal method to log a message."""
        if extra:
            self.logger.log(level, message, extra=extra)
        else:
            self.logger.log(level, message)

    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log an info message."""
        self._log(logging.INFO, message, extra)

    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log a debug message."""
        self._log(logging.DEBUG, message, extra)

    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log a warning message."""
        self._log(logging.WARNING, message, extra)

    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log an error message."""
        self._log(logging.ERROR, message, extra)

    def critical(self, message: str, extra: Dict[str, Any] = None):
        """Log a critical message."""
        self._log(logging.CRITICAL, message, extra)


# Global logger instance
logger = Logger()