---
name: Skill-Lib-Cleanup
description: >
  Use when auditing, deduplicating, merging, pruning, or reorganizing skills, agents, plugins,
  commands, or rules across AI runtimes on the machine. Also use for requests like "clean up my
  skills," "which skills overlap," "merge similar skills," "skill inventory," "drifted skills,"
  or any rollback-safe cross-location library maintenance or consolidation task.
---

# Skill Library Curator

Systematic audit and maintenance pipeline for a growing AI agent skill library.
Treats skills as composable infrastructure — not disposable prompts — and
applies conservative, reversible decisions.

Works across all agent runtimes: Claude Code, Codex CLI, Factory/Droid,
Cursor, Gemini CLI, AntiGravity, Kiro, Craft Agent, Osaurus, and Claude.ai.
Discovers skills, agents/droids, plugins, commands, and rules in every
location (global and project-local), compares versions across them, and
produces a unified audit with optional visual reports.

## Safety Default

**Phases 0-7 are read-only analysis.** They read files, run scripts, and
produce reports — nothing is modified, moved, or deleted. Phase 8 (Execute)
is the only phase that changes anything, and it requires explicit user
approval for every action. The default output is a recommendation report,
not an execution.

## Analysis Scope: Per-Location, Then Global

Recommendations are scoped to individual agent runtimes first, then
cross-referenced globally. A UI skill in Claude Code and a UI skill in
Codex CLI serve different agents with different capabilities — they are
not duplicates just because they share a domain.

- **Within-location analysis** (Phases 3-6): Similarity scanning, health
  checks, and action plans are generated *per agent runtime*. A merge
  recommendation only applies to skills within the same location.
- **Cross-location analysis** (Phase 2): Compares the *same* skill across
  locations to detect drift. This is about version consistency, not
  functional deduplication.
- **Global view**: The final report shows both per-location findings and
  a cross-location drift summary, but never recommends merging skills
  across different agent runtimes.

## Entity Type Taxonomy

The discovery script classifies every item into one of these entity types:

