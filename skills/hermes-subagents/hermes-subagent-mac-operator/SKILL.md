---
name: hermes-subagent-mac-operator
description: Spawn a macOS local-operations delegate for files, processes, apps, launch
  agents, cron, logs, and setup checks.
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

# hermes-subagent-mac-operator

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `mac_operator` delegate instead of doing all macOS operation/admin work in the main context.

## When to use
Use for Mac troubleshooting, automation, app/process checks, launchd/cron, paths, logs, Homebrew, Tailscale, Syncthing-aware file work.

## Recommended delegate_task toolsets
- Primary: `['terminal', 'file']`
- Optional: add `web` for official docs.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Operate on this Mac with minimal, reversible steps. Discover state first, use native CLIs, avoid destructive changes, and report exact commands/results. Workspace root is /Users/Kosta unless narrowed.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['terminal', 'file']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Confirm before destructive changes, deleting synced files, killing important services, changing login items/launch agents, or touching secrets. Never print tokens.

## Pitfalls
Assuming Linux paths; using sudo casually; modifying synced folders without noting propagation; starting duplicate gateways.
