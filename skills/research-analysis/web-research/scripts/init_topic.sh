#!/bin/bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <slug> [root_dir] [mode]" >&2
  echo "  slug: Topic identifier (letters, numbers, hyphens, underscores)" >&2
  echo "  root_dir: Optional root directory (default: \$HOME)" >&2
  echo "  mode: Optional mode (quick, standard, deep, parity-hunt)" >&2
  exit 1
fi

slug="$1"
ROOT="${2:-$HOME}"
MODE="${3:-standard}"

# Basic slug safety: keep folder names simple
if [[ ! "$slug" =~ ^[A-Za-z0-9][A-Za-z0-9_-]*$ ]]; then
  echo "Invalid slug: $slug (use letters, numbers, hyphen, underscore)" >&2
  exit 1
fi

base="$ROOT/research/${slug}"

mkdir -p "$base"

create_if_missing() {
  local path="$1"
  local content="$2"
  if [ -e "$path" ]; then
    echo "Exists: $path"
    return 0
  fi
  printf "%s" "$content" > "$path"
  echo "Created: $path"
}

create_if_missing "$base/plan.md" "# Research Plan

## Goal
-

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
  - \"\"
  - \"\"

## Success Criteria
- Coverage target:
- Confidence target:
- Stop conditions:
"

create_if_missing "$base/action-log.md" "# Action Log

| Step | Action Type | Target | Sub-question | Reason |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
"

create_if_missing "$base/evidence-ledger.md" "# Evidence Ledger

| claim_id | text | subq_id | stance | citations | confidence | notes |
| --- | --- | --- | --- | --- | --- | --- |
| q1-c1 |  | Q1 | supports/contradicts/contextualizes |  |  |  |
"

create_if_missing "$base/report.md" "# Report

## Executive Summary
-
-

## Findings by Sub-question
### Q1
- Claim:  (cite)

## Disagreements / Conflicts
-

## Limitations
-

## Open Questions
-

## Sources
-
"

create_if_missing "$base/stop-report.md" "# Stop Report

## Why the agent stopped
-

## Remaining uncertainties
-

## Impact on conclusions
-
"

# Parity-hunt mode: create additional required artifacts
if [ "$MODE" = "parity-hunt" ]; then
  echo ""
  echo "Mode: parity-hunt — creating additional artifacts..."

  create_if_missing "$base/parity-matrix.md" "# Parity Matrix: ${slug}

## Definitions

**Pre-made orchestration layer** = A deployable, product-shaped system that includes:
1. Scheduling (durable, timezone-aware, recurring)
2. Durable execution (retry, backoff, failure handling)
3. Persistence/state (task definitions, preferences, run history)
4. UI/dashboard (task CRUD, run visibility)
5. Notifications (email/push/Slack/webhooks)

## Tasks Baseline
- One-off + recurring schedules, timezone-aware
- Retries, backoff, failure states, run history
- Push/email notifications

## Pulse Baseline
- Daily overnight batch execution
- Memory/preferences, topic curation
- Card-based delivery UI, feedback loop

## Parity Matrix

| Capability | Tasks Baseline | Pulse Baseline | Evidence Required | Score (0-2) | Notes |
|------------|----------------|----------------|-------------------|-------------|-------|
| **Scheduling** | One-off + recurring; timezone | Daily overnight | Schedule/cron docs | | |
| **Durable Execution** | Retries, backoff | Resumable batches | Retry docs; run history | | |
| **Persistence/State** | Task defs persisted | Topic prefs + cards | Storage/DB docs | | |
| **Notifications** | Push/email/webhook | Card delivery | Notification docs | | |
| **UI/Dashboard** | Create/manage tasks | Scan cards | UI docs/screenshots | | |
| **Integrations** | API triggers | Calendar/feeds/apps | Connector docs | | |
| **Human Oversight** | Optional | Feedback loop | Approvals docs | | |
| **Security** | Tool least-privilege | Web data untrusted | Security docs | | |

## Scoring
- **0** = No evidence capability exists
- **1** = Capability exists but partial (engineering required)
- **2** = Product-grade (UI, docs, controls)
"

  create_if_missing "$base/candidate-inventory.md" "# Candidate Inventory: ${slug}

