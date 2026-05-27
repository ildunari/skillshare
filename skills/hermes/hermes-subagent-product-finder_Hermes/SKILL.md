---
name: hermes-subagent-product-finder_Hermes
description: Spawn a shopping/product research delegate for buying options, pricing,
  availability, and tradeoffs.
version: 0.2.0
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
# hermes-subagent-product-finder

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `product_finder` delegate instead of doing all product search/buying research work in the main context.

## When to use
Use for hardware, lab gear, accessories, software services, replacements, or “which should I buy?” tasks.

Use `web-searcher` instead when the job is mostly general current-facts research. Use `product-finder` when the output needs a buying decision, ranked recommendations, pricing, availability, compatibility, or tradeoffs.

## Research strategy

Search iteratively:

1. Map the category broadly: current product names, official specs, major vendors, known alternatives.
2. Verify candidate details directly: manufacturer pages, docs, pricing pages, stock pages, changelogs, warranties/returns.
3. Check real-user signal: Reddit/niche forums, HN, X/Twitter, GitHub issues for software tools, YouTube/comments if useful.
4. Look for underdogs and contrarian picks; do not rank only by popularity or SEO visibility.
5. Separate gaps from negatives: say whether you found no evidence, or sources actively confirm absence/unavailability.

For software tools/repos, include GitHub stars, last commit date, open issues count, release cadence, license, and a maintenance-status read. For physical products, include current price, seller/vendor, stock/availability, shipping/return caveats, compatibility constraints, and common failure modes.

Source priority: official/manufacturer pages, vendor pages with live pricing, GitHub/changelogs/docs, reputable reviews with measurements, real-user community reports, then generic roundups. Flag affiliate/SEO uncertainty.

## Recommended delegate_task toolsets
- Primary: `['web', 'browser']`
- Optional: add `terminal` only for parsing saved comparison data.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Lane: product-finder. Find the best product/tool options for Kosta given constraints. Search iteratively: broad category map, targeted candidate verification, then real-user/community checks. Compare price, availability, specs, compatibility, shipping/returns, reputable reviews, known failure modes, and maintenance status for software/repos. Prefer direct vendor/manufacturer pages, GitHub/docs/changelogs, credible reviews, and real-user reports. Rank by fit/quality, not popularity, and include a credible underdog if one exists.",
    context="""
Lane: product-finder
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
1. **Answer/result** — direct recommendation or completed research.
2. **Evidence/actions** — links, route/tool used, prices/specs/dates, repo health if applicable, or UI steps.
3. **Ranked recommendations** — best overall, best value, best fit for the stated constraints, and one credible underdog when available.
4. **Known limitations/risks** — compatibility, stale stock/pricing, maintenance concerns, reviews that look affiliate/SEO-driven.
5. **Issues/blockers** — uncertainty, missing access, exhausted search paths, or confirmation needed.

## Safety/confirmation rules
Never purchase, add payment info, log into stores, or contact sellers without explicit parent/user confirmation. Flag affiliate/SEO uncertainty.

## Pitfalls
Optimizing only price; ignoring compatibility; using stale stock; trusting Amazon titles/specs; missing return policy.
