---
name: hermes-subagent-product-finder
description: Spawn a shopping/product research delegate for buying options, pricing,
  availability, and tradeoffs.
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

# hermes-subagent-product-finder

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `product_finder` delegate instead of doing all product search/buying research work in the main context.

## When to use
Use for hardware, lab gear, accessories, software services, replacements, or “which should I buy?” tasks.

## Recommended delegate_task toolsets
- Primary: `['web', 'browser']`
- Optional: add `terminal` only for parsing saved comparison data.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Find the best product options for Kosta given constraints. Compare price, availability, specs, shipping/returns, reputable reviews, and known failure modes. Prefer direct vendor/manufacturer pages and credible reviews.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['web', 'browser']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Never purchase, add payment info, log into stores, or contact sellers without explicit parent/user confirmation. Flag affiliate/SEO uncertainty.

## Pitfalls
Optimizing only price; ignoring compatibility; using stale stock; trusting Amazon titles/specs; missing return policy.
