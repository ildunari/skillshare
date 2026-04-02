---
name: docs-freshness-verifier
description: Use when implementation depends on external APIs, SDKs, tools, or flags and you need current, source-backed verification before coding.
---

# Docs Freshness Verifier

## Overview
Prevents stale implementation by forcing current-doc verification and source receipts.

## Human Detail Standard
- Verify every critical symbol/flag against primary docs, not memory.
- If evidence is weak, slow down and verify before concluding.

## When to Use
Use when:
- External API/SDK behavior matters.
- You are changing versions, flags, or deployment/build commands.

## Skill Activation Order
- Load `research-freshness` as the base protocol.
- Load `openai-docs` for OpenAI API/SDK questions before broad web search.
- Load `mcp-operations` if MCP docs/search tooling is misconfigured or failing.

## Required Research Order
1. Native web search (`search_query`) for recency and broad signal.
2. Official docs/tools (e.g., Context7/OpenAI docs MCP).
3. Firecrawl only for extraction-heavy or JS-heavy pages.

## Required Behavior
- Confirm exact symbol/flag availability from current docs.
- Record versions/dates from authoritative sources.
- Refuse to invent unverified APIs/options.

## Output Contract
- Freshness receipts with URL + version/date + one-line note.
- Any conflicts or uncertainty explicitly listed.

## Good vs Bad
Good:
- Verifies exact signatures and dates.
- Cites primary sources.

Bad:
- Relies on memory for unstable APIs.
- Uses secondary blog claims without vendor confirmation.

## Test Cases
- Verify new SDK method exists before use.
- Confirm CLI flag deprecation and replacement.
