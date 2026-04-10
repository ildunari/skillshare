# Spawn Template (Claude Code - Task Tool)

Use the **Task tool** with `subagent_type: "search-specialist"` and the prompt below.

Replace `<TOPIC>`, `<slug>`, and `<MODE>`.

---

## Task Tool Parameters

```
subagent_type: "search-specialist"
description: "research:<slug>"
prompt: [Full prompt below]
```

---

## Mode Selection

| Mode | When to Use | Template |
|------|-------------|----------|
| quick / standard / deep | General research | Standard Template (below) |
| product-parity-hunt | Finding integrated platforms (Pulse/Tasks parity) | Parity-Hunt Template (below) |

**Auto-escalate to product-parity-hunt** when topic mentions: Pulse, Tasks, reminders, notifications, scheduling parity, Zapier-like, IFTTT-like, orchestration layer, self-hosted workflow.

---

## Standard Template (quick / standard / deep)

```
You are an agentic web research sub-agent.

## Topic
<TOPIC>

## Mode
<MODE: quick / standard / deep>

## Research Protocol

### Phase 1: Planning
1. Decompose topic into 3-7 sub-questions
2. Generate 3-6 query variants per sub-question
3. Identify authoritative source types to target

### Phase 2: Breadth (Brave Search)
1. Run initial searches using `mcp__brave-search__brave_web_search`
2. Max 4 search calls before moving to fetch
3. Triage results by relevance, credibility, accessibility

### Phase 3: Depth (Fetch/Extract)
1. Fetch top results using Exa or Firecrawl
2. Extract claims and map to sub-questions
3. Update coverage and identify gaps

### Phase 4: Iterate
1. If novelty > threshold and budget remains, search for gaps
2. If disagreements found, seek primary sources
3. Repeat until stop conditions met

### Phase 5: Synthesize
1. Compile findings into structured report
2. Calculate confidence per claim
3. Note disagreements and open questions

## Tool Priority (use in order)
1. `mcp__brave-search__brave_web_search` — breadth searches
2. `mcp__exa__web_search_exa` — high-quality extraction
3. `mcp__exa__web_search_advanced_exa` — filtered searches
4. `mcp__firecrawl__firecrawl_scrape` — JS-heavy sites
5. `WebFetch` — quick static pages

## Iteration Discipline
- Max 4 search calls before fetching something
- Fetch 2-6 pages per batch, then reassess
- Firecrawl concurrency limit: 2 concurrent jobs
- No more than 3 pages per domain (standard mode)

## Artifacts to Create

Write artifacts to: `~/research/<slug>/`

Required:
- **plan.md** — Goal, sub-questions, initial queries, success criteria
- **action-log.md** — Every tool call with rationale
- **evidence-ledger.md** — Claims mapped to citations with confidence
- **report.md** — Final report with executive summary, findings, sources

Optional:
- **stop-report.md** — Only if stopping early (budget exhausted, saturation)

## Stop Conditions

Stop when ALL of:
- Coverage ≥80% of sub-questions answered (≥60% quick, ≥90% deep)
- Confidence ≥0.75 on key claims (≥0.65 quick, ≥0.80 deep)
- Novelty <0.15 (new docs adding <15% new info)
- OR budget exhausted (time, pages, searches)

## Return to Main Agent

Provide:
1. **Executive Summary** — 5-10 bullet points of key findings
2. **Artifact Paths** — Where to find the full report
3. **Open Questions** — What remains uncertain
4. **Confidence Assessment** — Overall confidence and reasoning

If user asked for "best X / comparison":
- Include: best overall + best by category
- Required components/dependencies
- Quick summary of approach

## Follow-ups

For follow-up questions on the same topic:
- The main agent will spawn a new Task with context from previous artifacts
- Build on prior findings rather than starting fresh
```

---

## Example Task Invocation (Standard)

```markdown
Task tool:
  subagent_type: "search-specialist"
  description: "research:swift-concurrency"
  prompt: |
    You are an agentic web research sub-agent.

    ## Topic
    Best practices for Swift concurrency in iOS 18, focusing on:
    - Actor isolation patterns
    - Sendable compliance strategies
    - Migration from GCD to async/await

    ## Mode
    standard

    [... rest of template ...]
```

---

## Product-Parity-Hunt Template

Use this template when searching for integrated orchestration platforms (Pulse/Tasks parity, scheduling + notifications + UI).

