---
id: 0012
title: Fix Edit and Complete Todo Functionality in AI Service
stage: general
date: 2026-02-05
model: claude-sonnet-4-5-20250929
surface: agent
feature: none
branch: master
user: claude
command: sp.implement
labels: ["bug-fix", "ai-service", "nlp", "todo-functionality"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - backend/src/services/ai_service.py
  - history/prompts/general/0012-fix-edit-and-complete-todo-functionality-in-ai-service.general.prompt.md
tests_yaml:
  - edit todo functionality works with comma-separated input
  - complete todo functionality has improved title matching
  - delete todo functionality has improved title matching
outcome: Fixed AI service to properly handle edit and complete operations with enhanced NLP parsing and fuzzy matching
evaluation: Successfully resolved user-reported issue with edit and complete functionality
---

# Fix Edit and Complete Todo Functionality in AI Service

## User Input

```
now the chatboat is adding task and displaying it but it does not edite and complete the task
```

## Response Text

Fixed the AI service in backend/src/services/ai_service.py to properly handle edit and complete operations:

1. Improved the edit logic to handle comma-separated input like "edit fishing, to Boating" by properly parsing the target part and new value while stripping trailing commas
2. Enhanced the title matching algorithms for both complete and delete operations with more flexible matching that performs partial matches and word intersection checks
3. Applied fixes to both database-backed and session-based operations for consistent behavior across all user scenarios
4. Updated matching logic in four locations: complete user operation, complete session operation, delete user operation, and delete session operation

All changes significantly improve the natural language processing capabilities of the AI service, allowing users to more reliably edit, complete, and delete their todos using natural language commands.