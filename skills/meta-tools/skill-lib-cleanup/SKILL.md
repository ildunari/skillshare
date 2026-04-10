---
name: Skill-Lib-Cleanup
description: >
  Audit, reorganize, and manage skills, agents, plugins, commands, and rules across
  AI runtimes with a canonical-source-aware, skillshare-aware pipeline. Use when the
  user wants to clean up a skill library, compare skill installs across Claude/Codex/
  Cursor/Gemini/Factory/Craft Agent, detect drift, analyze routing collisions, or make
  safe merge/archive/delete plans. Also use for requests about the canonical source of
  truth under ~/.config/skillshare/skills, sync drift against downstream installs, skill
  inventory, overlap analysis, canonical-vs-install reports, or any rollback-safe skill
  ecosystem maintenance task. This skill should cover both machine-wide broad sweeps
  where skills live across many runtimes and unified skillshare setups where one source
  library distributes to downstream targets.
---

# Skill Library Curator

Systematic audit and maintenance pipeline for a growing AI agent skill library.
Treat skills as composable infrastructure, with explicit distinction between:
- canonical source
- downstream installs
- mirrors / backups / archives
- project-local exceptions

This upgraded version is designed for a skillshare-based setup where the canonical skill library lives at:
- `/Users/kosta/.config/skillshare/skills`

and distribution targets are defined in:
- `/Users/kosta/.config/skillshare/config.yaml`

## Safety default

**Phases 0–8 are analysis-only.** They read files, run scripts, and produce JSON, markdown, and visual reports. They do not modify source or installed skills.

**Phase 9 (Execute)** is the only phase that changes anything, and it requires explicit user approval.

## Two operating models

### 1. Runtime-centric cleanup
Use this when the user wants to understand skills by installed runtime location.

Questions this mode answers:
- what’s duplicated or drifted across installed runtimes?
- which installed copies collide or overlap?
- what should be merged, archived, or rewritten inside runtime libraries?

### 2. Canonical-library cleanup
Use this when the user wants analysis of the source-of-truth skill library.

Questions this mode answers:
- what’s in `~/.config/skillshare/skills`?
- which source skills are undistributed?
- which targets are missing or drifted?
- which installed copies are downstream artifacts rather than editable source?
- what should be synced, promoted, archived, or regenerated?

When in doubt, ask whether the user wants a **runtime view** or a **canonical source view**. If they mention `skillshare` or `~/.config`, prefer canonical mode.

The bundled scripts should support both paths:
- **broad-sweep** — mixed runtime locations with no single source of truth
- **canonical-source** — one editable source plus distributed installs

Default behavior should auto-detect canonical mode when the scanned data includes the configured skillshare source. Otherwise, fall back to broad-sweep.

## Modes

Choose the lightest mode that answers the user’s question.

### `runtime-audit`
Use for installed-library cleanup within and across runtimes.

### `canonical-audit`
Use for source-of-truth analysis centered on `~/.config/skillshare/skills`.

### `sync-drift`
Use when the user wants to know what is in sync, out of sync, install-only, or undistributed.

### `distribution-topology`
Use when the user wants a map of canonical source → targets → installed copies.

### `cleanup-candidates`
Use when the user wants archive/delete/promote/regenerate recommendations.

### `full-library-audit`
Run the whole upgraded pipeline.

If the user does not specify a mode:
- prefer `canonical-audit` when the request names `skillshare`, `~/.config/skillshare/skills`, or downstream target drift
- prefer `runtime-audit` for machine-wide cleanup or “what is installed where?” questions

## Feedback loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior audits.

1. Detect — note what the audit missed or overclaimed.
2. Search — check for the same issue in `FEEDBACK.md`.
3. Scope — one actionable observation per entry.
4. Draft-and-ask — propose logging the lesson.
5. Write-on-approval — append only if the user approves.
6. Compact-at-75 — merge duplicates and archive resolved items.

## Progressive disclosure: what to load

Load only the references needed for the active question.

