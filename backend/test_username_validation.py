#!/usr/bin/env python3
"""Test script to verify username validation works correctly with spaces."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.user import UserCreateRequest

def test_username_validation():
    """Test that username validation works correctly."""
    print("Testing username validation...")

    # Test cases
    test_cases = [
        ("zain khan", True, "Username with spaces"),
        ("zain", True, "Simple username"),
        ("zain_khan", True, "Username with underscore"),
        ("zain-khan", True, "Username with hyphen"),
        ("zain khan ", True, "Username with trailing space (should be stripped)"),
        (" zain khan", True, "Username with leading space (should be stripped)"),
        ("zain  khan", True, "Username with double space"),
        ("z k", True, "Short username with space"),
        ("", False, "Empty username"),
        ("z", False, "Too short"),
        ("a", False, "Single character"),
        ("ab", False, "Two characters"),
        ("za/in", False, "Username with invalid character"),
        ("zain@khan", False, "Username with @ symbol"),
    ]

    for username, should_pass, description in test_cases:
        try:
            # Create a UserCreateRequest instance
            user_req = UserCreateRequest(
                username=username,
                email="test@example.com",
                password="password123"
            )

            # Check if it passes validation
            if should_pass:
                print(f"[PASS] {description} - '{user_req.username}'")
            else:
                print(f"[FAIL] {description} - '{username}' should have failed validation but passed")

        except ValueError as e:
            if not should_pass:
                print(f"[PASS] {description} - '{username}' correctly failed: {e}")
            else:
                print(f"[FAIL] {description} - '{username}' should have passed but failed: {e}")
        except Exception as e:
            print(f"[ERROR] {description} - Unexpected error with '{username}': {e}")

if __name__ == "__main__":
    test_username_validation()