| Type | File Pattern | What It Is |
|------|-------------|------------|
| **skill** | `SKILL.md` in a named directory | Reusable instruction set loaded on demand |
| **agent** | `.md` files in `agents/` or `droids/` | Autonomous entity with its own system prompt, tools, and model |
| **command** | `.md` files in `commands/` | Slash command binding (e.g., `/commit` → `commit.md`) |
| **rule** | `.mdc` or `.md` files in `rules/` | Always-on or glob-triggered constraint (Cursor convention) |
| **plugin** | `plugin.json` in `.codex-plugin/` or `.factory-plugin/` | Installable distribution unit bundling skills + config |
| **profile** | Profile JSON in `profiles/` | Configuration preset selecting skills/settings/model |
| **context** | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` | Project-level instruction file for an agent runtime |

### Scope Classification

Every item is classified as either **global** or **project-local**:

- **Global** (`~/.<framework>/...`): User-level items available across all
  projects. These are the primary audit targets for deduplication and sync.
- **Project-local** (`<project>/.agents/skills/`, `<project>/.claude/skills/`,
  etc.): Items tied to a specific project. These are cataloged and reported
  but **never recommended for cross-project merge**. They serve their project
  and should be left alone unless the user explicitly wants to promote them
  to global scope.

### Framework Conventions (Quick Reference)

| Framework | Context File | Skill Dir | Agent Dir |
|-----------|-------------|-----------|-----------|
| Claude Code | `CLAUDE.md` | `.claude/skills/` | `.claude/agents/` |
| Codex CLI | `AGENTS.md` | `.agents/skills/` | — |
| Factory/Droid | `AGENTS.md` | `.factory/skills/` | `.factory/droids/` |
| Cursor | `.cursor/rules/*.mdc` | `.cursor/skills/` | — |
| Gemini CLI | `GEMINI.md` | `.gemini/skills/` | — |
| AntiGravity | `.antigravity/rules/` | `.antigravity/skills/` | — |
| Kiro | — | `.kiro/skills/` | — |
| Craft Agent | `CLAUDE.md` | workspace `skills/` | — |
| Osaurus | — | `~/.osaurus/skills/` | `~/.osaurus/Tools/` |

## Feedback Loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior audits.

1. **Detect** — After completing an audit, note anything that went wrong: a
   merge that lost nuance, a false duplicate, a missing edge case, a category
   that doesn't fit.
2. **Search** — Check `FEEDBACK.md` for existing entries on the same issue.
3. **Scope** — One actionable observation per entry.
4. **Draft-and-ask** — Propose the entry: "I noticed [issue]. Want me to log this?"
5. **Write-on-approval** — Append with date and category tag.
6. **Compact-at-75** — Merge duplicates, promote patterns to reference files,
   archive resolved. Reset to ~30 entries.

## Philosophy

The goal is not to minimize skill count. The goal is to maximize routing
clarity, reduce trigger collisions, eliminate redundancy, and keep
maintenance burden proportional to value delivered. A library of 30 sharp,
well-routed skills beats 15 bloated ones.

## Pipeline Overview

```
Phase 0: Discovery         → Find all entity locations, resolve symlinks, build environment map
Phase 1: Inventory         → Extract metadata from all entities (scripted + parallel subagents)
Phase 2: Cross-Location    → Compare same entities across locations, detect drift
Phase 3: Relationship Map  → Detect pairs, overrides, dependencies, command bindings
Phase 4: Similarity Scan   → Cluster by function, flag duplicates and near-dupes
Phase 5: Health Check      → Staleness, bloat, trigger collisions, quality
Phase 6: Action Plan       → Classify every skill with one action + rationale
Phase 7: Visualize         → Generate charts (runtime distribution, drift, health heatmap, bloat)
Phase 8: Execute           → Merge, rewrite, archive — only with user approval
```

## How to Run

### Phase 0: Discovery & Environment Map

Before reading any skills, map the entire skill landscape on the machine.

**Run the discovery script:**

```bash
python3 scripts/discover_skills.py --all --output /tmp/skill-discovery.json
```

The `--all` flag scans global skill directories AND common project roots
(~/LocalDev, ~/Developer, ~/Documents/Projects*) for project-local skills.
Without `--all`, only global directories are scanned.

**Global skill directories (always scanned):**

| Location | Agent Runtime | Entity Types |
|----------|--------------|-------------|
| `~/.agents/skills/` | global-pool | skills |
| `~/.claude/skills/` | claude-code | skills |
| `~/.claude-profiles/skills/` | claude-code | skills |
| `~/.claude/agents/` | claude-code | agents |
| `~/.claude/commands/` | claude-code | commands |
| `~/.factory/skills/` | factory | skills |
| `~/.factory/droids/` | factory | droids |
| `~/.factory/commands/` | factory | commands |
| `~/.codex/skills/` | codex-cli | skills |
| `~/.kiro/skills/` | kiro | skills |
| `~/.cursor/skills-cursor/` | cursor | skills |
| `~/.cursor/rules/` | cursor | rules |
| `~/.gemini/skills/` | gemini-cli | skills |
| `~/.gemini/antigravity/skills/` | antigravity | skills |
| `~/.osaurus/skills/` | osaurus | skills |
| `~/.craft-agent/workspaces/*/skills/` | craft-agent:* | skills |
| `~/.craft-agent-phone/workspaces/*/skills/` | craft-agent-phone:* | skills |
| `~/.agents/profiles/` | global-pool | profiles |

**Project-local patterns (scanned with `--all` or `--scan-projects`):**

The script searches one level deep inside project roots for:
`.agents/skills/`, `.claude/skills/`, `.factory/skills/`, `.cursor/skills/`,
`.gemini/skills/`, `.antigravity/skills/`, `.kiro/skills/`, `.claude/agents/`,
`.agents/agents/`, `.factory/droids/`

Project-local items are tagged with `scope: "project-local"` and include
the `project_root` path for grouping. They are reported separately from
global items and never recommended for cross-location merge.

For each item found, the script extracts: name, directory, entity_type
(skill/agent/command/rule), scope (global/project-local), path, canonical
path (symlink-resolved), agent runtime, modification time, content hash
(SHA256), line count, reference file count, script count, and FEEDBACK.md
presence.

To scan specific project directories:

```bash
python3 scripts/discover_skills.py --scan-projects ~/MyProjects ~/Work --output /tmp/skill-discovery.json
```

To add additional global skill paths:

```bash
python3 scripts/discover_skills.py --all --paths ~/custom/skills --output /tmp/skill-discovery.json
```

**On Claude.ai** (no filesystem scripts): Skip Phase 0. Use `/mnt/skills/user/`
as the single target directory and proceed to Phase 1 with manual reads.

Review the discovery output summary (by_entity_type, by_scope, by_runtime)
to understand: how many directories exist, which runtimes are present,
how many total items were found, and how many are project-local. This sets
the scope for all subsequent phases.

### Phase 1: Inventory

Extract metadata from every discovered skill.

**Run the inventory script:**

```bash
python3 scripts/inventory_to_json.py /tmp/skill-discovery.json --output /tmp/skill-inventory.json
```

This parses every SKILL.md frontmatter and extracts: name, description, trigger
phrases, supersedes declarations, section count, plus all discovery metadata.

**For libraries over 30 skills, parallelize the deep read:**

Dispatch subagents in batches of ~20 skills. Each subagent reads the full
SKILL.md content (not just frontmatter) for its batch and returns structured
analysis — scope signals, tools referenced, models assumed, platforms targeted.

- **Craft Agent**: Use the `Agent` tool with `subagent_type: "Explore"`
- **Claude Code**: Use the `Task` tool
- **Claude.ai**: Read sequentially (no subagent support)

Merge subagent results with the inventory JSON to produce the complete
inventory dataset.

**Also run the freshness report:**

```bash
python3 scripts/freshness_report.py /tmp/skill-discovery.json --flagged-only --output /tmp/skill-freshness.json
```

This flags: skills not modified in >90 days, skills without FEEDBACK.md, and
skills referencing obsolete model names (Claude 3.x/3.5, Sonnet 3, Opus 4.1, GPT-4/GPT-4 Turbo/GPT-4o, Gemini 1.5/2.0, etc.).

**Also run the token savings estimator:**

```bash
python3 scripts/token_savings.py /tmp/skill-discovery.json --output /tmp/token-savings.json
```

This computes the cost of having an LLM read everything vs. using scripts.
Typical savings: 90%+ of tokens (varies by library size). The output feeds into
the dashboard visualization (Phase 7).

### Phase 2: Cross-Location Analysis

Compare same-named skills across agent locations to detect drift and orphans.

**Run the cross-location diff script:**

```bash
python3 scripts/cross_location_diff.py /tmp/skill-discovery.json --output /tmp/skill-xdiff.json
```

This groups skills by directory name and classifies each group as:

| Status | Meaning |
|--------|---------|
| **symlinked** | All copies point to the same file (no drift possible) |
| **identical** | Independent copies with matching content hashes |
| **drifted** | Different versions exist across locations — needs attention |
| **singleton** | Exists in only one location |

For drifted skills, the script reports which location has the newest version
and which copies are stale. It also detects **renamed duplicates** — skills
with different directory names but identical SKILL.md content (same hash).
This catches cases where a skill was forked under a new name without
meaningful changes. Use the cross-location report to identify:

- Skills that were updated in one location but not propagated
- Skills that diverged independently (different edits in different places)
- Orphaned skills that exist in only one agent's directory

**Skillsync awareness:** If `~/.craft-agent/shared/skill-sync/manifest.json`
exists, check which drifted skills are in the sync manifest. Drifted skills
that are managed by skillsync should be synced rather than manually fixed.
Run `~/.craft-agent/shared/skill-sync/sync.sh --status` to check current
sync state.

Include the cross-location report in the audit output. Drifted skills are
not the same as duplicates — they need sync, not merge.

### Phase 3: Relationship Map

This is the phase most audit approaches skip, and it's where false merges
happen. Before comparing skills for similarity, map their relationships.

**Load `references/analysis-framework.md` now.** It contains the full
relationship taxonomy and decision tests.

Identify:

- **Designed pairs**: Skills explicitly designed to work together (e.g.,
  design-maestro + userinterface-wiki own aesthetics vs animation
  engineering). These are NOT merge candidates — they're complementary.
- **Override chains**: User skills that supersede public/example skills
  (e.g., docx-enhanced overrides public docx). The override is the keeper.
- **Command bindings**: Skills bound to slash commands in the user's system
  prompt (e.g., /game → game-dev). These have external dependencies.
- **Router references**: Skills referenced in the user's system prompt
  routing table, preference rules, or conditional loading instructions.
- **Dependency clusters**: Skills that reference each other's outputs or
  assume each other exists (e.g., skill-review references skill-creator
  conventions).
- **Platform-scoped skills**: Skills targeting specific platforms (Claude.ai
  artifacts, Claude Code, Codex CLI, OpenClaw) — same domain doesn't mean
  same skill if the platform context changes behavior.
- **Cross-location copies**: Skills that exist in multiple agent runtimes.
  These are distribution relationships, not functional ones — handle via
  sync, not merge.

### Phase 4: Similarity Scan

Now compare skills for functional overlap **within each agent runtime
separately**. A skill in Claude Code and a skill in Codex are not candidates
for merging — they serve different agents. Only compare skills that live in
the same location.

**Load `references/analysis-framework.md` if not already loaded** — use the
similarity decision matrix.

For each skill pair within the same location, evaluate using the weighted
similarity matrix in `references/analysis-framework.md` (section: Similarity
Decision Matrix). The matrix covers 7 dimensions with weighted scoring —
refer to it directly rather than using a simplified checklist here.

Quick reference for classification:
- Weighted score 12-14: Near-certain duplicate — strong merge candidate
- Weighted score 8-11: Significant overlap — inspect manually
- Weighted score 4-7: Adjacent but distinct — keep separate
- Weighted score 0-3: Unrelated
- Trigger overlap alone (without workflow overlap) → **Trigger collision**,
  not a merge candidate. Fix descriptions instead.

**Important:** When comparing skills that appear in multiple locations
(detected in Phase 2), compare *unique* skills only — don't score the same
skill against itself across locations. Use the cross-location report to
deduplicate before similarity scanning.

Group skills into families:
- Exact duplicates (same skill, different names or locations)
- Version chains (v1 → v2 → final patterns)
- Near-duplicates (same job, minor wording/example differences)
- General/specialist pairs (one broad, one narrow — keep both if the
  specialist adds real value)
- Designed complements (explicitly paired — never merge)
- Singletons (no close relatives)

### Phase 5: Health Check

Evaluate every skill on these dimensions. Flag issues but don't
auto-recommend removal based on flags alone.

Use the freshness report from Phase 1 (`scripts/freshness_report.py`) to
inform staleness assessment — it provides concrete modification dates and
stale model detection rather than guessing from content alone.

**Staleness indicators:**
- References obsolete models (flagged by freshness script)
- References deprecated tools or APIs
- References workflows the user no longer uses
- No FEEDBACK.md (flagged by freshness script)
- Contradicts current user preferences or system prompt conventions
- Not modified in >90 days AND has no unique job (stale + replaceable)

**Bloat indicators:**
- SKILL.md exceeds 500 lines without reference files absorbing detail
- Tries to handle 3+ distinct jobs in one skill
- Has reference files that are never loaded or referenced
- Has scripts that duplicate what Claude can do natively
- Mixes system prompt policy with task-specific workflow

**Trigger health:**
- Description is vague or overly broad (triggers on too many queries)
- Description is too narrow (misses obvious use cases)
- Description collides with another skill's trigger space
- Missing "supersedes" declaration when it should have one
- Missing "don't use when" boundary

**Quality signals (positive):**
- Clean progressive disclosure (metadata → SKILL.md → references)
- References are well-organized and actually loaded during use
- Scripts handle deterministic work that would waste LLM tokens
- Description functions as routing logic, not marketing copy
- Has FEEDBACK.md with real entries

### Phase 6: Action Plan

For every unique skill **within each agent runtime**, assign exactly one
action. Group the action plan by location — the user needs to see what
changes apply where. **Load `references/merge-protocol.md` now** for merge
execution guidance.

| Action | When to use | Confidence threshold |
|--------|-------------|---------------------|
| **KEEP** | Distinct, healthy, well-routed | — |
| **KEEP + REWRITE** | Valuable workflow but poor structure, stale refs, or bad routing | — |
| **MERGE INTO [target]** | Same job as another skill; combine best parts | ≥ 0.75 |
| **ARCHIVE** | Superseded but might have recoverable value, or confidence < 0.75 | ≥ 0.50 |
| **REMOVE** | Exact duplicate, broken skeleton, empty shell, stale cache copy | ≥ 0.90 |
| **SPLIT** | One skill hiding 2+ distinct jobs with different triggers | — |
| **FIX TRIGGERS** | Healthy skill with a routing/description problem | — |
| **SYNC** | Drifted copies detected — propagate the newest version | — |

Decision safeguards (each prevents a specific class of audit damage):
- Preserve the only skill serving a niche task — removing it leaves a
  coverage gap with no fallback
- Keep designed pairs and complementary skills separate — merging them
  collapses intentional domain boundaries
- Keep skills bound to different slash commands separate — merging breaks
  the user's command muscle memory
- Preserve unique examples, edge-case handling, or specialized scripts
  unless fully accounted for in the merge target — lossy merges destroy
  the hardest-won content
- Prefer archive over remove when confidence is below 0.90 — archiving
  is reversible, deletion is not
- Keep skills targeting different platforms separate — same domain does
  not mean same skill when platform context changes behavior
- When uncertain, mark NEEDS_REVIEW and ask the user — false merges
  destroy more value than keeping an extra skill
- For drifted skills, default to SYNC rather than merge or remove —
  drift is a distribution problem, not a duplication problem

Present the action plan as a table:

| Skill | Category | Action | Target | Reason | Confidence |
|-------|----------|--------|--------|--------|------------|

Follow with:
- Merge group details (what each skill contributes, what gets preserved)
- Archive rationale for each archived skill
- Proposed final library (the end-state canonical set)
- Impact on system prompt routing table (commands, routing rules, override
  declarations that need updating)
- Cross-location sync plan (which skills need propagating where)

### Phase 7: Visualize (Optional)

Generate visual charts from the audit data. These are useful for presenting
findings to the user and identifying patterns at a glance.

**Run the visualization script:**

```bash
python3 scripts/visualize_audit.py \
    --discovery /tmp/skill-discovery.json \
    --inventory /tmp/skill-inventory.json \
    --freshness /tmp/skill-freshness.json \
    --xdiff /tmp/skill-xdiff.json \
    --output-dir /tmp/audit-viz/
```

This generates 6 PNG charts:

| Chart | What it shows |
|-------|--------------|
| `runtime_distribution.png` | Horizontal bar chart of items per agent runtime |
| `entity_types.png` | Pie chart of skill vs agent vs command vs rule |
| `scope_split.png` | Stacked bar: global vs project-local per runtime |
| `drift_status.png` | Donut chart of identical/symlinked/drifted/singleton |
| `health_heatmap.png` | Heatmap of health flags (stale, no feedback, stale models) by runtime |
| `bloat_analysis.png` | Scatter plot of line count vs references, bubble-sized by scripts |

Requires `matplotlib` (`pip3 install matplotlib`). Falls back to text-based
ASCII summary if matplotlib is unavailable.

Present charts inline using `image-preview` code blocks. **Important:** When
running inside Craft Agent, use the session's `dataFolderPath` as the
output directory (not `/tmp/`) so the app can access the files:

```bash
python3 scripts/visualize_audit.py \
    --discovery /tmp/skill-discovery.json \
    --inventory /tmp/skill-inventory.json \
    --freshness /tmp/skill-freshness.json \
    --xdiff /tmp/skill-xdiff.json \
    --output-dir "$DATA_FOLDER_PATH"
```

Then reference charts via their full path in image-preview blocks:

````
```image-preview
{
  "title": "Audit Charts",
  "items": [
    {"src": "/full/path/to/data/runtime_distribution.png", "label": "By Runtime"},
    {"src": "/full/path/to/data/drift_status.png", "label": "Drift"},
    {"src": "/full/path/to/data/health_heatmap.png", "label": "Health"}
  ]
}
```
````

#### Interactive Dashboard (HTML)

Generate one HTML dashboard to present the audit data visually. Pick
whichever layout best fits the data — only one is needed by default.

| Layout | Style | Best for |
|--------|-------|----------|
| **Notion** | Flat white page, property tables, inline icons, hover highlights | Clean readability, minimal visual noise |
| **Craft** | Bento card grid, coral accents, CSS donut charts, hover lift | Visual density with Apple/Craft.do polish |
| **Editorial** | 4-col bento grid, terracotta/teal accents, warm typography | Editorial warmth with data density |

All three are single-file HTML with **no JavaScript** (sandboxed iframes
block it). Use Lucide inline SVG icons (never emoji). CSS-only animations
via transitions and hover states. Data is pre-baked from audit JSON outputs.
Max-width 1100px, bento grid layout, varied card spans.

Each dashboard should include these cards:
- Overview metrics (total entities, unique, drifted, token savings)
- Runtime distribution (horizontal bars)
- Drift status (CSS conic-gradient donut)
- Health signals (status dots + counts)
- Most drifted list (compact, 8-10 entries)
- Token economics (savings percentage + per-phase bars)

Generate via subagent or inline, write to the session data folder, and
present via `html-preview`:

````
```html-preview
{
  "src": "/path/to/dashboard.html",
  "title": "Skill Audit Dashboard"
}
```
````

### Phase 8: Execute

Only after the user approves the plan.

For each approved merge:
1. Read `references/merge-protocol.md` for the merge procedure
2. Create the canonical merged skill in a working directory
3. Preserve provenance (list source skills in a comment block)
4. Package as `.skill` file via skill-creator's packaging script if available
5. Present for user installation

For approved archives:
1. Move to `skills/_archived/` (or note for the user if read-only)
2. Record what's being archived and why

For trigger fixes:
1. Rewrite the description with proper routing boundaries
2. Update the skill in place (or package as `.skill` file)

For sync actions:
1. Identify the newest version (from cross-location report)
2. If skillsync manages the skill, run `sync.sh` to propagate
3. If not in skillsync, manually copy the newest version to all locations
4. Verify with `scripts/cross_location_diff.py` after sync

After execution, prompt the user about:
- Running `~/.craft-agent/shared/skill-sync/sync.sh` to propagate changes
  to other Craft Agent workspaces
- FEEDBACK.md entries for lessons learned

## Output Format

The final deliverable has these sections:

1. **Executive Summary** — Total items (per location, entity type, and unique),
   families found, drifted count, proposed end-state count, key actions
2. **Environment Map** — All directories discovered, agent runtimes, entity
   types, total counts per location, global vs project-local split
3. **Cross-Location Report** — Drifted items, orphans, sync recommendations
4. **Project-Local Catalog** — Items grouped by project root, noted but not
   recommended for merge (these serve their specific project context)
5. **Inventory Table** — Every unique global skill with metadata and action
6. **Relationship Map** — Designed pairs, override chains, command bindings
7. **Similarity Clusters** — Duplicate families with merge reasoning
8. **Health Findings** — Staleness, bloat, trigger issues (with freshness data)
9. **Action Plan** — The decision table with rationale
10. **Merge Proposals** — For each merge group: what's kept, what's dropped,
    what the canonical skill looks like
11. **Visual Reports** — Charts from `visualize_audit.py` (runtime distribution,
    entity types, scope split, drift status, health heatmap, bloat analysis)
12. **System Prompt Impact** — Routing table changes, command rebindings,
    preference updates needed
13. **Migration Checklist** — Ordered steps including cross-location sync

## Scripts

All scripts are in the `scripts/` directory. They handle deterministic work
that would otherwise waste LLM tokens on repetitive file reads.

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `discover_skills.py` | Find all skills, agents, commands, rules across all runtimes; classify entity types and scope (global vs project-local) | `--all` flag or custom paths | JSON with all entities and metadata |
| `inventory_to_json.py` | Parse frontmatter: name, description, triggers, supersedes, platform signals | Discovery JSON | Enriched inventory JSON |
| `cross_location_diff.py` | Compare entities across locations: drift, renamed duplicates, project-local summary | Discovery JSON | Cross-location report JSON |
| `freshness_report.py` | Flag stale items, missing FEEDBACK.md, obsolete model refs (incl. Claude 3.x/3.5, Sonnet 3, Opus 4.1, GPT-4/Turbo/GPT-4o, Gemini 1.5/2.0) | Discovery JSON | Freshness report JSON |
| `visualize_audit.py` | Generate 6 PNG charts: runtime distribution, entity types, scope split, drift donut, health heatmap, bloat scatter | All 4 JSONs above | PNG files + manifest.json |
| `token_savings.py` | Estimate LLM token savings from using scripts vs. reading everything | Discovery JSON | Token savings JSON (tokens, cost, per-phase breakdown) |

Run them in order: discover (Phase 0) → inventory + freshness in parallel
(Phase 1) → cross-location (Phase 2) → visualize (Phase 7). Each script
supports `--help` for all options. Note: content hashes cover SKILL.md only
— drift in reference files or scripts within a skill directory won't be
detected by the diff.

## What This Skill Does NOT Do

- Does not run skills against test cases (use skill-creator for that)
- Does not optimize individual skill descriptions (use skill-creator's
  description optimization loop)
- Does not produce deep single-skill quality audits (use skill-review)
- Does not auto-delete files without user approval
- Does not modify the user's system prompt directly
- Does not handle per-agent deny/allow lists (use skill-manager for that)
