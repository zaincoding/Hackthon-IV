"""
Comprehensive logging and monitoring utilities for the AI-Powered Todo Chatbot.
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from ..config.settings import settings


class DetailedLogger:
    """Enhanced logger with additional monitoring capabilities."""

    def __init__(self, name: str = "todo_chatbot_detailed"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

        # Prevent adding multiple handlers if logger already has handlers
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

            # Create file handler (optional, depending on settings)
            if hasattr(settings, 'LOG_FILE') and settings.LOG_FILE:
                file_handler = logging.FileHandler(settings.LOG_FILE)
                file_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
            else:
                file_handler = None

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )

            console_handler.setFormatter(formatter)
            if file_handler:
                file_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)
            if file_handler:
                self.logger.addHandler(file_handler)

    def log_request(self,
                   session_id: str,
                   user_input: str,
                   response: str,
                   processing_time: float,
                   extra: Optional[Dict[str, Any]] = None):
        """Log API request details for monitoring."""
        self.logger.info(
            f"API Request - Session: {session_id}, "
            f"Input: {user_input[:50]}{'...' if len(user_input) > 50 else ''}, "
            f"Response length: {len(response)}, "
            f"Processing time: {processing_time:.2f}s",
            extra=extra or {}
        )

    def log_todo_operation(self,
                          operation: str,
                          session_id: str,
                          todo_id: Optional[str] = None,
                          details: Optional[Dict[str, Any]] = None):
        """Log todo operation for audit trail."""
        details_str = f", Details: {details}" if details else ""
        self.logger.info(
            f"Todo Operation - {operation}, Session: {session_id}{', Todo: ' + todo_id if todo_id else ''}{details_str}"
        )

    def log_performance(self,
                       metric_name: str,
                       value: float,
                       unit: str = "",
                       extra: Optional[Dict[str, Any]] = None):
        """Log performance metrics."""
        self.logger.info(
            f"PERFORMANCE - {metric_name}: {value} {unit}",
            extra=extra or {}
        )

    def log_error(self,
                 error: Exception,
                 context: str = "",
                 session_id: Optional[str] = None,
                 extra: Optional[Dict[str, Any]] = None):
        """Log error with context."""
        context_str = f", Context: {context}" if context else ""
        session_str = f", Session: {session_id}" if session_id else ""

        self.logger.error(
            f"ERROR - {type(error).__name__}: {str(error)}{context_str}{session_str}",
            extra=extra or {}
        )

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log an info message."""
        self.logger.info(message, extra=extra or {})

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log a debug message."""
        self.logger.debug(message, extra=extra or {})

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log a warning message."""
        self.logger.warning(message, extra=extra or {})

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log an error message."""
        self.logger.error(message, extra=extra or {})

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log a critical message."""
        self.logger.critical(message, extra=extra or {})


# Global detailed logger instance
detailed_logger = DetailedLogger()