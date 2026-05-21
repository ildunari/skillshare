# Templates (Copy/Paste)

---

## Product Parity Hunt Templates (Required for parity-hunt mode)

### Parity Matrix (parity-matrix.md)

```markdown
# Parity Matrix: [Topic]

## Definitions

**Pre-made orchestration layer** = A deployable, product-shaped system that already includes:
1. Scheduling (durable, survives restarts, timezone-aware, recurring)
2. Durable execution (retry/backoff, failure handling, run history)
3. Persistence/state (task definitions, user prefs, artifacts)
4. UI/dashboard (create/manage tasks, view runs)
5. Notifications (email/push/Slack/webhooks or integration surface)

Optional but valuable: approvals/HITL, multi-tenant isolation, observability, connector ecosystem.

## Tasks Baseline (What OpenAI Tasks provides)

- One-off + recurring schedules, timezone-aware
- Retries, backoff, failure states, run history visibility
- Task definitions persisted
- Push/email notifications when tasks complete
- Create/manage tasks UI, view runs

## Pulse Baseline (What OpenAI Pulse provides)

- Daily overnight batch execution
- Memory/preferences store, topic curation
- Card-based delivery UI, scan-friendly summaries
- Feedback loop (thumbs up/down, curate)
- Integration hooks (calendar, feeds, apps)

## Parity Matrix

| Capability | Tasks Baseline | Pulse Baseline | Evidence Required | Score (0-2) | Notes |
|------------|----------------|----------------|-------------------|-------------|-------|
| **Scheduling** | One-off + recurring; timezone-aware | Daily overnight run | Schedule/cron docs; pause/update semantics | | |
| **Durable Execution** | Retries, backoff, failure states | Resumable batch runs | Retry policy docs; run history UI | | |
| **Persistence/State** | Task definitions persisted | Topic prefs + saved cards | Storage model; DB/queue docs | | |
| **Notifications** | Push/email/webhook | Card feed delivery | Notification docs; webhook integrations | | |
| **UI/Dashboard** | Create/manage tasks; view runs | Scan cards; save/expand | UI docs/screenshots | | |
| **Integrations** | API trigger surface | Calendar/feeds/connected apps | Connectors docs; auth model | | |
| **Human Oversight** | Optional | Feedback loop is core | Approvals; moderation; controls | | |
| **Security Boundaries** | Tool least-privilege | Web data is untrusted | Injection defenses; memory hygiene | | |

## Scoring Rule

- **0** = No evidence the capability exists
- **1** = Capability exists but partial or not productized (engineering required)
- **2** = Capability exists with product-grade affordances (UI, docs, controls)

## Stop Gate

Research cannot stop until:
- At least one candidate scores ≥1 on every Tasks-baseline row
- At least two candidates score ≥2 on: Scheduling + Durable Execution + UI + Notifications
- Every score has evidence URL in evidence-ledger.md
```

---

### Candidate Inventory (candidate-inventory.md)

```markdown
# Candidate Inventory: [Topic]

## Solution Class Quotas (Fail-Closed)

Before deep dives, ensure inventory includes at least:
- [ ] 3 workflow automation platforms (schedules + UI + integrations)
- [ ] 3 durable execution / orchestration engines
- [ ] 3 event-driven runtimes / task runners with dashboards
- [ ] 3 data orchestrators with schedules + UI

Agent frameworks may be included but must not exceed 25% of early inventory.

## Inventory Table

| Candidate | Solution Class | Repo/Home | Self-Host Docs | Scheduling Docs | UI/Run History Docs | Notifications Docs | Notes | Initial Score |
|-----------|----------------|-----------|----------------|-----------------|---------------------|-------------------|-------|---------------|
| | workflow-automation | | | | | | | |
| | workflow-automation | | | | | | | |
| | workflow-automation | | | | | | | |
| | durable-execution | | | | | | | |
| | durable-execution | | | | | | | |
| | durable-execution | | | | | | | |
| | event-driven-runtime | | | | | | | |
| | event-driven-runtime | | | | | | | |
| | event-driven-runtime | | | | | | | |
| | data-orchestrator | | | | | | | |
| | data-orchestrator | | | | | | | |
| | data-orchestrator | | | | | | | |

## Solution Class Definitions

| Class | What It Provides | Why It Matters | Proof Pages to Fetch |
|-------|------------------|----------------|---------------------|
| **Workflow Automation** | Schedules + UI + integrations | Closest to "pre-made layer" | Schedule docs; run history UI; notification nodes |
| **Durable Execution** | Reliability + long-running workflows | Makes tasks trustworthy | Schedule features; retry/overlap policies; observability |
| **Event-Driven Runtime** | Cron + queues + concurrency | Practical task runner | Scheduled task docs + dashboard |
| **Data Orchestrator** | Schedules + UI + monitoring | "Tasks" base with visibility | Schedules/sensors + UI automation docs |
| **Agent Framework** | Tool use + memory | "Agent brain" only | Tool/memory docs; persistence patterns |
| **Integrated Template** | End-to-end deployment | The actual target | docker-compose, example repo, deployment docs |

## Shortlist (Top Candidates for Deep Verification)

After solution-class sweep, shortlist 6-10 candidates here:

1.
2.
3.
4.
5.
6.
```

