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
| **quick** | Fast answers, simple questions | 20 calls | Coverage ≥60%, Confidence ≥0.65 |
| **standard** | Balanced research (default) | 40 calls | Coverage ≥80%, Confidence ≥0.75 |
| **deep** | Thorough investigation | 60 calls | Coverage ≥90%, Confidence ≥0.80 |
| **product-parity-hunt** | Finding integrated stacks/platforms | 60-80 calls | Parity gates satisfied (see below) |

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

1. Read `references/tool-policy.md` for tool priority and concurrency rules
2. Use the **Task tool** to spawn a research sub-agent
3. Sub-agent writes artifacts to `~/research/<slug>/` and returns executive summary
4. For comprehensive reference, load `references/scaffold.md`

---

## Tool Priority

| Priority | Tool | Use For |
|----------|------|---------|
| 1 | `mcp__brave-search__brave_web_search` | Breadth searches, query expansion |
| 2 | `mcp__exa__web_search_exa` | High-quality extraction |
| 3 | `mcp__exa__web_search_advanced_exa` | Filtered searches (domain, date, category) |
| 4 | `mcp__firecrawl__firecrawl_scrape` | JS-heavy sites, clean markdown |
| 5 | `mcp__firecrawl__firecrawl_map` | Site discovery, docs portals |
| 6 | `WebFetch` | Quick static pages (cheap) |
| 7 | Browser tools | Interactive/login only |

Also available as fallback: `search_query` → `open`/`click`/`find` (native Codex web tools). Use Firecrawl only when native tools fail — document the fallback.

---

## Spawning a Research Sub-Agent

Use the **Task tool** with:

```
subagent_type: "search-specialist"
description: "research:<topic-slug>"
prompt: [See spawn template in references/spawn-template.md]
```

### Quick Spawn Template

```
You are an agentic web research sub-agent.

## Topic
<TOPIC>

## Mode
<quick / standard / deep>

## Protocol
1. Decompose into 3-7 sub-questions
2. Breadth phase: Brave search for coverage (max 4 searches before fetching)
3. Depth phase: Fetch/scrape top results, extract claims
4. Iterate: Update gaps, search again if novelty remains
5. Synthesize: Compile structured report

## Tool Priority (use in order)
1. mcp__brave-search__brave_web_search — breadth
2. mcp__exa__web_search_exa — quality extraction
3. mcp__firecrawl__firecrawl_scrape — JS-heavy sites
4. WebFetch — static pages

## Iteration Discipline
- Max 4 search calls before fetching something
- Fetch 2-6 pages per batch, then reassess
- Firecrawl concurrency limit: 2 concurrent jobs

## Artifacts
Write to ~/research/<slug>/:
- plan.md
- action-log.md
- evidence-ledger.md
- report.md
- stop-report.md (if stopping early)

## Stop Conditions
- Coverage ≥80% of sub-questions
- Confidence ≥0.75 on key claims
- Novelty <0.15 (diminishing returns)
- OR budget exhausted

## Return Format
1. Executive summary (5-10 bullets)
2. Key findings by sub-question
3. Sources with URLs
4. Open questions
5. Confidence assessment
```

---

## Execution Loop (when running inline, not as sub-agent)

1. Expand the user request into 3-8 concrete sub-questions.
2. Check ledger to avoid duplicate sources.
3. Dispatch workers by independent question clusters (3-5 parallel tracks max).
4. Collect worker reports.
5. Update ledger:
   - Visited sources (url/title/date/status/reliability)
   - Claims with supporting URLs
   - Conflicts and unresolved gaps
6. Re-dispatch only unresolved/conflicting items.
7. Stop when coverage and confidence targets are reached.

## Ledger Discipline

Keep a compact in-context ledger each round. Never re-search the same source unless:
- A freshness re-check is required
- A previous extraction failed
- A new sub-question needs different evidence from the same source

---

## Iteration Discipline

**Do NOT front-load searches.** Follow this loop:

```
1. Run small search batch (≤4 queries)
2. Pick top results, fetch 2-6 pages
3. Update coverage/novelty/disagreements
4. Only then decide next search batch
```

Rule: No more than 4 search calls in a row without fetching/scraping something.

### Anti-Stagnation Rule

If the last iteration produced no new candidates, no coverage improvements, and no reduction in open questions — the next iteration MUST expand scope by:
- Adding a new solution-class target
- Adding a new query family
- Trying different search terms

---

## Quality Gates

- Time-sensitive claims must include explicit dates.
- Non-trivial claims should have at least 2 reliable sources.
- Conflicts must be called out and resolved or labeled unresolved.
- Final answer includes confidence tags and uncertainty notes.
- Every claim in report maps to evidence URL in `evidence-ledger.md`.
- No marketing-only claims: if the only evidence is a marketing page, parity score cannot exceed 1.

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
1. Read previous artifacts (plan.md, evidence-ledger.md)
2. Spawn new agent with context: "Continue research on <topic>. Previous findings at <path>."
3. Or pass key findings directly in the prompt

---

## References

- `references/scaffold.md` — Full research scaffold v2 (comprehensive, 1000+ lines)
- `references/tool-policy.md` — Tool choice + concurrency defaults
- `references/templates.md` — Artifact templates (plan/action/evidence/report)
- `references/spawn-template.md` — Full spawn prompt template

## Scripts

```bash
# Initialize topic folder with empty templates
scripts/init_topic.sh <slug>
```
