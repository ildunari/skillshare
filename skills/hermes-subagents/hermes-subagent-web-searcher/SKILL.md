---
name: hermes-subagent-web-searcher
description: Spawn a focused Hermes web-search delegate for current facts, source
  triage, and concise cited answers.
version: 0.3.0
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

## When to use — and when not to
Use for: news/current facts, vendor docs, comparisons, background research, or when parent context would be cluttered by sources.

**Skip delegation when:**
- The answer is already in the parent context or conversation history.
- The query is a stable fact answerable from training (definitions, syntax, well-known specs).
- Search overhead exceeds value (e.g. "what HTTP status code is 404?").

## Prerequisite checks
Before spawning, verify in order:
1. `delegate_task` is callable in this session — if not, search directly with available web tools.
2. The required toolset is accessible (`'web'` minimum). If a specific toolset like `'browser'` is unavailable, fall back to `'web'` only and note the gap in the result.
3. If no web tools are available at all, tell Kosta: "⚠️ Falling back to training-data knowledge (no live web access) — treat this as potentially stale."

## Toolset selection

Pick the minimum set. Decide before spawning — don't give `browser` or `terminal` speculatively.

| Condition | Add |
|-----------|-----|
| Default | `['web']` |
| Page requires login or JS rendering | `'browser'` |
| Delegate must read/write local files | `'file'` |
| `curl`/`jq` or shell verification needed | `'terminal'` |
| Task needs Hermes CLI operations | `'hermes-cli'` (rare) |

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Find current, credible information and return a compact, cited synthesis. Search broadly, extract only promising sources, note dates, avoid SEO filler, and separate confirmed facts from uncertainty. If you hit a dead end, note what you tried.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <specific artifact — e.g. "current version number of X", "comparison of A vs B on metric M", "direct download URL for Y", "release date confirmed from official source">
Recency requirement: <e.g. "must be from the past 7 days" | "within past 6 months is fine" | "stable fact, recency not critical">
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['web']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links with dates. Minimum 2 independent sources for factual claims; 1 authoritative source is acceptable for niche or emerging topics with low coverage (flag this case explicitly).
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Parent-side output verification
After receiving the delegate result, auto-check before accepting:
- Answer section is non-empty and directly addresses the ask.
- At least one dated source or link is present (no floating facts).
- Recency: verify against the DoD field's stated `Recency requirement`, not a fixed threshold — requirements vary (live prices/APIs: hours; library versions: days–weeks; background research: months).
- Uncertainty is labeled; confirmed facts are separated from guesses.

If checks fail: re-spawn **once** with a narrower goal. Narrow by one of: (a) scope to a single specific artifact ("just the current semver, not the changelog"), (b) anchor with a known-good source URL (`site:docs.example.com`), or (c) switch from broad keywords to an exact quoted phrase. If the second attempt also fails, return the best partial result to the user with explicit gaps noted — do not silently synthesize from incomplete evidence.

## Failure recovery (no user prompt needed)
- **Empty/stub result**: retry once with a specific artifact and at least one example source URL.
- **All sources paywalled**: return best public snippets with dates; note paywall clearly. Do not retry behind paywall.
- **Timeout/error**: report failure and any partial context captured. Do not swallow silently.
- **Second retry fails**: escalate to Kosta with what was tried and what is missing.

## Safety/confirmation rules
Do not buy, sign up, post, message, or interact with accounts. Respect robots/paywalls; use snippets or public pages only. No confirmation needed for read-only searches.

## Pitfalls
Over-searching; trusting snippets without extraction; omitting dates; burying links; returning raw dumps; silently swallowing delegate errors.
