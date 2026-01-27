---
id: 1
title: add-title-and-description-support
stage: general
date: 2026-01-23
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.implement i don't know how the ai chat bot work it only add description not title i don't know how to instruct to the ai chatbot assistance to add title and description both with the same instruction?
labels: [ai, chatbot, nlp, enhancement]
links: {spec: null, ticket: null, adr: null, pr: null}
files:
  - backend/src/services/ai_service.py
  - HOW_TO_USE_TITLE_DESCRIPTION.md
tests: []
---

# Add Title and Description Support to AI Chatbot

## User Request
User wanted to know how to instruct the AI chatbot to add both title and description with the same instruction, as it was only adding description before.

## Analysis
After examining the codebase, I found that the AI chatbot already supported both title and description, but the regex patterns weren't prioritized correctly for extracting both fields from a single command. The system was working but not optimally handling natural language commands that included both title and description.

## Changes Made

### 1. Updated Regex Patterns in `backend/src/services/ai_service.py`
- Reordered the `add_todo` patterns to prioritize those that capture both title and description
- The patterns `"add\s+(.+?)\s+with\s+description\s+(.+)"` and `"add\s+(.+?)\s+and\s+description\s+(.+)"` now have higher priority
- Added enhanced fallback logic to extract title and description from the original input string

### 2. Enhanced OpenAI Assistant Instructions
- Updated the assistant instructions to specifically mention handling both title and description
- Added explicit examples for the supported formats

### 3. Improved Response Formatting
- Updated the response to display both title and description when available
- Changed from checking entities to checking the actual todo data for description display

## Usage Examples
Users can now use these formats:
- `add grocery shopping with description buy milk, bread, and eggs`
- `add workout routine and description 30 minutes cardio and strength training`

## Outcome
The AI chatbot now properly handles commands that include both title and description in a single instruction. The system maintains backward compatibility with existing commands while adding enhanced support for dual-field input.

## Files Modified
- `backend/src/services/ai_service.py` - Updated patterns, instructions, and response formatting
- `HOW_TO_USE_TITLE_DESCRIPTION.md` - Documentation for the new functionality