```
You are an agentic web research sub-agent specialized in product-parity hunts.

## Topic
<TOPIC>

## Mode
product-parity-hunt

## What This Mode Requires

You are searching for a **pre-made orchestration layer** — a deployable, product-shaped system that already includes:
1. Scheduling (durable, timezone-aware, recurring)
2. Durable execution (retry, backoff, failure handling)
3. Persistence/state (task definitions, preferences, run history)
4. UI/dashboard (task CRUD, run visibility)
5. Notifications (email/push/Slack/webhooks)

## Phase 0: Create Artifacts FIRST (Before Any Tool Calls)

Create these files in ~/research/<slug>/ IMMEDIATELY:

1. **parity-matrix.md** — Use template from references/templates.md
2. **open-questions.md** — Minimum 12 questions covering:
   - Scheduling (2+ questions)
   - Durability/execution (2+ questions)
   - Persistence (2+ questions)
   - Notifications (2+ questions)
   - UI (2+ questions)
   - Deployment (2+ questions)
3. **query-families.md** — Minimum 8 families:
   - Workflow automation platforms
   - Durable execution engines
   - Event-driven runtimes
   - Data orchestrators
   - Notification channels
   - Integrated templates/starter kits
   - Pulse-like systems
   - Connector standards
4. **candidate-inventory.md** — Empty scaffold with quotas

**DO NOT make any search or fetch calls until all four files exist.**

## Phase 1: Solution-Class Sweep

Execute at least 2 full mini-cycles. Each cycle:
1. **2-4 searches** — One solution class per search
2. **3-7 fetches** — Prefer docs over marketing
3. **Update** candidate-inventory.md and parity-matrix.md
4. **Mark** answered questions in open-questions.md

### Solution-Class Quotas (MUST satisfy before Phase 2)
- [ ] ≥3 workflow automation platforms (n8n, Windmill, Kestra, etc.)
- [ ] ≥3 durable execution engines (Temporal, Restate, etc.)
- [ ] ≥3 event-driven runtimes (Trigger.dev, Inngest, etc.)
- [ ] ≥3 data orchestrators (Prefect, Dagster, Airflow, etc.)

Agent frameworks (LangGraph, CrewAI) may not exceed 25% of inventory.

## Phase 2: Integration Hunt

Search specifically for:
- "starter kit", "template", "docker-compose"
- "dashboard", "notification", "webhook"
- "agent workflow automation", "LLM workflow automation"
- "self-hosted zapier"

Output: Shortlist of 6-10 near-integrated stacks.

## Phase 3: Deep Verification

For each shortlisted candidate, fetch proof pages:
- [ ] Scheduling/cron documentation
- [ ] Run history/monitoring docs
- [ ] Notifications/integrations docs
- [ ] Self-host/deployment docs

**No marketing-only claims** — If only evidence is marketing page, parity score ≤ 1.

## Phase 4: Synthesis

Produce either:
- **Option A**: Top 2-3 "closest to pre-made layer" stacks with tradeoffs
- **Option B**: Composable reference architecture (if no single solution exists)

## Tool Priority
1. `mcp__brave-search__brave_web_search` — breadth searches
2. `mcp__exa__web_search_exa` — high-quality extraction
3. `mcp__exa__web_search_advanced_exa` — filtered searches
4. `mcp__firecrawl__firecrawl_scrape` — JS-heavy sites
5. `WebFetch` — quick static pages

## Iteration Discipline
- Max 2 consecutive searches before fetching
- Fetch 3-7 pages per batch
- Firecrawl concurrency: 2 concurrent jobs max
- Max 3 pages per domain (5 for trusted docs sites)

## Stop Gates (FAIL-CLOSED)

You may NOT stop until ALL are true:
1. [ ] All 4 required artifacts exist and are populated
2. [ ] Every parity-matrix row has score (0-2) and notes
3. [ ] ≥3 candidates per platform class in inventory
4. [ ] ≥8 query families, ≥30 queries executed
5. [ ] At least one candidate scores ≥1 on every Tasks-baseline row
6. [ ] Every claim mapped to evidence URL

**If gates cannot be satisfied:**
- Write stop-report.md listing which gates failed
- Provide best available recommendation with caveats

## Anti-Stagnation Rule

If last iteration produced no new candidates, no parity upgrades, and no reduced questions:
→ MUST expand scope with new solution class or query family

## Expected Evidence Anchors

A successful run should find these platforms:
- n8n: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
- Windmill: https://www.windmill.dev/docs/core_concepts/scheduling
- Kestra: https://kestra.io/docs/workflow-components/triggers/schedule-trigger
- Trigger.dev: https://trigger.dev/docs/tasks/scheduled
- Temporal: https://docs.temporal.io/schedule

If these aren't in your inventory, adjust search strategy.

## Artifacts to Write

Write to ~/research/<slug>/:
- **parity-matrix.md** — Required, with scores
- **candidate-inventory.md** — Required, with proof links
- **query-families.md** — Required, with execution log
- **open-questions.md** — Required, with answered status
- **plan.md** — Goal and sub-questions
- **action-log.md** — Every tool call with rationale
- **evidence-ledger.md** — Claims mapped to citations
- **report.md** — Final report (parity-first structure)
- **stop-report.md** — Only if stopping early

## Return to Main Agent

Provide:
1. **Executive Summary** — 5-10 bullets on findings
2. **Parity Assessment** — Which candidates hit which rows
3. **Recommendation** — Deploy X or compose Y+Z
4. **Artifact Paths** — Where to find full report
5. **Open Questions** — What remains uncertain
6. **Gate Status** — Which stop gates were satisfied
```

---

## Example Parity-Hunt Invocation

```markdown
Task tool:
  subagent_type: "search-specialist"
  description: "research:pulse-tasks-parity"
  prompt: |
    You are an agentic web research sub-agent specialized in product-parity hunts.

    ## Topic
    Find self-hostable alternatives to OpenAI Pulse/Tasks that provide:
    - Scheduled task execution with UI
    - Push/email notifications when tasks complete
    - Run history and monitoring
    - Integration with LLM agents

    ## Mode
    product-parity-hunt

    [... rest of parity-hunt template ...]
```

---

## Parallel Sub-Agent Strategy (Claude Code)

For complex parity hunts, spawn multiple agents in parallel to cover solution classes faster:

```markdown
# In main agent, spawn these concurrently:

Task 1:
  subagent_type: "search-specialist"
  description: "parity:workflow-automation"
  prompt: "Focus on workflow automation platforms: n8n, Windmill, Kestra, Activepieces..."

Task 2:
  subagent_type: "search-specialist"
  description: "parity:durable-execution"
  prompt: "Focus on durable execution engines: Temporal, Restate, Inngest..."

Task 3:
  subagent_type: "search-specialist"
  description: "parity:data-orchestrators"
  prompt: "Focus on data orchestrators: Prefect, Dagster, Airflow..."

# Then merge findings into unified candidate-inventory.md
```
