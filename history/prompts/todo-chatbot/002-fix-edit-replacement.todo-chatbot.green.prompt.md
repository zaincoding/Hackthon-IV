---
id: "002"
title: "fix-edit-replacement"
stage: "green"
date_iso: "2026-01-22"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-chatbot"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["enhancement", "edit", "replacement", "ai-service"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/services/ai_service.py"
tests_yaml: []
---

# Prompt

```
edit buy to sell
    10:33 PM
    I found multiple todos matching 'buy'. Please respond with the number of your choice:
    1. i buy two apple
    2. i will buy two mangoes

    For example, respond with '1' or '2' to select the corresponding todo.
    10:33 PM      there is an issue when i edite one word such as buy to sell it replace the whole sentence
    with a single word sell so it is not working like manual editing where you can edit a single word
    without replacing the whole sentence so try to solve this issue
```

# Response

Fixed the todo editing functionality so that when a user says "edit [word] to [new_word]", it replaces only the specified word in the todo title instead of replacing the entire title.

Changes made:
1. Modified the AI service to perform word-level replacement using regex instead of full title replacement
2. Updated the logic to find the target word in the original title and replace it with the new word
3. Updated the context handling for multiple todo matches to show the preview of the updated title
4. Fixed the number selection flow to use the pre-calculated updated title

The edit functionality now works as expected - when a user says "edit buy to sell" on a todo titled "i buy two apples", it will update the title to "i sell two apples" instead of just "sell".

# Outcome

The word replacement functionality now works correctly, allowing users to replace specific words in todo titles rather than replacing the entire title.

# Evaluation

The fix was successful - users can now perform partial text replacements in todo titles, making the editing experience more intuitive and aligned with manual editing expectations.