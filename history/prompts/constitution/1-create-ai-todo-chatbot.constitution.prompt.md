---
id: 1
title: Create AI Todo Chatbot Constitution
stage: constitution
date_iso: 2026-01-20
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: sp.implement
labels:
  - constitution
  - ai-chatbot
  - todo-app
  - governance
link_spec: null
link_ticket: null
link_adr: null
link_pr: null
files_yaml:
  - .specify/memory/constitution.md
  - history/prompts/constitution/1-create-ai-todo-chatbot.constitution.prompt.md
tests_yaml: []
---

# Create AI-Powered Todo Chatbot Constitution

## User Input

```
You are an expert AI software architect.

Create a constitution for an AI-Powered Todo Chatbot built using OpenAI ChatKit, OpenAI Agents SDK, and the Official MCP SDK.

The constitution must define:
- Project goals and scope
- Core user principles (simplicity, clarity, responsiveness)
- AI behavior rules (helpful, concise, safe, deterministic where needed)
- Data handling rules (in-memory only, no permanent storage unless explicitly stated)
- Security and privacy constraints
- Technology constraints (Next.js frontend, FastAPI/Python backend if needed, OpenAI SDKs only)
- Non-goals and limitations

Keep the constitution clear, concise, and enforceable for downstream planning and implementation.
```

## Response Summary

Created a comprehensive constitution document for the AI-Powered Todo Chatbot that addresses all the required elements:

1. Core Principles including user-centric simplicity, AI responsiveness, privacy-first data handling, secure interaction model, deterministic operations, and minimalist architecture
2. Technology stack requirements specifying Next.js, FastAPI, OpenAI ChatKit, OpenAI Agents SDK, and MCP SDK
3. Data handling policies emphasizing in-memory storage by default
4. Security and privacy requirements covering API security, user privacy, and session management
5. AI behavior guidelines for helpful, safe, and deterministic interactions
6. Non-goals and limitations clearly defining out-of-scope features
7. Development standards for code quality, testing, and performance

The constitution serves as the authoritative guide for all future development decisions and ensures alignment with the project's core values and technical requirements.

## Outcome

Successfully created a comprehensive constitution document that defines the governance, principles, and constraints for the AI-Powered Todo Chatbot project. The constitution is stored at `.specify/memory/constitution.md` and will serve as the foundational document for all future development activities.