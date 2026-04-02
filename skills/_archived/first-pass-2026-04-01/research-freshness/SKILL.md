---
name: research-freshness
description: Use when implementing or debugging anything that depends on external APIs/SDKs/tools and must be current (docs, flags, breaking changes, migrations).
---

Treat this as the “you don’t get to guess” workflow.

## When to invoke

Invoke this skill any time you are about to:
- write code that calls an external API or SDK,
- change build tooling, CLIs, or deployment scripts,
- migrate versions,
- rely on a flag, config key, or command you are not 100% certain is current.

## Tool stack (in order)

1) First-party web search
Use it first for “what changed recently” and broad recall. Search is enabled by default; keep it cached unless you explicitly need live.

2) Context7
Use it for exact API signatures and versioned docs pages. Prefer official vendor docs and release notes.

3) Exa
Use it as a quality override when first-party results are noisy or incomplete. Bias toward official docs, GitHub releases, and primary sources.

4) Firecrawl
Use it only when you must extract content from JS-heavy sites, long pages, or paywalls that prevent normal extraction. Extract the smallest relevant section.

## Anti-hallucination rules

- If you cannot verify a symbol/flag/endpoint from docs or real examples, do not use it.
- Prefer “show me the exact snippet / version line” over paraphrase.
- Confirm versions explicitly (package.json, lockfile, --version output, release note date).

## Output requirements (“freshness receipts”)

At the end of the task report, include a short section (2–3 sources is enough):

Freshness receipts:
- Source: <doc URL or release note>  Version/date: <…>  Notes: <1 line>
- Source: <…>

Keep code comments minimal. Put the receipts in the report unless a call site is genuinely non-obvious.