## Solution Class Quotas (MUST satisfy before deep verification)

- [ ] 3+ workflow automation platforms
- [ ] 3+ durable execution engines
- [ ] 3+ event-driven runtimes
- [ ] 3+ data orchestrators

Agent frameworks may not exceed 25% of early inventory.

## Inventory

| Candidate | Solution Class | Repo/Home | Self-Host Docs | Scheduling Docs | UI/Runs Docs | Notifications Docs | Notes | Score |
|-----------|----------------|-----------|----------------|-----------------|--------------|-------------------|-------|-------|
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

## Shortlist (Top 6-10 for Deep Verification)

1.
2.
3.
4.
5.
6.
"

  create_if_missing "$base/query-families.md" "# Query Families: ${slug}

## Requirements
- Minimum 8 query families
- Minimum 30 distinct queries executed
- Minimum 4 iterations

## Query Families

| Family | Goal | Queries Executed | Key Sources | Gaps | Next Queries |
|--------|------|------------------|-------------|------|--------------|
| Workflow Automation | Find platforms with schedules + UI | 0 | | | |
| Durable Execution | Find reliable orchestration | 0 | | | |
| Event-Driven Runtimes | Find job queues with dashboards | 0 | | | |
| Data Orchestrators | Find data pipeline scheduling | 0 | | | |
| Notification Channels | Find scheduling + notifications | 0 | | | |
| Integrated Templates | Find starter kits / docker-compose | 0 | | | |
| Pulse-like Systems | Find daily briefing automation | 0 | | | |
| Connector Standards | Find MCP / agent patterns | 0 | | | |

## Seed Queries

### Workflow Automation
- self-hosted workflow automation schedule trigger dashboard
- n8n schedule trigger docs
- windmill scheduling documentation

### Durable Execution
- temporal schedules documentation
- durable execution workflow orchestration schedules

### Event-Driven Runtimes
- trigger.dev scheduled tasks
- inngest scheduled functions

### Data Orchestrators
- prefect schedules sensors
- dagster schedules partitions
- kestra schedule trigger

### Notification Channels
- scheduled workflow email notification
- slack notification workflow automation

### Integrated Templates
- docker-compose agent scheduler dashboard
- starter kit LLM agent schedule

### Pulse-like Systems
- daily briefing automation self-hosted

### Connector Standards
- Model Context Protocol MCP schedule

## Query Execution Log

| # | Query | Family | Tool | Results | New Candidates | Notes |
|---|-------|--------|------|---------|----------------|-------|
| 1 | | | | | | |
"

  create_if_missing "$base/open-questions.md" "# Open Questions: ${slug}

## Requirements
Minimum 12 questions spanning: scheduling, durability, persistence, notifications, UI, integrations, deployment, security.

## Questions

### Scheduling
1. [ ] Which platforms support one-off AND recurring schedules with timezone awareness?
2. [ ] Which platforms allow pause/resume/update of schedules?

### Durability / Execution
3. [ ] Which platforms have built-in retry with configurable backoff?
4. [ ] Which platforms handle overlapping schedule runs?
5. [ ] Which platforms persist run history?

### Persistence / State
6. [ ] Which platforms store task definitions durably?
7. [ ] Which platforms support user-specific preferences?

### Notifications
8. [ ] Which platforms have built-in email/push/Slack?
9. [ ] Which platforms provide webhook integrations?

### UI / Dashboard
10. [ ] Which platforms provide web UI for managing schedules?
11. [ ] Which platforms show run history and logs in UI?

### Integrations
12. [ ] Which platforms support external triggers (API/webhook)?
13. [ ] Which platforms have connector ecosystems?

### Deployment
14. [ ] Which platforms can be self-hosted via docker-compose?
15. [ ] Which platforms have production-ready deployment docs?

### Security
16. [ ] Which platforms document prompt injection defenses?
17. [ ] Which platforms support least-privilege tool access?

## Answered Questions

| # | Question | Answer | Evidence | Confidence |
|---|----------|--------|----------|------------|
| | | | | |
"
fi

echo ""
echo "Initialized research topic: $base (mode: $MODE)"
echo ""
echo "Artifacts created:"
ls -la "$base"
