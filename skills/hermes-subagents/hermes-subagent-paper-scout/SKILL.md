---
name: hermes-subagent-paper-scout
description: Spawn an academic literature scout for papers, methods, datasets, authors,
  and citation trails.
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

# hermes-subagent-paper-scout

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `paper_scout` delegate instead of doing all paper/literature scouting work in the main context.

## When to use
Use for nanomedicine/biomed background, related work, protocol/method lookup, or building a reading queue.

## Recommended delegate_task toolsets
- Primary: `['web']`
- Optional: add `terminal` for BibTeX/metadata parsing.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Scout the literature for the specified biomedical/technical question. Prioritize primary papers, reviews, preprints when appropriate, methods relevance, recency, and citation context. Return a short annotated reading list with DOIs/PMIDs/arXiv links.",
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
Do not claim full-text access unless verified. Respect paywalls. Distinguish peer-reviewed vs preprint. Do not give medical advice.

## Pitfalls
Listing papers without why they matter; confusing reviews with primary data; missing negative/older foundational work.
