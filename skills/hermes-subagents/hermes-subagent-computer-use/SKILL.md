---
name: hermes-subagent-computer-use
description: Spawn a browser/GUI computer-use delegate for interaction-heavy websites
  or visual UI tasks.
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
- claude-hermes
---

# hermes-subagent-computer-use

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `computer_use` delegate instead of doing all browser/GUI computer use work in the main context.

## When to use
Use when screenshots, dynamic web apps, forms, dashboards, or click paths matter more than pure search.

## Recommended delegate_task toolsets
- Primary: `['browser', 'vision', 'web']`
- Optional: add `file` only if saving screenshots/notes.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Use browser and vision tools to complete the specified UI task. Keep a step log, prefer read-only exploration first, and stop before irreversible actions. Return the final state and any blockers.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['browser', 'vision', 'web']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Do not submit purchases, legal/medical/financial forms, account changes, public posts, or messages without explicit confirmation. Do not enter secrets unless user has already authorized that exact site/action.

## Implementation/backend notes
When Kosta asks to add Codex/Operator-style computer use to Hermes without relying on Codex itself, prefer **Browser Use** (`browser-use/browser-use`) as the first backend to evaluate or wrap. It is Python-first, MIT-licensed, self-hostable, actively maintained, and fits Hermes better than TypeScript-first options. Treat Stagehand as the strongest runner-up for a Node sidecar; treat OpenHands and UI-TARS as heavier reference architectures for full desktop/sandboxed computer use rather than the initial browser-control layer.

The recommended Hermes shape is a sidecar/tool wrapper around Browser Use for high-level “do this website task” loops, while preserving Hermes’ existing CDP/browser tools for deterministic navigation, DOM inspection, screenshots, and low-level recovery.

## Pitfalls
Clicking before reading; losing state; solving via guesses; ignoring modals; failing to report exact blocker/screenshot context; embedding a full agent platform when a focused browser-control library is enough.
