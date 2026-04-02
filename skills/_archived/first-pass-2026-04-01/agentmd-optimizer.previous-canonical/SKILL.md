---
name: agentmd-optimizer
description: >
  Scan the entire machine for CLAUDE.md, AGENTS.md, GEMINI.md, and other agent
  instruction files, then analyze them for token bloat, redundancy, staleness,
  hierarchy conflicts, and drift. Produces a token-saving manifest with
  per-file recommendations and orchestrates sub-agent cleanup using cheap
  models as workforce. Use this skill whenever the user mentions optimizing
  instructions, reducing context tokens, cleaning up CLAUDE.md files, auditing
  agent configs, finding redundant instructions, or wants to slim down what
  gets loaded on every agent launch. Also use when the user says "my context is
  too big", "too many instructions", "tokens are expensive", or "clean up my
  instruction files". Works on any machine — no hardcoded paths.
---

# Instruction Optimizer

Systematically discover, audit, and optimize every agent instruction file on the
machine. The goal: minimize tokens loaded on every agent launch while preserving
the instructions that actually matter.

## Why This Exists

Agent instruction files (CLAUDE.md, AGENTS.md, GEMINI.md) are loaded into context
on every conversation start. Every unnecessary line costs real money at scale and
dilutes the model's attention on instructions that matter. Research shows frontier
models reliably follow ~150-200 individual instructions — beyond that, compliance
degrades uniformly. This skill finds the bloat and tells you exactly what to cut.

## Safety Default

**Phases 0-4 are read-only analysis.** Nothing is modified. Phase 5 (Execute) is
the only phase that changes files, and it requires explicit user approval for every
batch. The default output is a recommendation manifest, not an execution.

## Feedback Loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior runs.

1. **Detect** — After an audit, note anything off: a false positive, a missed
   redundancy, a hierarchy call that was wrong, a recommendation that lost nuance.
2. **Search** — Check `FEEDBACK.md` for existing entries on the same issue.
3. **Scope** — One actionable observation per entry.
4. **Draft-and-ask** — Propose the entry: "I noticed [issue]. Want me to log this?"
5. **Write-on-approval** — Append with date and category tag.
6. **Compact-at-75** — Merge duplicates, archive resolved. Reset to ~30 entries.

## What Gets Scanned

### Instruction File Types

| File | Runtime | Loaded When |
|------|---------|-------------|
| `CLAUDE.md` | Claude Code, Craft Agent | Every conversation in that directory or below |
| `AGENTS.md` | Codex CLI, Factory/Droid | Every conversation in that directory or below |
| `GEMINI.md` | Gemini CLI | Every conversation in that directory or below |
| `.cursor/rules/*.mdc` | Cursor | Per glob pattern or always-on |
| `.antigravity/rules/*.md` | AntiGravity | Per configuration |
| Custom Instructions | ChatGPT | Every conversation (user-level) |

### Hierarchy (Precedence Order)

Instruction files form a precedence chain. Later entries override earlier ones:

```
1. Global user-level     ~/.claude/CLAUDE.md, ~/.agents/AGENTS.md, etc.
2. Project root          /path/to/project/CLAUDE.md
3. Project .claude/      /path/to/project/.claude/CLAUDE.md
4. Subdirectory          /path/to/project/packages/api/CLAUDE.md
5. Conversation context  (skills, agents loaded on-demand — NOT always-loaded)
```

**The key insight:** Information that only matters for specific tasks should live
in skills (loaded on-demand), not in instruction files (loaded every time). Every
line in a CLAUDE.md is a line the model reads on every single conversation start.

## Progressive Disclosure: What to Load

| Reference | Load when... |
|---|---|
| `FEEDBACK.md` | **Always** — before every use |
| `references/analysis-guide.md` | Running analysis (Phases 2-3) — hierarchy rules, redundancy detection, token counting, staleness checks, cross-platform calibration |
| `references/delegation-guide.md` | Running cleanup execution (Phase 5) — sub-agent orchestration, model selection, batch sizing, prompt templates |

## Pipeline Overview

```
Phase 0: Discovery      → Find every instruction file on the machine
Phase 1: Inventory      → Read each file, extract metadata, count tokens
Phase 2: Hierarchy Map  → Build the precedence chain, detect overrides and drift
Phase 3: Analysis       → Redundancy, staleness, bloat, extractability
Phase 4: Manifest       → Per-file recommendations with token savings estimates
Phase 5: Execute        → Sub-agent cleanup — only with user approval
```

