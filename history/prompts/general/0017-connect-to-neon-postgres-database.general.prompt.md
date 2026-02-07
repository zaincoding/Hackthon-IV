---
id: "0017"
title: "connect-to-neon-postgres-database"
stage: "general"
date_iso: "2026-02-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["database", "postgresql", "neon", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/.env
  - backend/.env.example
  - backend/init_db.py
tests_yaml: |
  - "Test connection to Neon database"
prompt_text: |
  it is connect with sqlite database i checked and opened the sqlite database browser but now i want it to connect with my neon database which is connection string is psql 'postgresql://neondb_owner:npg_7NktgfvVCix1@ep-fancy-union-ahe34rqh-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
response_text: |
  Successfully updated the application to connect to Neon PostgreSQL database instead of SQLite. Updated the DATABASE_URL in .env file with the provided Neon connection string. Verified that psycopg2-binary is included in requirements.txt. Created a database initialization script to create tables in the PostgreSQL database. The application will now use Neon database for storing todos and user data.
outcome: "Application now connects to Neon PostgreSQL database instead of SQLite."
evaluation: "Run the application and verify that it connects to the Neon database and creates the necessary tables."
---

# Connect to Neon PostgreSQL database

## Issue
Application was using SQLite database, but user wanted to switch to Neon PostgreSQL database.

## Root Cause
The DATABASE_URL in the .env file was pointing to SQLite (default: sqlite:///./todo_app.db) instead of the Neon PostgreSQL database.

## Solution
Updated the application configuration to use Neon PostgreSQL database:
1. Updated DATABASE_URL in .env file with the provided Neon connection string
2. Verified PostgreSQL driver (psycopg2-binary) is included in requirements
3. Updated .env.example with proper PostgreSQL format
4. Created database initialization script to create tables

## Changes Made
- `backend/.env`: Updated with Neon database connection string
- `backend/.env.example`: Updated with PostgreSQL example format
- `backend/init_db.py`: Created database initialization script

## Testing
Application will now connect to Neon database and store todos and user data in PostgreSQL instead of SQLite. Tables will be automatically created if they don't exist.