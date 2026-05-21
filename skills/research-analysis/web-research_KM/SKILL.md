---
name: "Web Research"
description: >
  Multi-step web research with sub-agent spawning, evidence tracking, citation management,
  and iterative gap-closing across multiple sources. Use this skill when a question needs
  current web information, citations, or investigation across multiple sources.
  Triggers on: "research", "look up", "search for", "find information about",
  "compare sources", "gather citations", "web research", "/search command",
  "deep research", "multi-source research", "fact-check", "investigate",
  or any task requiring synthesis from multiple web pages rather than a quick single lookup.
  Do not use for quick single-source lookups or local-only code work with no web dependency.
---

<!-- Merged from agentic-web-research and web-research-orchestrator. research-agent-protocol also archived (absorbed). Both source directories archived. -->
<!-- Merged from: research-prompt-writer, research-report-distiller (2026-04-05). Legacy material preserved under merged/. -->

# Web Research

Agentic, multi-step web research with sub-agent spawning, evidence-ledger artifacts, iterative gap-closing, and reproducible source-backed reports.

## Human Detail Standard

- Do not gloss over uncertainty, conflicts, or missing evidence.
- Work like a careful analyst: check, re-check, and document why each conclusion is justified.
- If a step is skipped, explicitly state what was skipped and why.

---

## Research Modes

### Mode Selection

| Mode | When to Use | Tool Budget | Stop Threshold |
|------|-------------|-------------|----------------|
| **quick** | Fast answers, simple questions | 20 calls | ≥3/5 sub-questions answered, ≥2 sources each |
| **standard** | Balanced research (default) | 40 calls | ≥4/5 sub-questions answered, ≥2 sources each |
| **deep** | Thorough investigation | 60 calls | All sub-questions answered, ≥3 independent sources each |
| **product-parity-hunt** | Finding integrated stacks/platforms | 60-80 calls | Parity gates satisfied (see below) |

**Coverage definition**: A sub-question is "answered" when ≥2 independent, non-marketing sources either agree on an answer or the disagreement is documented. Confidence is expressed as source count + corroboration, not a float — e.g., "3 independent sources agree; 1 contradicts; treating as confirmed with caveat."

### Auto-Escalation to Product-Parity-Hunt

Automatically switch to `product-parity-hunt` mode when the user's request includes:
- "Pulse", "Tasks", "ChatGPT Tasks", "OpenAI Pulse"
- "reminders", "notifications", "scheduling parity"
- "Zapier-like", "IFTTT-like", "n8n alternative"
- "orchestration layer", "workflow automation platform"
- "self-hosted Zapier", "self-hosted workflow"
- "scheduling + UI", "scheduler with dashboard"
- "find me a [X] that can schedule/notify/remind"

When auto-escalating, inform the user: "This looks like a product-parity hunt. I'll use the `product-parity-hunt` mode which requires broader coverage across solution classes and stricter evidence requirements."

---

## Quick Start

1. Check which search tools are available this session (see Tool Priority below).
2. Use the **Task tool** to spawn a research sub-agent using the Quick Spawn Template.
3. Sub-agent writes artifacts to `~/research/<slug>/` and returns executive summary.
4. For deep/parity modes, follow the full Execution Loop below.

**Note**: Reference files (`references/scaffold.md`, `references/tool-policy.md`, etc.) are supplementary and may not be present. If absent, use this SKILL.md as the complete protocol.

---

## Tool Priority

Use tools in priority order; skip any that are unavailable in the current session.

| Priority | Tool | Use For |
|----------|------|---------|
| 1 | `mcp__tavily__tavily_search` | Breadth searches, query expansion |
| 2 | `mcp__tavily__tavily_research` | Deep single-topic research |
| 3 | `mcp__zai-search__web_search_prime` | Alternative breadth searches |
| 4 | `mcp__tavily__tavily_extract` | Structured extraction from known URLs |
| 5 | `mcp__claude_ai_Firecrawl__firecrawl_scrape` | JS-heavy sites, clean markdown |
| 6 | `mcp__claude_ai_Firecrawl__firecrawl_map` | Site discovery, docs portals |
| 7 | `mcp__zai-reader__webReader` | Reading specific pages cleanly |
| 8 | `WebFetch` | Quick static pages (cheap fallback) |
| 9 | `WebSearch` | Last-resort native search |
| 10 | Browser tools | Interactive/login only |