| Reference | Load when... |
|---|---|
| `FEEDBACK.md` | **Always** |
| `references/analysis-framework.md` | Relationship mapping and similarity reasoning |
| `references/canonical-library-mode.md` | Canonical source-of-truth or `~/.config` analysis |
| `references/skillshare-topology.md` | Reading skillshare config and target topology |
| `references/distribution-drift.md` | Sync drift / canonical-vs-install questions |
| `references/capability-taxonomy.md` | Capability extraction and overlap analysis |
| `references/routing-collision-guide.md` | Trigger and routing collision analysis |
| `references/blocklist.md` | Skills that should be treated as hands-off by cleanup actions |
| `references/action-scoring.md` | Merge/archive/delete/sync/promote scoring |
| `references/reporting-guide.md` | Final report and visual structure |
| `references/merge-protocol.md` | Execute phase only |

## Core distinctions the skill must preserve

Do not collapse these into one concept:
1. canonical source
2. runtime install
3. distribution drift
4. functional overlap
5. routing collision
6. delete/archive safety

Two same-named skills in different places are not automatically merge candidates.
A drifted install is primarily a sync problem, not a merge problem.
Skills named in `references/blocklist.md` should be treated as protected: report on them if needed, but do not recommend merge, rewrite, archive, or delete actions by default.

## Pipeline overview

```text
Phase 0: Discovery
Phase 1: Inventory
Phase 2: Skillshare / Canonical Topology
Phase 3: Canonical vs Install Drift Analysis
Phase 4: Relationship Map
Phase 5: Similarity Analysis
Phase 6: Capability / Trigger / Routing Analysis
Phase 7: Safety + Action Scoring
Phase 8: Visualize + Report
Phase 9: Execute (approved only)
```

## Phase details

### Phase 0 — Discovery
Map the entire skill ecosystem.

Use the discovery script to identify:
- skills
- agents/droids
- commands
- rules
- plugins
- profiles
- context files

For each item, record:
- path
- slug/name
- runtime
- scope
- content hash
- modification time
- line count
- role in distribution flow

Roles should include:
- canonical-source
- runtime-install
- mirror
- backup
- archive
- generated-artifact
- project-local-exception

### Phase 1 — Inventory
Extract frontmatter and structural metadata.

Also capture:
- trigger phrases
- supersedes declarations
- script count
- reference count
- FEEDBACK presence
- stale reference/model signals

### Phase 2 — Skillshare / Canonical Topology
**Load `references/canonical-library-mode.md` and `references/skillshare-topology.md`.**

Read:
- `~/.config/skillshare/config.yaml`

Treat:
- `~/.config/skillshare/skills`

as the canonical source when the user wants canonical analysis.

Generate:
- source skill inventory
- target runtime list
- skill topology map (source → targets)
- source-only / install-only / missing-target insights

### Phase 3 — Canonical vs Install Drift Analysis
**Load `references/distribution-drift.md`.**

Compare canonical skills against downstream installs.

Classify each source/target pair as:
- `in-sync`
- `out-of-sync`
- `install-only`
- `undistributed-source`
- `missing`

Important: drift is a distribution problem first. Do not jump to merge or delete.

### Phase 4 — Relationship Map
**Load `references/analysis-framework.md`.**

Preserve the existing strong concepts here:
- designed pairs
- override chains
- command bindings
- dependency clusters
- platform-scoped skills
- cross-location distribution relationships

### Phase 5 — Similarity Analysis
Run:
- exact duplicate clustering
- near-duplicate clustering
- family grouping

Keep these distinct:
- exact copies
- derived variants
- canonical source vs install copies
- genuinely overlapping source skills

Do not recommend merging canonical source with downstream install copies.

### Phase 6 — Capability / Trigger / Routing Analysis
**Load `references/capability-taxonomy.md` and `references/routing-collision-guide.md`.**

Extract:
- trigger phrases
- capability lines
- scripts/resources uniqueness
- runtime assumptions
- routing collisions

This phase should reduce false merges by separating:
- same keywords
- same function
- same trigger zone
- same platform surface

### Phase 7 — Safety + Action Scoring
**Load `references/action-scoring.md`.**

Every skill should end with one primary action.

