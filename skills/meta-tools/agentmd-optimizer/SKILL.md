---
name: agentmd-optimizer
description: >
  Audit and optimize CLAUDE.md, AGENTS.md, GEMINI.md, Cursor rules, and related
  agent instruction files with a runtime-aware, deterministic pipeline. Use when
  the user wants to reduce context bloat, understand what actually loads together,
  find exact or near-duplicate instructions, detect prompt drift or conflicts,
  manage cross-runtime skill copies, identify canonical sources, or generate safe
  merge/archive/delete plans. Also use when the user says their instruction stack
  is too big, wants to clean up skills across Claude/Codex/Gemini/Cursor, needs a
  session-impact audit rather than just a file inventory, or wants better stats,
  visuals, and deterministic recommendations for instruction-file hygiene.
---

# Instruction & Skill Optimizer

Audit, explain, and clean up instruction files and skill installs across the machine.

The upgraded goal is not just to find large files. It is to answer the operational questions that actually matter:

- What exists on disk?
- What likely loads together in a real session?
- Which files are exact duplicates, near duplicates, or just semantically overlapping?
- Which copy is the likely source of truth?
- Which files are safe delete/archive candidates versus active runtime burden?
- How should a user manage, merge, split, or regenerate skill copies across runtimes?

## Safety default

**Phases 0–7 are analysis-only.** They may write JSON and markdown outputs, but do not modify target instruction files.

**Phase 8 (Execute)** is the only phase that changes user files. It requires explicit user approval for each batch.

Never claim that all discovered files load together. Always separate:
1. disk footprint
2. possible runtime load
3. likely session stack
4. on-demand skill/reference loading

## Feedback loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior runs.

1. Detect — note what the audit missed or overclaimed.
2. Search — check `FEEDBACK.md` for the same issue.
3. Scope — one actionable observation per entry.
4. Draft-and-ask — propose the entry to the user.
5. Write-on-approval — append only if the user approves.
6. Compact-at-75 — merge duplicates and archive resolved entries.

## Modes

Pick the lightest mode that answers the user's question.

### 1. `fast-audit`
Use when the user wants a quick snapshot.

Runs:
- discovery
- exact duplicate clustering
- basic stats

### 2. `session-impact`
Use when the user wants to know what actually loads together.

Runs:
- discovery
- load-stack simulation
- runtime/session visuals
- heavy stack summary

### 3. `skill-library`
Use when the user wants to manage skills across runtimes.

Runs:
- discovery
- exact + near duplicate clustering
- skill topology analysis
- canonical-source scoring
- merge/delete planning for skills

### 4. `delete-candidates`
Use when the user wants cleanup candidates.

Runs:
- discovery
- canonical-source scoring
- delete-candidate scoring
- live-state validation
- delete safety report

### 5. `merge-planning`
Use when the user wants canonical-source and merge plans.

Runs:
- discovery
- exact + near duplicate clustering
- canonical-source scoring
- skill topology analysis
- action scoring recommendations

### 6. `full-audit`
Use for the complete pipeline.

Runs all phases 0–7 and produces the richest report set.

## Progressive disclosure: what to load

Load only the references needed for the active phase.

| Reference | Load when... |
|---|---|
| `FEEDBACK.md` | **Always** |
| `references/analysis-guide.md` | Discovery/inventory/bloat/staleness analysis |
| `references/runtime-load-models.md` | Session-impact or load-stack questions |
| `references/similarity-guide.md` | Duplicate / near-duplicate / semantic overlap analysis |
| `references/directive-schema.md` | Directive extraction and instruction-count work |
| `references/conflict-taxonomy.md` | Contradiction / override / drift analysis |
| `references/action-scoring.md` | Merge/archive/delete recommendation work |
| `references/skill-topology.md` | Cross-runtime skill management |
| `references/reporting-guide.md` | Final report and visuals |
| `references/delegation-guide.md` | Execute phase only |

## Outputs the skill should prefer

This skill should produce machine-readable facts first, then narrative and visuals.

### JSON outputs
- `inventory.json`
- `load-stacks.json`
- `duplicate-clusters.json`
- `similarity-clusters.json`
- `directive-index.json`
- `conflicts.json`
- `canonical-sources.json`
- `delete-candidates.json`
- `merge-plans.json`
- `skill-topology.json`
- `stats-summary.json`
- `visual-data.json`

### Human outputs
- executive markdown manifest
- load-stack diagrams
- duplicate-cluster diagrams
- skill-topology diagrams
- session-impact matrix
- delete-candidate dashboard
- before/after savings summary

## Pipeline overview

```text
Phase 0: Discovery
Phase 1: Inventory
Phase 2: Load Stack Simulation
Phase 3: Similarity Analysis
Phase 4: Directive Extraction + Conflict Detection
Phase 5: Canonical Source + Action Scoring
Phase 6: Skill Topology Analysis
Phase 7: Reporting + Visuals
Phase 8: Execute (approved only)
```

## Phase details

### Phase 0 — Discovery
Run `scripts/discover_instructions.py`.