**Availability check**: Before spawning a sub-agent, note which tier-1 tools are available. If `mcp__tavily__tavily_search` is absent, step down to `mcp__zai-search__web_search_prime`. Document the fallback in `action-log.md`. Do not reference unavailable tools in spawn prompts.

**Legacy note**: Earlier versions listed `mcp__brave-search__brave_web_search` and `mcp__exa__web_search_exa`. These are superseded by the Tavily/ZAI stack above. If brave-search or exa appears in your session, they can be used as tier-1/2 alternatives.

**Firecrawl concurrency limit**: 2 concurrent jobs max.

---

## Spawning a Research Sub-Agent

Use the **Task tool** with:

```
subagent_type: "search-specialist"
description: "research:<topic-slug>"
prompt: [See Quick Spawn Template below]
```

### Quick Spawn Template

```
You are an agentic web research sub-agent.

## Topic
<TOPIC>

## Mode
<quick / standard / deep>

## Protocol
1. Decompose into 3-7 concrete sub-questions (write them to plan.md first).
2. Breadth phase: Search for coverage (max 4 searches before fetching anything).
3. Depth phase: Fetch/scrape top results, extract claims, note source URL + date.
4. Iterate: Update open questions, search again only if novelty remains.
5. Synthesize: Compile structured report with all claims mapped to source URLs.

## Tool Priority (use in order; skip unavailable tools)
1. mcp__tavily__tavily_search — breadth
2. mcp__tavily__tavily_research — deep single-topic
3. mcp__zai-search__web_search_prime — alternative breadth
4. mcp__claude_ai_Firecrawl__firecrawl_scrape — JS-heavy sites
5. mcp__zai-reader__webReader — clean page reading
6. WebFetch — static pages
7. WebSearch — last-resort native

## Iteration Discipline
- Max 4 search calls before fetching something.
- Fetch 2-6 pages per batch, then reassess coverage.
- Firecrawl concurrency limit: 2 concurrent jobs.
- If last iteration produced zero new claims: switch query family or escalate scope.

## Artifacts (write to ~/research/<slug>/)
- plan.md — sub-questions list (write BEFORE first tool call)
- action-log.md — every tool call, result summary, and tool used
- evidence-ledger.md — url | title | date | claim(s) | reliability
- report.md — final structured report
- stop-report.md — if stopping early (explain which gates failed)

## Stop Conditions (standard mode)
- ≥4 of 5 sub-questions answered (≥2 independent non-marketing sources each)
- No sub-question has zero coverage
- OR budget exhausted (document remaining gaps in stop-report.md)

## Citation Format
Each claim in report.md must have inline citation: [Source Title](URL) (YYYY-MM-DD).
If date unknown, write (date unknown). Never omit the URL.

## Return Format
1. Executive summary (5-10 bullets)
2. Key findings by sub-question
3. Sources with URLs and dates
4. Open questions (unanswered or conflicting)
5. Evidence quality note (how many independent sources; any marketing-only claims)
```

---

## Execution Loop (inline, not sub-agent)

1. Write `plan.md` with 3-8 concrete sub-questions **before any tool calls**.
2. Check ledger to avoid duplicate sources.
3. Dispatch workers by independent question clusters (3-5 parallel tracks max).
4. Collect worker reports.
5. Update ledger:
   - Visited sources: url / title / date / status / reliability
   - Claims with supporting URLs and dates
   - Conflicts and unresolved gaps
6. Re-dispatch only unresolved/conflicting items.
7. Stop when coverage targets are met (see mode table above).

## Ledger Discipline

Keep a compact in-context ledger each round. Never re-search the same source unless:
- A freshness re-check is required (time-sensitive claim)
- A previous extraction failed (document the failure)
- A new sub-question needs different evidence from the same source

---

## Iteration Discipline

