---
name: web-research-orchestrator
description: Use when a query needs multi-step web research with citations, fast parallel workers, and iterative gap-closing without duplicate source checks.
---

# Web Research Orchestrator

## Overview
Run as a fast parent orchestrator on `gpt-5.3-codex (thinking: low)`.
Spawn `codex-spark` workers, collect evidence, close gaps round-by-round, and deliver source-backed conclusions.

## Human Detail Standard
- Do not gloss over uncertainty, conflicts, or missing evidence.
- Work like a careful analyst: check, re-check, and document why each conclusion is justified.
- If a step is skipped, explicitly state what was skipped and why.

## When to Use
Use when:
- The question needs current web information across multiple sources.
- You need citations and confidence tags.
- One-pass search is likely incomplete.

Do not use when:
- The user needs a quick single-source lookup.
- The task is local-only code work with no web dependency.

## Skill Activation Order
- Load `research-freshness` before first query to enforce recency and source quality checks.
- Load `delegation-autopilot` when spawning/iterating subagents.
- Load `context-control` if worker outputs become large.
- Load `workflow-protocols` when you need compact triage/reporting formats.

## Model and Topology
- Parent: `gpt-5.3-codex`, thinking low.
- Workers: `codex-spark` only.
- Worker count: 3-5 parallel tracks max.
- Workers must never spawn subagents.
- Parent can spawn, route, wait, and re-dispatch.

## Tool Priority (Mandatory)
1. Native Codex web tools first: `search_query` -> `open`/`click`/`find`.
2. Firecrawl only when native tools are weak (JS rendering, extraction failure, weak coverage).
3. Use domain MCP docs/tools when primary sources require it.

## Execution Loop
1. Expand the user request into 3-8 concrete sub-questions.
2. Check ledger to avoid duplicates.
3. Dispatch workers by independent question clusters.
4. Collect worker reports.
5. Update ledger:
   - visited sources (url/title/date/status/reliability)
   - claims with supporting URLs
   - conflicts and unresolved gaps
6. Re-dispatch only unresolved/conflicting items.
7. Stop when coverage and confidence targets are reached.

## Ledger Discipline
Keep a compact in-context ledger each round. Never re-search the same source unless:
- A freshness re-check is required.
- A previous extraction failed.
- A new sub-question needs different evidence from the same source.

## Quality Gates
- Time-sensitive claims must include explicit dates.
- Non-trivial claims should have at least 2 reliable sources.
- Conflicts must be called out and resolved or labeled unresolved.
- Final answer includes confidence tags and uncertainty notes.

## Worker Prompt Contract
Each Spark worker must return:
1. `worker_id`
2. Queries executed
3. URLs searched/opened
4. Key findings
5. Claim -> URL evidence table
6. Gaps/uncertainties
7. Recommended next queries

Worker hard constraints:
- No subagent spawning.
- No duplicate source passes unless explicitly instructed.
- Keep reports concise and source-dense.

## Good vs Bad
Good:
- Splits work into independent tracks and runs grouped waits.
- Maintains an updated ledger to avoid repeated browsing.
- Escalates to Firecrawl only when native tools fail.

Bad:
- Re-runs the same queries each round.
- Uses Firecrawl first without testing native tools.
- Returns answers without source/date checks.

## Test Cases
- Case 1: "Latest pricing/model changes across 3 vendors" -> ensure date-verified sources and conflict handling.
- Case 2: "Compare two APIs with changelog links" -> ensure at least two primary sources per major claim.
- Case 3: "JS-heavy docs page" -> native tools fail, then Firecrawl fallback documented.
