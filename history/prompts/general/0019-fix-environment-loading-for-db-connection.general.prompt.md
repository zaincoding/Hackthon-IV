---
id: "0019"
title: "fix-environment-loading-for-db-connection"
stage: "general"
date_iso: "2026-02-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["bug-fix", "configuration", "database", "environment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/api/main.py
tests_yaml: |
  - "Verify application uses Neon database when started with uvicorn"
prompt_text: |
  as you tested the registeration form it created the the user in database but when i tried to registeration form it create the user in sqldatabase (todo_app database file)
response_text: |
  Fixed the environment loading issue in the main application file. The application wasn't explicitly loading the .env file when started with uvicorn, which caused it to default to the SQLite database instead of the configured Neon PostgreSQL database. Added dotenv.load_dotenv() call to the main application file to ensure environment variables are loaded before creating the database connection.
outcome: "Application now correctly uses Neon PostgreSQL database when started with uvicorn."
evaluation: "Start the application with uvicorn and verify it connects to the Neon database instead of SQLite."
---

# Fix environment loading for database connection

## Issue
The application was connecting to SQLite database (todo_app.db) instead of the configured Neon PostgreSQL database when started via uvicorn, even though the .env file had the correct PostgreSQL URL.

## Root Cause
The main application file (src/api/main.py) wasn't explicitly loading the .env file, so when uvicorn started the application, it fell back to the default SQLite configuration defined in the Settings class.

## Solution
Added explicit environment loading using dotenv.load_dotenv() in the main application file to ensure environment variables are loaded before the database connection is established.

## Changes Made
- `backend/src/api/main.py`: Added dotenv import and load_dotenv() call to ensure .env file is loaded on application startup

## Verification
The application will now properly read the DATABASE_URL from the .env file and connect to the Neon PostgreSQL database instead of defaulting to SQLite when started with uvicorn.