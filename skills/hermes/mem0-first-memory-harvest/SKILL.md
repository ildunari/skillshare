---
name: mem0-first-memory-harvest
description: Run a Hermes nightly or ad hoc memory harvest that uses live mem0 tools first, keeps built-in MEMORY.md/USER.md as a tiny hot cache, and reports skill candidates for procedural lessons instead of polluting long-term memory. Use when reviewing recent Hermes sessions for durable memories, memory hygiene, mem0 dedupe, hot-cache cleanup, or deciding whether a lesson belongs in mem0, built-in memory, or a reusable skill.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes mem0-first memory harvest

Use this for nightly or ad hoc durable-memory harvesting.

The point is simple: review recent Hermes conversations, keep only facts that will still matter later, and persist them into live mem0 without polluting memory with task logs or transient noise.

## Start with the hard gate

Before doing anything else, verify that live mem0 tools are actually exposed in this run.

Required tool surface:
- `mem0_search`
- `mem0_conclude`

Useful extras when available:
- `mem0_profile`
- `mem0_recall_recent`
- `mem0_add_document`

If `mem0_search` or `mem0_conclude` is missing, stop and report that explicitly. Do **not** silently fall back to built-in `memory`, and do **not** assume an old `mem0` skill exists.

## Survey recent sessions the efficient way

1. Call `session_search` with no query first.
   - This gives the recent-session browse view.
   - Use it to spot the likely substantive sessions inside the last 24h window.

2. Then run targeted `session_search` queries for likely topic clusters.
   - Good pattern: parallel searches over obvious themes from recent work.
   - Examples:
     - `mem0 OR memory OR harvest OR cron`
     - `telegram OR discord OR gateway OR bot`
     - `voice OR moss OR samantha OR tts OR stt`
     - project-specific terms from the recent recents list

3. Skip junk aggressively.
   - Skip `/start` sessions, trivial pings, abandoned threads, and pure cron/control chatter.
   - Favor sessions that contain a stable decision, correction, workflow rule, environment fact, or recurring lesson.


## Hot-cache and skill hygiene

Treat built-in `MEMORY.md` and `USER.md` as a tiny hot cache, not the canonical long-term store. During harvest, keep these rules in mind:

- Prefer mem0 for rich operational facts, environment details, project conventions, and workflow lessons.
- Use built-in `memory` / `user` only for ultra-stable facts that deserve to appear in every prompt.
- Do not auto-prune or rewrite built-in memory from an unattended cron run unless the duplicate is obvious and the replacement is strictly safer. If cleanup is needed, report it as a recommended hot-cache cleanup item.
- If a durable lesson is procedural — a repeatable workflow, tool sequence, debugging playbook, conversion pipeline, or validation checklist — report it as a skill candidate rather than storing the whole procedure in mem0. If an existing skill covers it but needs an update, report the skill name and proposed patch.
- If a new skill was created manually during the day, it is fine to store a compact mem0 fact saying that the skill exists and where it is managed; do not duplicate the skill body into mem0.

## What counts as durable

Good mem0 candidates:
- stable technical conventions
- machine-specific environment facts
- project structure or protocol facts
- recurring workflow rules
- durable user preferences
- lessons that would prevent repeated future mistakes

Bad candidates:
- temporary task progress
- one-off outputs
- transient failures or current outages
- PIDs, log paths, current process state
- prompt/runtime scaffolding of the cron job itself
- budget/status checks like “X is OK,” “Y is outdated,” or “Z was reviewed” unless they encode a durable rule, preference, or environment convention
- tool/project classification notes that only describe today’s triage state rather than a stable reusable fact
- anything secret or credential-adjacent

When in doubt, skip. mem0 should get richer over time, but not by accumulating task logs with better search.

## Classify before writing

Default destination is mem0.

Use these categories:
- `coding`
- `environment`
- `preferences`
- `personal`
- `workflow`

Use built-in `memory` only for the rare ultra-stable compact facts that truly deserve to inject into every future prompt. If built-in memory is already crowded, prefer not writing there at all.

## Dedupe every candidate first

For each candidate fact:

1. Run `mem0_search` with a focused query and the likely category.
2. If a near-duplicate already exists, skip it.
3. If an older memory exists but the new version is sharper or more complete, still write it with `mem0_conclude` and let mem0 reconcile.

Do not batch-write guesses without checking. The nightly job is only useful if it stays clean.

## Writing pattern

Use plain prose in `mem0_conclude`.

Prefer the format:
- one fact per write
- one sentence if possible
- explicit, concrete wording
- include `machine` when the fact is host-specific

Examples:
- `Hermes user-facing /verbose should cycle off -> all -> compact -> verbose -> off; tool_progress new stays config-valid but should not appear in the visible cycle.`
- `In Craft Companion, permission modes use wire values safe, ask, and allow-all, which map to the user-facing labels explore, ask, and execute.`

## Recommended harvesting loop

1. Verify mem0 tool surface.
2. Browse recents with blank `session_search`.
3. Run targeted topic searches.
4. Read enough summaries to understand what was actually learned.
5. Draft a short list of durable candidates.
6. For each candidate, run `mem0_search` dedupe.
7. Write only the survivors with `mem0_conclude`.
8. Report counts for:
   - mem0 added
   - mem0 updated
   - built-in memory added
   - categories intentionally skipped

## Reporting rule

If nothing genuinely durable surfaced, output exactly:
- `[SILENT]`

Otherwise keep the report concise and scan-friendly.

Suggested structure:
- `Memory harvest — YYYY-MM-DD`
- `mem0 added: N items`
- `mem0 updated: N items`
- `built-in memory added: none` (usually)
- `skipped on purpose: ...`
- `pattern worth keeping: ...`

## Pitfalls

- Do not assume old mem0-related skills still exist in the live registry.
- Do not treat a successful cron completion as proof that mem0 writes happened.
- Do not store findings just because they were repeated in session summaries; repetition is not durability.
- Do not over-trust truncated or indirect recall when the evidence is weak.
- Do not use built-in `memory` as a catch-all overflow store.

## Good trigger phrases

This skill should fire for requests like:
- "run the nightly memory harvest"
- "review the last 24h and save durable lessons into mem0"
- "mem0-first harvest"
- "harvest recent Hermes sessions into long-term memory"
- "dedupe recent session lessons against mem0 and store the durable ones"
