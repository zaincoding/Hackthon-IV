"""
Security utilities for the AI-Powered Todo Chatbot.
Includes input validation, sanitization, and other security measures.
"""

import re
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from pydantic import BaseModel
from ..utils.logger import logger


class SecurityValidator:
    """Utility class for security-related validation and sanitization."""

    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Sanitize user input to prevent injection attacks.
        """
        if not text:
            return text

        # Remove potentially dangerous characters/sequences
        sanitized = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

        # Remove other potentially dangerous patterns
        dangerous_patterns = [
            r'eval\s*\(',
            r'expression\s*\(',
            r'alert\s*\(',
            r'document\.cookie',
            r'document\.location',
        ]

        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)

        return sanitized.strip()

    @staticmethod
    def validate_todo_input(todo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize todo input data.
        """
        validated_data = {}

        # Validate and sanitize title
        if 'title' in todo_data:
            title = todo_data['title']
            if not isinstance(title, str) or len(title.strip()) == 0:
                raise ValueError("Title must be a non-empty string")
            if len(title) > 500:
                raise ValueError("Title must be 500 characters or less")

            validated_data['title'] = SecurityValidator.sanitize_input(title)

        # Validate and sanitize description
        if 'description' in todo_data:
            description = todo_data['description']
            if description is not None:
                if not isinstance(description, str):
                    raise ValueError("Description must be a string")
                if len(description) > 1000:
                    raise ValueError("Description must be 1000 characters or less")

                validated_data['description'] = SecurityValidator.sanitize_input(description)

        # Validate due date format
        if 'due_date' in todo_data and todo_data['due_date']:
            due_date = todo_data['due_date']
            if not isinstance(due_date, str):
                raise ValueError("Due date must be a string")
            # Basic ISO format validation (YYYY-MM-DD)
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', due_date):
                raise ValueError("Due date must be in YYYY-MM-DD format")

            validated_data['due_date'] = due_date

        # Validate priority
        if 'priority' in todo_data and todo_data['priority']:
            priority = todo_data['priority']
            if priority not in ['low', 'medium', 'high']:
                raise ValueError("Priority must be 'low', 'medium', or 'high'")
            validated_data['priority'] = priority

        # Validate category
        if 'category' in todo_data and todo_data['category']:
            category = todo_data['category']
            if not isinstance(category, str):
                raise ValueError("Category must be a string")
            if len(category) > 50:
                raise ValueError("Category must be 50 characters or less")

            validated_data['category'] = SecurityValidator.sanitize_input(category)

        return validated_data

    @staticmethod
    def validate_session_input(session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize session input data.
        """
        validated_data = {}

        if 'user_id' in session_data:
            user_id = session_data['user_id']
            if user_id is not None:
                if not isinstance(user_id, str):
                    raise ValueError("User ID must be a string")
                if len(user_id) > 100:
                    raise ValueError("User ID must be 100 characters or less")

                validated_data['user_id'] = SecurityValidator.sanitize_input(user_id)

        # Validate preferences if provided
        if 'preferences' in session_data and session_data['preferences']:
            preferences = session_data['preferences']
            if not isinstance(preferences, dict):
                raise ValueError("Preferences must be a dictionary")

            validated_preferences = {}
            if 'default_priority' in preferences:
                priority = preferences['default_priority']
                if priority not in ['low', 'medium', 'high']:
                    raise ValueError("Default priority must be 'low', 'medium', or 'high'")
                validated_preferences['default_priority'] = priority

            if 'default_category' in preferences:
                category = preferences['default_category']
                if category is not None:
                    if not isinstance(category, str):
                        raise ValueError("Default category must be a string")
                    if len(category) > 50:
                        raise ValueError("Default category must be 50 characters or less")
                    validated_preferences['default_category'] = SecurityValidator.sanitize_input(category)

            validated_data['preferences'] = validated_preferences

        return validated_data

    @staticmethod
    def is_valid_uuid(uuid_string: str) -> bool:
        """
        Validate UUID format.
        """
        import uuid
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False


def get_security_headers() -> Dict[str, str]:
    """
    Get recommended security headers.
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    }


# Global security validator instance
security_validator = SecurityValidator()