## How to Run

### Phase 0: Discovery

Find every instruction file on the machine.

**Run the discovery script:**

```bash
python3 <skill-path>/scripts/discover_instructions.py --output /tmp/instruction-discovery.json
```

The script scans:
- **Global directories**: `~/.claude/`, `~/.agents/`, `~/.gemini/`, `~/.cursor/`,
  `~/.antigravity/`, `~/.factory/`, `~/.codex/`, `~/.kiro/`
- **Project roots**: `~/LocalDev/`, `~/Developer/`, `~/Projects/`, `~/Documents/`,
  `~/Desktop/`, `~/repos/`, and any additional paths passed via `--scan`
- **Home directory**: `~/CLAUDE.md`, `~/AGENTS.md`, `~/GEMINI.md`
- **Memory directories**: `~/.claude/projects/*/memory/MEMORY.md`

For each file found, the script extracts: path, filename, runtime (claude-code,
codex-cli, gemini-cli, cursor, etc.), scope (global vs project-local), project
root (if applicable), file size, line count, modification date, and content hash.

To scan additional directories:

```bash
python3 <skill-path>/scripts/discover_instructions.py --scan ~/Work ~/Clients --output /tmp/instruction-discovery.json
```

**Review the discovery summary** — total files found, breakdown by runtime and
scope, largest files. This sets the scope for all subsequent phases.

### Phase 1: Inventory

Read each discovered file and extract structured metadata.

For small sets (<20 files), read them sequentially. For larger sets, dispatch
subagents in batches of ~10 files each using `subagent_type: "Explore"` or
Haiku-model agents to minimize cost.

For each file, capture:
- **Token estimate**: line count x 4 (rough tokens-per-line average)
- **Instruction count**: count discrete behavioral directives (each "do X",
  "don't Y", "when X do Y" is one instruction)
- **Section inventory**: headings and what each section covers
- **Staleness signals**: references to obsolete models (Claude 3.x, GPT-4,
  Gemini 1.5), deprecated tools, outdated API patterns
- **Cross-references**: does it reference other files, skills, or tools?
- **Runtime target**: which agent runtime is this written for?

Output: enriched JSON with all metadata per file.

### Phase 2: Hierarchy Map

Build the precedence chain for each project and globally.

**Load `references/analysis-guide.md` now.**

For each project directory that has instruction files:
1. List all instruction files in precedence order (global → project root → subdirectory)
2. Identify **override conflicts** — where a project file restates something the global
   file already says (redundant) or contradicts it (intentional override vs drift)
3. Identify **orphaned globals** — global instructions that no project needs
4. Identify **missing context** — projects that lack instruction files but could
   benefit from them (large codebases with no CLAUDE.md)

Build a hierarchy tree showing which files apply to which directories and how
they layer.

### Phase 3: Analysis

Run each instruction file through the analysis checklist. This is the core phase.

**Keep `references/analysis-guide.md` loaded.**

For each file, evaluate:

#### Token Bloat
- Total token estimate vs recommended ceiling (global: ~800 tokens / ~200 lines,
  project: ~400 tokens / ~100 lines)
- Sections that could be shorter without losing meaning
- Verbose explanations that could be compressed to conditional rules
- Examples or templates that should be in reference files or skills instead
- Comments, whitespace, or formatting that inflates token count

#### Redundancy
- Instructions repeated across multiple files in the same hierarchy chain
- Instructions that restate default agent behavior (the agent already does this)
- Instructions that overlap with loaded skills or plugins
- Copy-pasted blocks that appear in multiple project instruction files

#### Staleness
- References to obsolete models, tools, APIs, or patterns
- Instructions for workflows the user no longer uses
- Dated information that should have been updated
- Links to resources that may no longer exist

#### Extractability
- Instructions that only matter for specific tasks → extract to a skill
- Long reference tables or documentation → extract to a reference file
- Setup/onboarding instructions → extract to a one-time script
- Tool-specific instructions → should live with the tool, not in global context

#### Drift
- Same instruction phrased differently across files (semantic duplicates)
- Contradictions between files at different hierarchy levels
- Instructions that were updated in one file but not propagated to others

#### Calibration (cross-platform)
- ALL-CAPS emphasis that causes overtriggering on Claude 4.5/4.6
- Anti-laziness language ("be thorough", "don't skip steps") that wastes attention
- Personality padding ("you are a world-class expert") that adds no value
- Missing scope boundaries that cause overengineering
- Instructions that work for Claude but would fail on GPT or vice versa