Purpose:
- find instruction files on disk
- record runtime, scope, project root, path kind, content hash, and existence state

### Phase 1 — Inventory
Build the base inventory and summary stats.

Use:
- `scripts/build_stats_summary.py`

Purpose:
- total files, tokens, largest files
- per-runtime and per-directory burden
- baseline machine snapshot

### Phase 2 — Load Stack Simulation
**Load `references/runtime-load-models.md`.**

Use:
- `scripts/simulate_load_stacks.py`

Purpose:
- model plausible stacks per runtime + project root
- separate disk totals from actual likely session burden
- flag overloaded stacks

Important: do not imply every discovered file loads in one session.

### Phase 3 — Similarity Analysis
**Load `references/similarity-guide.md`.**

Use:
- `scripts/cluster_exact_duplicates.py`
- `scripts/cluster_near_duplicates.py`

Purpose:
- exact duplicates via content hash
- near duplicates via deterministic similarity heuristics
- semantic-overlap analysis only with caution and confidence labels

### Phase 4 — Directive Extraction + Conflict Detection
**Load `references/directive-schema.md` and `references/conflict-taxonomy.md`.**

Use:
- `scripts/extract_directives.py`
- `scripts/detect_conflicts.py`

Purpose:
- estimate instruction counts more meaningfully than token counts alone
- find repeated policies, contradictions, and drift
- identify what should move into references or skills

### Phase 5 — Canonical Source + Action Scoring
**Load `references/action-scoring.md`.**

Use:
- `scripts/score_canonical_sources.py`
- `scripts/score_delete_candidates.py`

Purpose:
- identify likely source-of-truth files
- distinguish delete-now vs archive-first vs review-required
- assign primary action recommendations like KEEP / MERGE / EXTRACT / DELETE

### Phase 6 — Skill Topology Analysis
**Load `references/skill-topology.md`.**

Use:
- `scripts/analyze_skill_topology.py`

Purpose:
- understand source skill vs runtime installs vs mirrors vs generated copies
- show drift and redundant installs across runtimes

### Phase 7 — Reporting + Visuals
**Load `references/reporting-guide.md`.**

Use:
- `scripts/render_manifest.py`
- `scripts/render_visual_data.py`

Preferred visuals:
- load-stack Mermaid diagrams
- duplicate-cluster Mermaid diagrams
- skill-topology Mermaid diagrams
- datatables for delete candidates and stack matrixes
- before/after savings charts where possible

### Phase 8 — Execute
**Load `references/delegation-guide.md`.**

Only after user approval.

Execution batches should:
- group by action type
- start with highest-confidence safe candidates
- revalidate existence before edits/deletes
- preserve one canonical source before removing duplicates
- report after each batch

## Deterministic action classes

Every file or cluster should end with one primary recommendation:
- KEEP
- MERGE
- EXTRACT
- SPLIT
- ARCHIVE
- DELETE
- REGENERATE
- REWRITE

Each recommendation should include:
- confidence
- risk
- token savings estimate
- directive savings estimate where possible
- why this action is recommended

## Visuals to generate when useful

Prefer visuals heavily. This skill benefits from pictures more than prose.

### Use Mermaid for:
- load-stack chains
- duplicate clusters
- skill topology maps
- conflict maps

### Use tables for:
- delete candidates
- per-runtime stack matrix
- per-file stats
- skill inventory

### Use charts for:
- token burden by runtime
- duplicate waste by cluster
- before/after savings estimates
- heavy-stack ranking

## What this skill does NOT do

- It does not assume all discovered files load together.
- It does not treat semantic overlap as safe deletion evidence.
- It does not delete files automatically.
- It does not optimize arbitrary prompts that are not part of instruction/skill ecosystems.
- It does not rewrite whole skills unless the user explicitly asks for execution.

## Quick-start recipes

### If the user says “what’s actually loading?”
1. Run discovery
2. Run load-stack simulation
3. Show a session-impact matrix and 3–5 stack diagrams

### If the user says “which skills are duplicated?”
1. Run discovery
2. Run exact + near duplicate clustering
3. Run skill topology analysis
4. Show duplicate clusters and likely canonical sources

### If the user says “what can I delete?”
1. Run discovery
2. Run delete scoring
3. Revalidate live state
4. Show delete-now / probably-delete / archive-first buckets

### If the user says “clean up everything”
1. Run full audit
2. Present manifest and visuals
3. Get approval for execution batches
4. Execute in order of confidence and reversibility

## Eval guidance for improving this skill

This skill should be evaluated like a product, not just edited by taste.

Use fixtures covering:
- exact duplicate clusters
- near-duplicate variants
- semantic-overlap-but-not-delete-safe cases
- active project stacks
- archive/vendor/mirror junk
- stale deleted-tree scenarios
- source skill + runtime install topologies
- contradictory instruction chains

Key success metrics:
- exact duplicate precision
- near-duplicate precision
- canonical-source accuracy
- delete recommendation precision
- session-stack simulation usefulness
- stale-state revalidation correctness