Preferred action set:
- KEEP
- KEEP + REWRITE
- MERGE INTO
- SPLIT
- ARCHIVE
- REMOVE
- SYNC FROM SOURCE
- PUSH TO TARGETS
- PROMOTE TO SOURCE
- REGENERATE INSTALLS
- FIX ROUTING
- MARK PROJECT-LOCAL EXCEPTION

Use canonical-aware logic:
- source/install mismatch → usually SYNC / PUSH / PROMOTE / REGENERATE
- functional overlap among source skills → MERGE / SPLIT / KEEP + REWRITE
- mirrors/backups/archives → ARCHIVE / REMOVE candidates

### Phase 8 — Visualize + Report
**Load `references/reporting-guide.md`.**

Produce machine-readable outputs first, then markdown and visuals.

Preferred JSON outputs:
- `skill-discovery.json`
- `skill-inventory.json`
- `skill-capabilities.json`
- `skill-topology.json`
- `canonical-vs-install.json`
- `distribution-matrix.json`
- `duplicate-clusters.json`
- `similarity-clusters.json`
- `routing-collisions.json`
- `delete-candidates.json`
- `action-plan.json`
- `visual-data.json`

Preferred visuals:
- canonical source → target topology maps
- drift heatmap / distribution matrix
- duplicate family maps
- routing collision tables
- delete/archive safety ladder
- before/after reduction charts

### Phase 9 — Execute
**Load `references/merge-protocol.md`.**

Only after approval.

Execution order should be:
1. fix canonical source quality first
2. resolve source/install drift second
3. merge overlapping canonical source skills third
4. archive/delete stale installs or backups fourth
5. sync or regenerate targets last

This prevents syncing garbage or deleting the wrong copy.

## Scripts to prefer

Use these scripts for deterministic work:
- `scripts/discover_skills.py`
- `scripts/inventory_to_json.py`
- `scripts/analyze_skillshare_topology.py`
- `scripts/compare_canonical_vs_installs.py`
- `scripts/extract_skill_capabilities.py`
- `scripts/cluster_skill_duplicates.py`
- `scripts/cluster_skill_near_duplicates.py`
- `scripts/detect_routing_collisions.py`
- `scripts/score_skill_actions.py`
- `scripts/score_skill_delete_candidates.py`
- `scripts/build_distribution_matrix.py`
- `scripts/render_skill_cleanup_manifest.py`
- `scripts/render_skill_visual_data.py`
- existing freshness / token / visualization scripts where useful

## Visuals to generate when useful

Prefer visuals heavily. This skill is about topology and drift, not just prose.

### Use Mermaid for:
- source skill → target runtime topology
- one-skill distribution maps
- duplicate families

### Use tables for:
- distribution matrix
- action dashboard
- delete/archive candidates
- routing collisions

### Use charts for:
- synced vs drifted vs missing targets
- canonical source health
- duplicate family counts
- before/after cleanup impact

## Output structure

The final report should include:
1. executive summary
2. canonical source status
3. distribution drift matrix
4. duplicate / near-duplicate families
5. routing collisions
6. action dashboard
7. delete/archive ladder
8. visuals
9. execution order if requested

## What this skill does NOT do

- It does not auto-sync skillshare targets.
- It does not auto-delete source or installed skills without approval.
- It does not treat all same-name copies as merge candidates.
- It does not replace deep single-skill review and skill creation work (`skill-creator`).
- It does not assume project-local exceptions should be promoted unless the user asks.

## Quick-start recipes

### If the user says “what’s going on in ~/.config/skillshare/skills?”
1. Run canonical-audit
2. read skillshare topology
3. produce source inventory + drift matrix + action dashboard

### If the user says “which installs are out of sync?”
1. Run sync-drift
2. compare canonical vs installs
3. show distribution matrix and SYNC/PUSH/PROMOTE recommendations

### If the user says “which skills overlap?”
1. Run runtime-audit or canonical-audit depending on scope
2. run duplicate + near-duplicate clustering
3. run capability extraction and routing collision scan
4. show overlap families with merge confidence

### If the user says “what can I archive or delete?”
1. run cleanup-candidates
2. score delete/archive safety
3. distinguish canonical source from install/backup noise
4. show delete-now / archive-first / review-required buckets
