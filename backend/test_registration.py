#!/usr/bin/env python3
"""Test script to verify user registration works with Neon database."""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.user import UserCreateRequest
from src.services.user_service import UserService
from src.utils.auth import get_password_hash

def test_user_registration():
    """Test that user registration works with Neon database."""
    print("Testing user registration with Neon database...")

    # Create database session
    db: Session = SessionLocal()

    try:
        user_service = UserService()

        # Test creating a user with spaces in the username
        user_data = UserCreateRequest(
            username="zain khan",
            email="zain.test@2026.com",  # Using a unique email for test
            password="securepassword123"
        )

        print(f"Attempting to create user: {user_data.username}")
        print(f"Email: {user_data.email}")

        # Check if user already exists
        existing_user = user_service.get_user_by_username(db, user_data.username)
        if existing_user:
            print(f"User with username '{user_data.username}' already exists. Trying with different username...")

            # Try a different test username
            user_data.username = "zain khan test"
            user_data.email = "zain.khan.test@2026.com"
            print(f"Trying with new username: {user_data.username}")

        # Create the new user
        db_user = user_service.create_user(db, user_data)

        print(f"User created successfully!")
        print(f"  ID: {db_user.id}")
        print(f"  Username: {db_user.username}")
        print(f"  Email: {db_user.email}")
        print(f"  Created at: {db_user.created_at}")

        # Try to retrieve the user
        retrieved_user = user_service.get_user_by_username(db, user_data.username)
        if retrieved_user:
            print(f"User successfully retrieved from database!")
            print(f"  Retrieved ID: {retrieved_user.id}")
            print(f"  Retrieved Username: {retrieved_user.username}")
        else:
            print("ERROR: Could not retrieve user from database after creation!")

        # Clean up - delete test user (optional)
        # Uncomment the next lines if you want to remove the test user
        # db.delete(retrieved_user)
        # db.commit()
        # print("Test user deleted.")

        return True

    except Exception as e:
        print(f"ERROR during user registration test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_user_registration()
    if success:
        print("\n[SUCCESS] User registration test completed successfully!")
    else:
        print("\n[FAILURE] User registration test failed!")
        sys.exit(1)