### Phase 4: Manifest

Produce the **Token-Saving Manifest** — the primary deliverable.

Structure it as:

#### 1. Executive Summary
- Total instruction files found
- Total estimated tokens loaded across all files
- Estimated tokens that can be saved
- Percentage reduction achievable
- Top 3 highest-impact changes

#### 2. Per-File Report

For each file, sorted by potential token savings (highest first):

| Field | Content |
|-------|---------|
| **File** | Full path |
| **Runtime** | Which agent runtime |
| **Scope** | Global / project-local |
| **Current tokens** | Estimated token count |
| **Instruction count** | Number of discrete directives |
| **Health** | Healthy / Bloated / Stale / Redundant |
| **Recommended actions** | Numbered list of specific changes |
| **Estimated savings** | Tokens saved if recommendations applied |
| **Priority** | P0 (do now) / P1 (do soon) / P2 (nice to have) |

Each recommended action should be specific and actionable:
- "Remove lines 45-62: restates default Claude Code behavior"
- "Extract lines 80-120 (MCP tool reference table) to a skill reference file"
- "Shorten the 'Code Style' section from 15 lines to 3 conditional rules"
- "Update model references: Claude 3.5 Sonnet → Claude Sonnet 4.6"
- "Remove anti-laziness language on line 23 — causes overtriggering on Opus 4.6"

#### 3. Hierarchy Optimization

For each project with multiple instruction files:
- Show the current hierarchy chain
- Identify what can be deduplicated across levels
- Recommend what should move up (to global) or down (to project-local)
- Flag instructions that should become skills instead

#### 4. Cross-File Drift Report

List all semantic duplicates and contradictions found across files, with
recommended resolution for each.

#### 5. Extraction Candidates

List all content blocks that should be extracted from always-loaded instruction
files into on-demand resources (skills, reference files, scripts), with:
- What to extract
- Where it currently lives
- Where it should go
- Why (token savings + when it's actually needed)

### Phase 5: Execute (User Approval Required)

**Load `references/delegation-guide.md` now.**

Only proceed after the user reviews the manifest and approves specific actions.

#### Sub-Agent Orchestration Strategy

The orchestrator (you, running on the expensive model) coordinates. Cheap models
do the actual file editing. This saves significant cost when cleaning many files.

**Batch formation:**
1. Group files by priority (P0 first, then P1, then P2)
2. Within each priority, group by similarity of changes needed
3. Each batch: 3-5 files with similar change types
4. Each sub-agent gets: the specific files to edit, the exact recommendations
   from the manifest, and clear constraints on what NOT to change

**Sub-agent dispatch (per batch):**

```
You are editing instruction files to reduce token usage.

Files to edit: [list with full paths]

For each file, apply ONLY these specific changes:
[paste the numbered recommendations from the manifest for each file]

Rules:
- Do not add new content. Only remove, shorten, or restructure existing content.
- Preserve the meaning and intent of every instruction you keep.
- When shortening, use conditional form: "When X, do Y" — not imperative commands.
- Do not remove instructions that are unique to this file (not found elsewhere
  in the hierarchy chain).
- After editing, report: lines before, lines after, sections changed.
```

Use `model: "haiku"` or `model: "sonnet"` for the sub-agents. Reserve the
orchestrator model for reviewing results and handling edge cases.

**Verification:**
After each batch completes, the orchestrator:
1. Reads the edited files
2. Verifies no instructions were incorrectly removed
3. Checks that the hierarchy still makes sense
4. Reports results to the user before proceeding to the next batch

**Rollback:** If a batch produces bad results, revert using git or the backup
copies the sub-agents should create before editing.

## What This Skill Does NOT Do

- Does not optimize individual skills (use `skill-lib-cleanup` for that)
- Does not write new instruction files from scratch (use `prompt-architect`)
- Does not auto-edit files without user approval
- Does not evaluate skill triggering or descriptions (use `skill-review`)
- Does not handle ChatGPT Custom Instructions (no filesystem access to those)

## Quick Start

If you just want the fastest path to results:

1. Run the discovery script
2. Read the output summary
3. Ask for Phase 3 analysis on the top 5 largest files
4. Review recommendations
5. Approve and execute on the ones you agree with

For a full audit, run Phases 0-4 sequentially. Phase 5 is always opt-in.
