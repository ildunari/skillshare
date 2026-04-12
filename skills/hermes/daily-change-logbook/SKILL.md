---
name: hermes__daily-change-logbook
description: >
  Maintain the Hermes day-by-day change logbook when canonical operational
  history lives under ~/.hermes/shared/durable-state/change-log/. Use when
  updating daily Hermes change records, maintaining the shared change-log spec,
  or wiring automation that harvests recent sessions into the shared logbook.
targets: [hermes-default, hermes-gpt]
---

# Hermes Daily Change Logbook

Use this when Hermes changes should be recorded as durable operational history instead of disappearing into chat transcripts.

## Canonical paths

- Durable-state root: `~/.hermes/shared/durable-state/`
- Top-level spec: `~/.hermes/shared/durable-state/SPEC.md`
- Change-log spec: `~/.hermes/shared/durable-state/specs/change-log-spec.md`
- Change-log root: `~/.hermes/shared/durable-state/change-log/`
- Daily files: `~/.hermes/shared/durable-state/change-log/daily/YYYY-MM-DD.md`
- Helper script: `~/.hermes/scripts/hermes_logbook_context.py`

The old repo path under `~/.hermes/hermes-agent/ops/change-log/` should be treated as legacy documentation or migration surface, not the canonical log destination.

## When to log

Log durable work that changes Hermes behavior or the local Hermes operating environment, such as:
- repo code edits in `~/.hermes/hermes-agent`
- profile/config changes that materially change behavior
- shared durable-state migrations or spec changes
- local patches, restore hooks, patch preservation, update-preservation work
- gateway, voice, STT, TTS, browser, memory, skillshare, automation, cron, or update workflow changes
- debugging that established a real root cause or ruled out an important assumption

Do not log random chat, vague brainstorming, or experiments that changed nothing.

## Daily file shape

1. `# YYYY-MM-DD`
2. `## Summary`
3. `## Changes`
4. `## Decisions / Findings`
5. `## Follow-ups`
6. `## Session coverage`

Keep it compact and factual.

## Workflow

1. Read the top-level durable-state spec and the change-log spec first.
2. Read today's daily file if it exists; append/update instead of creating duplicates.
3. Gather evidence from live files, git state, config, and recent sessions.
4. Write only the durable result:
   - what changed
   - where it changed
   - why it mattered
   - current state now
5. Put root causes and confirmed mismatches in `## Decisions / Findings`.
6. Put only still-relevant unfinished work in `## Follow-ups`.
7. In `## Session coverage`, account for every candidate session as reviewed or ignored.
8. If automation is in play, ensure the finished daily log is ingested into mem0.

## Session coverage format

- reviewed: `<session_id>` — `<source>` — `<short title or preview>`
- ignored: `<session_id>` — `<reason>`

## Automation pattern

The helper script should build context from active Hermes state DBs and emit:
- the final `log_path`
- the shared durable-state spec path(s)
- already-logged session IDs
- candidate sessions

The cron job should:
- read the shared durable-state specs
- update the canonical shared daily log in place
- preserve good human edits
- account for every candidate session
- ingest the final daily log into mem0
- never schedule more cron jobs from inside the cron run

## Verification checklist

Before finishing, verify:
- the shared durable-state root exists
- today's daily file exists or was updated correctly
- helper script output points at the shared durable-state paths
- cron prompt/jobs do not still teach the old repo-local canonical path
- the finished daily log was read back and, if applicable, ingested into mem0