**Do NOT front-load searches.** Follow this loop:

```
1. Run small search batch (≤4 queries)
2. Pick top results, fetch 2-6 pages
3. Update coverage (sub-questions answered / total)
4. Only then decide next search batch
```

Rule: No more than 4 search calls in a row without fetching/scraping something.

### Anti-Stagnation Rule

If the last iteration produced no new claims, no coverage improvements, and no reduction in open questions — the next iteration MUST expand scope by:
- Adding a new solution-class target
- Adding a new query family
- Trying different search terms (synonyms, competitor names, technical alternatives)

### Tool Failure Recovery

If a tool call returns an error or empty result:
1. Log the failure in `action-log.md` with tool name and error.
2. Step down to the next priority tool immediately.
3. If all tier-1/2 tools fail: use `WebFetch` with direct URLs found via any prior search.
4. Do not silently skip a sub-question due to tool failures — document the gap.

---

## Quality Gates

- Time-sensitive claims must include explicit dates.
- Non-trivial claims must have at least 2 reliable, independent (non-marketing) sources.
- Conflicts must be called out and either resolved or labeled "unresolved — see evidence-ledger.md".
- Final answer includes evidence quality notes (source count, any marketing-only sources).
- Every claim in report.md maps to a URL entry in `evidence-ledger.md`.
- Marketing-only claims are tagged `[marketing-only]` and excluded from coverage count.

---

## Product-Parity-Hunt Mode (Special Protocol)

This mode is for finding **pre-made orchestration layers** — deployable systems that already include scheduling, durable execution, persistence, UI, and notifications.

### Step 0: Mandatory Artifacts (BEFORE any tool calls)

Create these files immediately in `~/research/<slug>/`:

1. **`parity-matrix.md`** — Define what "parity" means for this hunt
2. **`open-questions.md`** — Minimum 12 concrete questions
3. **`query-families.md`** — Minimum 8 query families planned
4. **`candidate-inventory.md`** — Empty scaffold with solution-class quotas

No searches or fetches until Step 0 is complete.

### Mandatory Phases

| Phase | Name | What Happens |
|-------|------|--------------|
| 0 | Define | Create artifacts, no tool calls |
| 1 | Solution-Class Sweep | Breadth search with quotas (min 2 cycles) |
| 2 | Integration Hunt | Search for starter kits, templates, docker-compose |
| 3 | Deep Verification | Fetch proof pages for shortlisted candidates |
| 4 | Synthesis | Score parity matrix, produce decision |

### Solution-Class Quotas (Fail-Closed)

Before deep dives, the candidate inventory MUST include at least:
- **3** workflow automation platforms (schedules + UI + integrations)
- **3** durable execution / orchestration engines
- **3** event-driven runtimes / task runners with dashboards
- **3** data orchestrators with schedules + UI

Agent frameworks may be included but must not exceed **25%** of early inventory.

### Stop Gates (Fail-Closed)

You may NOT stop until ALL are true:

1. `parity-matrix.md` exists with scores + notes for every row
2. `candidate-inventory.md` has ≥3 candidates per platform class
3. `query-families.md` has ≥8 families and ≥30 executed queries
4. At least one candidate scores ≥1 on every Tasks-baseline row
5. Every claim in report maps to evidence URL in `evidence-ledger.md`

**If gates cannot be satisfied and budget is exhausted:**
- Write `stop-report.md` explaining which gates failed
- List what additional research would be needed
- Provide best available recommendation with caveats

---

## Follow-up Research

For follow-ups on the same topic:
1. Read previous artifacts (plan.md, evidence-ledger.md).
2. Spawn new agent with context: "Continue research on <topic>. Previous findings at <path>."
3. Or pass key findings directly in the prompt.

---

## References

The following reference files may exist alongside this SKILL.md in the installed skill directory. They are supplementary — this file is the complete protocol.

- `references/scaffold.md` — Full research scaffold v2 (comprehensive)
- `references/tool-policy.md` — Tool choice + concurrency defaults
- `references/templates.md` — Artifact templates (plan/action/evidence/report)
- `references/spawn-template.md` — Extended spawn prompt template
