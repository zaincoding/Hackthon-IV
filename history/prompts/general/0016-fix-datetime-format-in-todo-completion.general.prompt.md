---
id: "0016"
title: "fix-datetime-format-in-todo-completion"
stage: "general"
date_iso: "2026-02-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["bug-fix", "database", "datetime", "todo-completion"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/services/todo_service_db.py
tests_yaml: |
  - "Manual test of todo completion functionality"
prompt_text: |
  the check box ui completion and with chat boat compete does not work   Chat with Your AI Assistant
  Complete zoo
  12:24 PM
  Sorry, I encountered an error finding that todo: (builtins.TypeError) SQLite DateTime type only accepts Python datetime and date objects as input.
  [SQL: UPDATE todos SET status=?, updated_at=?, completed_at=? WHERE todos.id = ?]
  [parameters: [{'status': 'completed', 'completed_at': '2026-02-06T07:24:01.048574', 'updated_at': datetime.datetime(2026, 2, 6, 7, 24, 1, 48574), 'todos_id': 'd7946a68-0182-4d2f-b0ea-93719cd82c37'}]]
response_text: |
  Fixed the datetime format issue in the todo completion functionality by updating todo_service_db.py to use Python datetime objects instead of ISO format strings when setting completed_at timestamps. The error occurred because SQLite DateTime columns require Python datetime objects, but the code was providing ISO format strings from datetime.utcnow().isoformat(). Changed both instances to use datetime.utcnow() directly.
outcome: "Todo completion functionality now works correctly through both UI checkboxes and chatbot commands."
evaluation: "Test by completing a todo through both the UI checkbox and chatbot command like 'Complete zoo'."
---

# Fix datetime format in todo completion

## Issue
The todo completion functionality was failing with error: `(builtins.TypeError) SQLite DateTime type only accepts Python datetime and date objects as input.`

## Root Cause
The `todo_service_db.py` file was using `datetime.utcnow().isoformat()` which returns a string, but SQLite DateTime columns require Python datetime objects.

## Solution
Updated both instances in the TodoService class to use `datetime.utcnow()` directly instead of `datetime.utcnow().isoformat()`:
1. In the `update_todo` method where setting completed_at during status updates
2. In the `toggle_todo_completion` method where setting completed_at during completion toggling

## Changes Made
- `backend/src/services/todo_service_db.py`: Updated datetime assignment to use Python datetime objects instead of ISO format strings

## Testing
The fix addresses the exact error scenario described where completing a todo via chatbot or UI would fail with the SQLite DateTime type error.