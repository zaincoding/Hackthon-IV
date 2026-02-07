#!/usr/bin/env python3
"""Test script to check which database configuration is being used."""

import sys
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(__file__))

from src.config.settings import settings

def check_db_configuration():
    """Check which database configuration is being used."""
    print("Database Configuration Check:")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")

    if 'sqlite' in settings.DATABASE_URL.lower():
        print("Current configuration: SQLite database")
    elif 'postgresql' in settings.DATABASE_URL.lower() or 'neon' in settings.DATABASE_URL.lower():
        print("Current configuration: PostgreSQL/Neon database")
    else:
        print("Current configuration: Other database type")

    print("\nEnvironment variable check:")
    env_db_url = os.getenv('DATABASE_URL')
    print(f"Environment DATABASE_URL: {env_db_url}")

    if env_db_url and 'postgresql' in env_db_url.lower():
        print("✓ Environment has PostgreSQL/Neon URL")
    elif env_db_url and 'sqlite' in env_db_url.lower():
        print("⚠ Environment has SQLite URL")
    else:
        print("? Environment DATABASE_URL not set or unrecognized")

if __name__ == "__main__":
    check_db_configuration()