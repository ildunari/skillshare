---
name: hermes-subagent-ui-polish
description: Spawn a UI polish/design critique delegate for product surfaces, screenshots,
  CSS/SwiftUI/layout, and copy fit.
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

# hermes-subagent-ui-polish

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `ui_polish` delegate instead of doing all UI polish/design review work in the main context.

## When to use
Use for screenshots, web/app UI passes, Telegram message formatting, dashboards, onboarding, and “make it feel less janky” tasks.

## Recommended delegate_task toolsets
- Primary: `['vision', 'file']`
- Optional: add `browser` for web UIs; add `terminal` for local previews.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Review the UI for practical polish: hierarchy, spacing, alignment, contrast, state clarity, copy, responsiveness, and implementation cost. Give prioritized fixes and, if asked, make small targeted edits.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['vision', 'file']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Confirm before large visual redesigns or asset replacement. Avoid accessibility regressions; preserve product intent.

## Pitfalls
Vague taste comments; over-redesigning; ignoring dark mode/responsive states; using tables in Telegram when plain text is better.
