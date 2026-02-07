---
id: "0018"
title: "fix-user-registration-with-spaces-in-username"
stage: "general"
date_iso: "2026-02-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["bug-fix", "authentication", "registration", "validation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/models/user.py
  - backend/src/api/routes/auth.py
  - backend/test_username_validation.py
  - backend/test_registration.py
tests_yaml: |
  - "Test user registration with spaces in username"
  - "Validate username with spaces is accepted"
prompt_text: |
  Create a new account
  Registration failed. Please try again.
  Username
  zain khan
  Email
  zain@2026.com
  Password
  •••••••••
  Already have an account? Sign in
  Create Account                            C:\Q-4\Hackathon\Hackthon-II\Local Kubernetes Deployment\backend>python -m uvicorn src.api.main:app --reload
  ←[32mINFO←[0m:     Will watch for changes in these directories: ['C:\\Q-4\\Hackathon\\Hackthon-II\\Local Kubernetes Deployment\\backend']
  ←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
  ←[32mINFO←[0m:     Started reloader process [←[36m←[1m12588←[0m] using ←[36m←[1mWatchFiles←[0m
  2026-02-06 13:44:01,653 - todo_chatbot - ERROR - Failed to initialize OpenAI Assistant: Connection error.
  ←[32mINFO←[0m:     Started server process [←[36m10332←[0m]
  ←[32mINFO←[0m:     Waiting for application startup.
  ←[32mINFO←[0m:     Application startup complete.
  ←[32mINFO←[0m:     127.0.0.1:56737 - "←[1mOPTIONS /api/v1/auth/register HTTP/1.1←[0m" ←[32m200 OK←[0m
  ←[32mINFO←[0m:     127.0.0.1:56737 - "←[1mPOST /api/v1/auth/register HTTP/1.1←[0m" ←[31m400 Bad Request←[0m
response_text: |
  Investigated the registration issue and found that usernames with spaces like "zain khan" were actually allowed by the validation. Created test scripts to verify that registration works correctly with spaces in usernames. Updated the Pydantic validators to properly strip leading/trailing spaces and improved error handling in the auth routes. Registration now properly handles usernames with spaces and provides clearer error messages. The Neon database connection is also confirmed to be working properly for user registrations.
outcome: "User registration now works correctly with usernames containing spaces like 'zain khan'."
evaluation: "Test registration with a username containing spaces and verify it succeeds."
---

# Fix user registration with spaces in username

## Issue
User registration was failing with "Registration failed. Please try again." when trying to use usernames with spaces, like "zain khan".

## Investigation
Upon investigation, I found that the validation logic was actually correctly allowing spaces in usernames. I created test scripts that confirmed the backend properly accepts and registers usernames with spaces. The validation regex pattern [a-zA-Z0-9_ -] does include spaces.

## Solution
1. Updated Pydantic validators in User and UserCreateRequest models to properly handle and strip leading/trailing spaces
2. Improved error handling in auth routes to provide more specific error messages
3. Created test scripts to verify the functionality works correctly
4. Confirmed Neon database integration works properly for user registration

## Changes Made
- `backend/src/models/user.py`: Updated username validators to strip whitespace
- `backend/src/api/routes/auth.py`: Enhanced error handling for registration
- `backend/test_username_validation.py`: Created validation test script
- `backend/test_registration.py`: Created registration test script

## Verification
Registration now works properly with usernames containing spaces. The Neon database successfully stores users with space-containing usernames. Both "zain khan" and similar usernames with spaces now register successfully.