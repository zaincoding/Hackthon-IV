#!/usr/bin/env python3
"""Initialize the database tables in the PostgreSQL database."""

import sys
import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(__file__))

from src.models.database import create_tables, engine
from src.config.settings import settings

def init_database():
    """Initialize the database by creating all tables."""
    print(f"Initializing database with URL: {settings.DATABASE_URL}")

    try:
        # Create all tables
        create_tables()
        print("Database tables created successfully!")

        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection test successful!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

    return True

if __name__ == "__main__":
    success = init_database()
    if success:
        print("Database initialization completed successfully!")
    else:
        print("Database initialization failed!")
        sys.exit(1)