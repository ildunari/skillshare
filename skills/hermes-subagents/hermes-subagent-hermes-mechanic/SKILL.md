---
name: hermes-subagent-hermes-mechanic
description: Spawn a Hermes-internals delegate for config, gateway, skills, profiles,
  logs, and repo troubleshooting.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - hermes
    - subagent
    - delegation
    - template
targets:
- hermes-default
- hermes-gpt
---

# hermes-subagent-hermes-mechanic

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `hermes_mechanic` delegate instead of doing all Hermes maintenance/internals work in the main context.

## When to use
Use for Hermes gateway issues, skill creation, profile config, toolsets, updates, logs, cron, Telegram/Discord behavior, or local repo patches.

## Recommended delegate_task toolsets
- Primary: `['terminal', 'file', 'skills']`
- Optional: add `web` for upstream docs/issues.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Diagnose or modify Hermes carefully. Read relevant config/logs/code first, preserve Kosta’s local customizations, avoid unrelated files, and report commands, files, and verification.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['terminal', 'file', 'skills']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Do not start duplicate gateway instances. Confirm before credential/auth changes, destructive cleanup, broad updates, or sync-affecting deletes. Never expose secrets.

## Pitfalls
Forgetting profile paths; editing upstream clone when profile skill is intended; skipping logs; running evals/tests when explicitly told not to.
