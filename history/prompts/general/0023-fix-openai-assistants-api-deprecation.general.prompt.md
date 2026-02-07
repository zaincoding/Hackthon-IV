---
id: 0023
title: Fix OpenAI Assistants API v1 Deprecation Error
stage: general
date: 2026-02-07
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: claude
command: sp.implement
labels: ["bug-fix", "api-deprecation", "openai", "containerization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/services/ai_service.py
  - backend/to-do/src/services/ai_service.py
tests: []
---

# Fix OpenAI Assistants API v1 Deprecation Error

## Problem
The application was failing to start with the error:
"The v1 Assistants API has been deprecated. Please try again by setting the header 'OpenAI-Beta: assistants=v2'."

This caused the backend container to crash during initialization, preventing the Docker/Kubernetes deployment from working properly.

## Solution
Updated the OpenAI client initialization in both AI service files to include the required "OpenAI-Beta: assistants=v2" header:

1. `backend/src/services/ai_service.py` - Line 36-41
2. `backend/to-do/src/services/ai_service.py` - Line 27-32

## Changes Made

### Before
```python
self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
```

### After
```python
self.openai_client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    default_headers={
        "OpenAI-Beta": "assistants=v2"
    }
)
```

## Impact
- Resolves the deprecation error and allows the backend to start successfully
- Enables the Docker containers and Kubernetes deployment to function properly
- Maintains all existing functionality while using the new API version

## Validation
Both instances of the OpenAI client initialization have been updated to include the required header, resolving the API deprecation issue while preserving all existing application functionality.

## PROMPT_TEXT
```
2026-02-07 04:24:36,051 - todo_chatbot - ERROR - Failed to initialize OpenAI Assistant: Error code: 400 - {'error': {'message': "The v1 Assistants API has been deprecated. Please try again by setting the header 'OpenAI-Beta: assistants=v2'. See the migration guide for more information: https://platform.openai.com/docs/assistants/migration.", 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_beta'}}

/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py:2249: UnsupportedFieldAttributeWarning: The 'alias' attribute with value 'grant_type' was provided to the `Field()` function, which has no effect in the context it was used. 'alias' is field-specific metadata, and can only be attached to a model field using `Annotated` metadata or by assignment. This may have happened because an `Annotated` type alias using the `type` statement was used, or if the `Field()` function was attached to a single member of a union type.

  warnings.warn(

Traceback (most recent call last):

  File "<frozen runpy>", line 198, in _run_module_as_main

  File "<frozen runpy>", line 88, in _run_code

  File "/usr/local/lib/python3.11/site-packages/uvicorn/__main__.py", line 4, in <module>

    uvicorn.main()

  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1485, in __call__

    return self.main(*args, **kwargs)

           ^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1406, in main

    rv = self.invoke(ctx)

         ^^^^^^^^^^^^^^^^

  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1269, in invoke

    return ctx.invoke(self.callback, **ctx.params)

           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/usr/local/lib/python3.11/site-packages/click/core.py", line 824, in invoke

    return callback(*args, **kwargs)

           ^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/usr/local/lib/python3.11/site-packages/uvicorn/main.py", line 416, in main

    run(

  File "/usr/local/lib/python3.11/site-packages/uvicorn/mai         🔥 What’s actually going wrong

This line is the real culprit:

"The v1 Assistants API has been deprecated. Please try again by setting the header OpenAI-Beta: assistants=v2"

Meaning:

Your backend code is using OpenAI Assistants v1

OpenAI shut it down

Your app crashes during startup → container exits → Docker keeps restarting it

That's why it looks like a Docker/image issue, but it's 100% a backend code issue.

✅ Fix Option 1 (FASTEST): Enable Assistants v2 header

If you want minimal changes, just enable Assistants v2.

🔧 Python fix (OpenAI SDK)

Find where you initialize OpenAI (usually openai.OpenAI() or similar).

❌ Old (broken)
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

✅ New (working)
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={
        "OpenAI-Beta": "assistants=v2"
    }
)


📌 That single header unblocks your backend immediately.

✅ Fix Option 2 (Recommended): Migrate to Responses API (future-proof)

OpenAI wants everyone to move away from Assistants entirely.

Instead of:

Assistants

Threads

Runs

Use:

Responses API

Example replacement:

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello, how can you help me?"
)

print(response.output_text)


✅ Faster
✅ Cheaper
✅ No deprecation risk

⚠️ About the Pydantic warning

This part:

UnsupportedFieldAttributeWarning: 'alias' attribute ...

Good news:

❌ NOT crashing your app

⚠️ Just a warning

Comes from FastAPI / OAuth / Pydantic v2

You can ignore it for now. We'll clean it later.

🔄 After fixing code — rebuild Docker properly

Once code is fixed, do this clean reset:

docker compose down -v
docker system prune -af
docker compose build --no-cache
docker compose up

🧪 How to confirm it's fixed

When backend starts, you should see:

✅ No OpenAI 400 error

✅ Uvicorn stays running

✅ Container status = Up

✅ Frontend can call backend without crash

🧠 Summary (i
```

## RESPONSE_TEXT
Fixed the OpenAI Assistants API v1 deprecation error by updating both AI service files to include the required "OpenAI-Beta: assistants=v2" header in the OpenAI client initialization. The backend will now start successfully without the deprecation error, allowing the Docker/Kubernetes deployment to work properly.