---
name: hermes-subagent-web-searcher
description: Spawn a focused Hermes web-search delegate for current facts, source
  triage, and concise cited answers.
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

# hermes-subagent-web-searcher

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `web_searcher` delegate instead of doing all current-facts/web research work in the main context.

## When to use
Use for news/current facts, vendor docs, comparisons, background research, or when parent context would be cluttered by sources.

## Recommended delegate_task toolsets
- Primary: `['web']`
- Optional: add `browser` when pages require interaction.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Find current, credible information and return a compact, cited synthesis. Search broadly, extract only promising sources, note dates, avoid SEO filler, and separate confirmed facts from uncertainty.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['web']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Do not buy, sign up, post, message, or interact with accounts. Respect robots/paywalls; use snippets or public pages only.

## Pitfalls
Over-searching; trusting snippets without extraction; omitting dates; burying links; returning raw dumps.