---

### Query Families (query-families.md)

```markdown
# Query Families: [Topic]

## Requirements

- Minimum 8 query families
- Minimum 30 distinct queries executed total
- Minimum 4 iterations (search batch → fetch batch → update → repeat)

## Query Families Table

| Family | Goal | Queries Executed | Key Sources Found | Gaps | Next Queries |
|--------|------|------------------|-------------------|------|--------------|
| Workflow Automation Platforms | Find self-hostable platforms with schedules + UI | 0 | | | |
| Durable Execution Engines | Find reliable orchestration with schedules | 0 | | | |
| Event-Driven Runtimes | Find job queues with dashboards | 0 | | | |
| Data Orchestrators | Find data pipeline tools with scheduling | 0 | | | |
| Notification Channels | Find scheduling + notification integrations | 0 | | | |
| Integrated Templates | Find starter kits / docker-compose deployments | 0 | | | |
| Pulse-like Systems | Find daily briefing / digest automation | 0 | | | |
| Connector Standards | Find MCP / agent instruction patterns | 0 | | | |

## Seed Queries by Family

### Workflow Automation Platforms
- self-hosted workflow automation schedule trigger dashboard open source
- cron workflow UI open source scheduling triggers runs history
- "schedule trigger" node workflow automation platform docs
- self-hosted zapier alternative schedule webhook notification
- n8n schedule trigger docs
- windmill scheduling docs

### Durable Execution Engines
- durable execution workflow orchestration schedules pause update
- overlap policy schedules retries backfill workflow engine
- "schedule" "overlap policy" "backfill" docs workflow orchestration
- temporal schedules documentation
- restate scheduling durable execution

### Event-Driven Runtimes
- scheduled tasks dashboard open source job queue UI retries
- "cron schedules" "dashboard" task runner open source
- trigger.dev scheduled tasks documentation
- inngest scheduled functions

### Data Orchestrators
- prefect schedules sensors UI automation
- dagster schedules sensors partitions
- kestra schedule trigger documentation
- airflow scheduler UI runs

### Notification Channels
- scheduled workflow email notification integration
- push notification webhook scheduled job
- slack notification node scheduled workflow
- workflow automation notification channel docs

### Integrated Templates
- docker-compose agent scheduler dashboard notifications
- starter kit "workflow automation" "LLM agent" schedule
- "template" "agent" "scheduler" "webhooks" repo github
- self-hosted pulse alternative daily briefing

### Pulse-like Systems
- daily briefing automation self-hosted summarize news schedule
- "digest" "daily" "workflow automation" notifications
- personalized news aggregator self-hosted schedule

### Connector Standards
- Model Context Protocol MCP schedule automation agent
- AGENTS.md instructions file pattern for agents
- agent tool integration standard specification

## Query Execution Log

| # | Query | Family | Tool Used | Results Found | New Candidates | Notes |
|---|-------|--------|-----------|---------------|----------------|-------|
| 1 | | | | | | |
```

---

### Open Questions (open-questions.md)

```markdown
# Open Questions: [Topic]

## Requirements

Minimum 12 concrete questions spanning: scheduling, durability, persistence, notifications, UI, integrations, deployment, security.

## Questions

### Scheduling
1. [ ] Which platforms support one-off AND recurring schedules with timezone awareness?
2. [ ] Which platforms allow pause/resume/update of schedules without recreation?

### Durability / Execution
3. [ ] Which platforms have built-in retry with configurable backoff policies?
4. [ ] Which platforms handle overlapping schedule runs (skip, queue, allow)?
5. [ ] Which platforms persist run history and allow inspection of past executions?

### Persistence / State
6. [ ] Which platforms store task definitions durably (survive restarts)?
7. [ ] Which platforms support user-specific preferences or memory?

### Notifications
8. [ ] Which platforms have built-in email/push/Slack notifications?
9. [ ] Which platforms provide webhook integrations for custom notifications?

### UI / Dashboard
10. [ ] Which platforms provide a web UI for creating/managing schedules?
11. [ ] Which platforms show run history, logs, and failure details in UI?

### Integrations
12. [ ] Which platforms support external triggers (API, webhook, event)?
13. [ ] Which platforms have connector ecosystems (MCP, app integrations)?

### Deployment
14. [ ] Which platforms can be self-hosted via docker-compose or similar?
15. [ ] Which platforms have production-ready deployment documentation?

### Security
16. [ ] Which platforms document prompt injection / tool abuse defenses?
17. [ ] Which platforms support least-privilege tool access or approval flows?

## Answered Questions

| # | Question | Answer | Evidence | Confidence |
|---|----------|--------|----------|------------|
| | | | | |
```

