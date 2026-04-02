---
name: agentic-web-research
user-invocable: false
description: |
  Agentic, multi-step web research with sub-agent spawning, evidence-ledger artifacts, and reproducible reports.
  Use when asked to research, look things up, compare sources, or gather citations across multiple web pages.
  Triggers: research, look up, search for, find information, compare, gather sources, web research, /search command.
---

# Agentic Web Research

## When to Use This Skill

Use for web research that needs:
- Multi-step browsing across multiple sources
- Citations and evidence tracking
- Cross-checking and source verification
- Structured reporting with confidence levels

**Trigger via:** `/search <query>` command or when user asks to research something.

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

**Automatically switch to `product-parity-hunt` mode** when the user's request includes:

- "Pulse", "Tasks", "ChatGPT Tasks", "OpenAI Pulse"
- "reminders", "notifications", "scheduling parity"
- "Zapier-like", "IFTTT-like", "n8n alternative"
- "orchestration layer", "workflow automation platform"
- "self-hosted Zapier", "self-hosted workflow"
- "scheduling + UI", "scheduler with dashboard"
- "find me a [X] that can schedule/notify/remind"

When auto-escalating, inform the user:
> "This looks like a product-parity hunt. I'll use the `product-parity-hunt` mode which requires broader coverage across solution classes and stricter evidence requirements."

---

## Product-Parity-Hunt Mode (Special Protocol)

This mode is for finding **pre-made orchestration layers** — deployable systems that already include scheduling, durable execution, persistence, UI, and notifications.

### Step 0: Mandatory Artifacts (BEFORE any tool calls)

Create these files immediately in `~/research/<slug>/`:

1. **`parity-matrix.md`** — Define what "parity" means for this hunt
2. **`open-questions.md`** — Minimum 12 concrete questions
3. **`query-families.md`** — Minimum 8 query families planned
4. **`candidate-inventory.md`** — Empty scaffold with solution-class quotas

**No searches or fetches until Step 0 is complete.**

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

### Proof-Page Requirements

For each shortlisted candidate, fetch at least:
- [ ] Scheduling/cron/trigger documentation
- [ ] Run history / monitoring / observability docs
- [ ] Notifications / integrations documentation
- [ ] Self-host / deployment documentation

**No marketing-only claims**: If the only evidence is a marketing page, parity score cannot exceed 1.

### Stop Gates (Fail-Closed)

You may NOT stop until ALL are true:

1. ✅ `parity-matrix.md` exists with scores + notes for every row
2. ✅ `candidate-inventory.md` has ≥3 candidates per platform class
3. ✅ `query-families.md` has ≥8 families and ≥30 executed queries
4. ✅ At least one candidate scores ≥1 on every Tasks-baseline row
5. ✅ Every claim in report maps to evidence URL in `evidence-ledger.md`

**If gates cannot be satisfied and budget is exhausted:**
- Write `stop-report.md` explaining which gates failed
- List what additional research would be needed
- Provide best available recommendation with caveats

### Anti-Stagnation Rule

If the last iteration produced:
- No new candidates
- No parity matrix row upgrades
- No reduction in open questions

Then the next iteration MUST expand scope by:
- Adding a new solution-class target
- Adding a new query family
- Trying different search terms

**No more "keep fetching more docs from the same framework."**

---

## Quick Start

1. Read `references/tool-policy.md` for tool priority and concurrency rules
2. Use the **Task tool** to spawn a research sub-agent
3. Sub-agent writes artifacts to `~/research/<slug>/` and returns executive summary
4. For comprehensive reference, load `references/scaffold.md`

## Tool Priority (Claude Code)

| Priority | Tool | Use For |
|----------|------|---------|
| 1 | `mcp__brave-search__brave_web_search` | Breadth searches, query expansion |
| 2 | `mcp__exa__web_search_exa` | High-quality extraction |
| 3 | `mcp__exa__web_search_advanced_exa` | Filtered searches (domain, date, category) |
| 4 | `mcp__firecrawl__firecrawl_scrape` | JS-heavy sites, clean markdown |
| 5 | `mcp__firecrawl__firecrawl_map` | Site discovery, docs portals |
| 6 | `WebFetch` | Quick static pages (cheap) |
| 7 | Browser tools | Interactive/login only |

## Spawning a Research Agent

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

## Mode Presets

| Mode | Max Pages | Max Minutes | Stop When |
|------|-----------|-------------|-----------|
| **Quick** | 15 | 3 | Coverage ≥60%, Confidence ≥0.65 |
| **Standard** | 40 | 8 | Coverage ≥80%, Confidence ≥0.75 |
| **Deep** | 60 | 15 | Coverage ≥90%, Confidence ≥0.80 |

## Iteration Discipline

**Do NOT front-load searches.** Follow this loop:

```
1. Run small search batch (≤4 queries)
2. Pick top results, fetch 2-6 pages
3. Update coverage/novelty/disagreements
4. Only then decide next search batch
```

Rule: No more than 4 search calls in a row without fetching/scraping something.

## Follow-up Research

For follow-ups on the same topic:
1. Read previous artifacts (plan.md, evidence-ledger.md)
2. Spawn new agent with context: "Continue research on <topic>. Previous findings at <path>."
3. Or pass key findings directly in the prompt

## References

- `references/scaffold.md` — Full research scaffold v2 (comprehensive, 1000+ lines)
- `references/tool-policy.md` — Tool choice + concurrency defaults
- `references/templates.md` — Artifact templates (plan/action/evidence/report)
- `references/spawn-template.md` — Full spawn prompt template

## Scripts

```bash
# Initialize topic folder with empty templates
~/.claude/skills/agentic-web-research/scripts/init_topic.sh <slug>
```