---

### Integration Architecture (integration-architecture.md) — Only if no single solution exists

```markdown
# Integration Architecture: [Topic]

## When to Use This Template

Create this document only if:
- No single candidate achieves parity on all Tasks-baseline rows
- Best path forward is composing multiple systems

## Reference Architecture for Tasks Parity

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│  (Task CRUD + Run History + Cards Feed + Feedback Loop)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Scheduler / Orchestrator                      │
│  (Cron + Durable Schedules + Pause/Resume + Overlap Policy)      │
│  Options: Temporal, Windmill, n8n, Kestra                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Agent Runtime                               │
│  (LLM Tool Use + Memory + Web Browsing + Action Execution)       │
│  Options: LangGraph, CrewAI, custom with tool boundaries         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Persistence Layer                             │
│  (Task Definitions + User Prefs + Run History + Artifacts)       │
│  Options: PostgreSQL, SQLite, Redis, S3                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Notification Layer                             │
│  (Email + Push + Slack + Webhooks)                               │
│  Options: Built-in (n8n/Windmill) or Novu/Knock/custom           │
└─────────────────────────────────────────────────────────────────┘
```

## Component Selection

| Component | Recommended | Rationale | Evidence |
|-----------|-------------|-----------|----------|
| Scheduler | | | |
| Agent Runtime | | | |
| Persistence | | | |
| Notifications | | | |
| UI | | | |

## What's Missing Relative to Pulse

- [ ] Memory-driven topic curation
- [ ] Card-like delivery UI
- [ ] Feedback loop (thumbs up/down)
- [ ] Connected app integrations (calendar, feeds)

## Deployment Complexity

| Approach | Components | Deployment Effort | Notes |
|----------|------------|-------------------|-------|
| Single platform | 1 | Low | If one hits parity |
| Scheduler + Runtime | 2 | Medium | Most common |
| Full stack | 4-5 | High | Maximum flexibility |
```

---

## Standard Templates (All Modes)

## Research Plan (plan.md)

```markdown
# Research Plan

## Goal
- [What are we answering?]

## Scope & Constraints
- Timeframe:
- Exclusions:
- Required source types:
- Mode: quick / standard / deep

## Clarifying Questions
1. 
2. 
3. 

## Sub-questions
- Q1:
- Q2:
- Q3:

## Initial Queries
- Q1:
  - "..."
  - "..."
- Q2:
  - "..."

## Success Criteria
- Coverage target:
- Confidence target:
- Stop conditions:
```

## Action Log (action-log.md)

```markdown
# Action Log

| Step | Action Type | Target | Sub-question | Reason |
| --- | --- | --- | --- | --- |
| 1 | search | "query" | Q1 | Breadth pass |
```

## Evidence Ledger (evidence-ledger.md)

```markdown
# Evidence Ledger

| claim_id | text | subq_id | stance | citations | confidence | notes |
| --- | --- | --- | --- | --- | --- | --- |
| q1-c1 | [claim text] | Q1 | supports/contradicts/contextualizes | [citation1] | 0.75 | caveats |
```

## Report (report.md)

```markdown
# Report

## Executive Summary
- 
- 

## Recommendation (if applicable)
- Best overall: 
- Best for bosses: 
- Best for speedfarming: 
- Best for pushing: 

## 30-second playstyle
- 

## Required pieces (if applicable)
- Key uniques: 
- Key aspects: 

## Findings by Sub-question
### Q1
- Claim: ... (cite)
- Claim: ... (cite)

### Q2
- Claim: ... (cite)

## Disagreements / Conflicts
- 

## Limitations
- 

## Open Questions
- 

## Sources
- [Title] — Publisher (Date) — URL
```

## Stop Report (stop-report.md)

```markdown
# Stop Report

## Why the agent stopped
- [Budget exhausted / saturation reached / critical coverage achieved]
- Novelty fell below [threshold] / redundancy above [threshold]
- Coverage of sub-questions: [X%]
- Minimum claim confidence: [value]

## Remaining uncertainties
- 

## Impact on conclusions
- 
```

## Topic lifecycle checklist (optional)

```markdown
# Topic lifecycle

## When to keep using the same research session
- Follow-up questions on the same topic
- Expanding coverage or resolving disagreements for the same report

## When to start a new topic
- New domain/topic (not just a sub-question)
- New deliverable (e.g., decision memo vs technical spec)

## When you’re done
- report.md complete
- stop-report.md (if needed)
- optionally archive the whole folder to research/_archive/
```
