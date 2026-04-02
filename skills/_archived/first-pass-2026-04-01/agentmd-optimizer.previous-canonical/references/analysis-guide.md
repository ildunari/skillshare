# Analysis Guide

Reference for Phases 2-3 of the Instruction Optimizer. Load this when running
hierarchy mapping and file analysis.

## Hierarchy Rules

### Precedence Chain (Most General → Most Specific)

```
Level 0: Global user-level    ~/.claude/CLAUDE.md
Level 1: Project root         /project/CLAUDE.md
Level 2: Project config dir   /project/.claude/CLAUDE.md
Level 3: Subdirectory          /project/packages/api/CLAUDE.md
Level 4: On-demand             Skills, agents (NOT always-loaded)
```

**Key principle:** Each level should only contain instructions that are NOT
already covered by a higher level. If `~/.claude/CLAUDE.md` says "use TypeScript",
no project-level file needs to repeat that unless it overrides it.

### What Belongs at Each Level

| Level | Should contain | Should NOT contain |
|-------|---------------|-------------------|
| **Global** | Cross-project defaults: code style, response format, behavioral preferences, tool preferences, model-specific calibration | Project-specific details, dependency lists, architecture decisions, team norms |
| **Project root** | Project context: tech stack, architecture decisions, team conventions, important paths, deployment info | Instructions already in global, task-specific workflows, one-time setup steps |
| **Subdirectory** | Module-specific overrides: "this package uses X convention instead of Y", special testing requirements | Anything the project root already covers, general coding practices |
| **On-demand (skills)** | Task-specific workflows, detailed templates, reference tables, tool-specific instructions, domain knowledge | Cross-cutting instructions that should apply to every conversation |

### Detecting Hierarchy Problems

**Redundancy (same instruction at multiple levels):**
Look for semantic matches, not just string matches. These are all the same instruction:
- Global: "Always write TypeScript, never JavaScript"
- Project: "Use TypeScript for all code"
- Subdir: "Code should be in TypeScript"

Resolution: Keep the most specific version at the lowest applicable level. Remove
from all higher levels unless the higher level needs a different default.

**Drift (same intent, different specifics):**
- Global: "Use 2-space indentation"
- Project: "Use tabs for indentation"

This might be intentional (project override) or accidental (someone edited one
and forgot the other). Flag for user review with context about which was modified
more recently.

**Orphaned instructions:**
Instructions at the global level that no current project uses. Common after
abandoning a project or switching tech stacks. Example: global CLAUDE.md has
Swift-specific instructions but the user no longer does iOS development.

**Missing levels:**
Large projects (>50 files) with no CLAUDE.md at all. The agent is flying blind
on project context, which means it asks more questions and makes more wrong
assumptions, costing tokens in a different way.

## Token Budget Guidelines

These are guidelines, not hard limits. A well-structured 300-line CLAUDE.md
is better than a cramped 100-line one that's missing critical context.

| Level | Recommended ceiling | Rationale |
|-------|-------------------|-----------|
| Global | ~200 lines (~800 tokens) | Loaded on EVERY conversation across ALL projects |
| Project root | ~100 lines (~400 tokens) | Loaded on every conversation in the project |
| Subdirectory | ~50 lines (~200 tokens) | Loaded alongside project root — combined budget matters |
| Combined stack | ~350 lines (~1400 tokens) | Total context loaded before the user says anything |

### Token Estimation

Quick estimate: **lines x 4 = approximate tokens** for English prose in markdown.
This is rough but sufficient for comparison and triage.

For more precision:
- Code blocks and tables: lines x 5 (more tokens per line)
- Sparse markdown (lots of headings, short bullets): lines x 3
- Dense prose paragraphs: lines x 5-6

### The 150-Instruction Ceiling

Frontier models (Claude 4.5/4.6, GPT-5.x) reliably follow approximately 150-200
individual instructions. Beyond this, compliance degrades uniformly — the model
doesn't selectively ignore new instructions, it starts dropping all of them with
equal probability.

Count instructions by counting discrete behavioral directives:
- "Use TypeScript" = 1 instruction
- "When writing tests, use vitest and prefer integration tests over unit tests" = 2 instructions
- A 5-item bulleted list of coding conventions = 5 instructions

If the combined instruction stack exceeds ~150 directives, something needs to
be extracted to a skill or removed entirely.

## Analysis Checklist

### 1. Token Bloat Detection

**Verbose explanations that could be compressed:**
```
Before (3 lines, ~12 tokens):
  When you encounter a situation where you need to create a new file,
  make sure that you check whether a similar file already exists in the
  project before creating a new one.

After (1 line, ~8 tokens):
  Before creating files, check if a similar file already exists.
```

**Instructions that restate default behavior:**
Many agents already do these things by default. Including them wastes tokens
and can even cause overtriggering (the model focuses too much on the stated
behavior at the expense of judgment):
- "Read files before editing them" (Claude Code already does this)
- "Use git for version control" (default behavior)
- "Write clean, readable code" (default behavior)
- "Handle errors appropriately" (default behavior)
- "Follow best practices" (too vague to be actionable)

**Excessive examples:**
Examples are valuable for ambiguous instructions, but instruction files often
include examples for self-evident rules. If the instruction is clear without
an example, the example is bloat.

**Comments and meta-instructions:**
Lines like `# This section covers our coding standards` add zero value. The
heading itself conveys this.

**Whitespace inflation:**
Excessive blank lines between sections. One blank line between sections is
sufficient. Three blank lines is three tokens wasted.

### 2. Redundancy Detection

**Within a single file:**
Search for semantically equivalent instructions within the same file. Common
pattern: an instruction appears in a "General" section and again in a
domain-specific section.

**Across the hierarchy chain:**
For each project, load the full stack (global + project + subdir) and look
for instructions that appear at multiple levels. The lower-level version
wins; higher-level duplicates should be removed.

**Across files at the same level:**
If there are multiple CLAUDE.md files at the same hierarchy level (e.g.,
`/project/CLAUDE.md` and `/project/.claude/CLAUDE.md`), they may contain
overlapping instructions. Recommend consolidation.

**With loaded skills or plugins:**
Check if any instruction file content duplicates what a skill already provides.
If a skill covers "how to write tests" and the CLAUDE.md also has a testing
section, the CLAUDE.md section is redundant.

### 3. Staleness Detection

**Obsolete model references:**
- Claude 3.x, Claude 3.5, Sonnet 3, Opus 3 → stale
- Claude 4.0, Opus 4.0, Opus 4.1 → stale
- GPT-4, GPT-4 Turbo, GPT-4o → stale
- Gemini 1.5, Gemini 2.0, Gemini 2.5 Pro → check currency
- Any model version that predates the current generation

**Deprecated tools and APIs:**
- References to tools that have been replaced or removed
- API endpoints that no longer exist
- Framework versions that are end-of-life

**Workflow references:**
- Instructions for workflows the user no longer follows
- References to team members who've left
- Deployment instructions for infrastructure that's changed

**Date-stamped content:**
- "As of March 2025" — check if still accurate
- Temporary instructions that were never removed ("for the next sprint")
- "TODO" or "FIXME" comments that have been sitting

### 4. Extractability Assessment

Content should be extracted from instruction files into skills when:

| Signal | Why extract |
|--------|------------|
| Only relevant to specific tasks | Loaded every time but only used 10% of the time |
| >20 lines of detailed workflow | Too long for an always-loaded file |
| Contains templates or reference tables | Better served by progressive disclosure |
| Is a complete standalone procedure | Can be triggered by description matching |
| Has tool-specific instructions | Only relevant when that tool is being used |

Content should stay in instruction files when:
- It applies to every conversation (code style, response format)
- It's <5 lines (not worth the overhead of a separate skill)
- It's a behavioral constraint (don't do X, always do Y)
- It needs to survive context compaction in long conversations

### 5. Cross-Platform Calibration

When analyzing instruction files, check for platform-specific antipatterns:

**Claude 4.5/4.6 antipatterns:**
- ALL-CAPS emphasis (CRITICAL, MUST, ALWAYS, NEVER) — causes overtriggering
- Anti-laziness language ("be thorough", "explore all possibilities") — unnecessary and harmful on Opus
- Personality padding ("you are a world-class expert") — wastes tokens
- "Think step by step" outside of extended thinking context — can cause issues on Opus 4.5

**GPT-5.x antipatterns (in AGENTS.md files):**
- Personality padding is even more harmful — simpler prompts outperform
- Micro-step instructions for tasks within native capability — trust the model
- Missing scope boundaries — GPT-5.x will overengineer without explicit constraints
- Missing done-conditions — will keep going without explicit stop signals

**Cross-platform instruction files:**
Some projects have both CLAUDE.md and AGENTS.md. Check for:
- Contradictions between the two (different conventions stated)
- One being a copy of the other without platform-appropriate calibration
- Opportunities to share a common base with platform-specific overlays

### 6. Drift Detection

**Semantic drift:** Same intent expressed differently across files. Use these
heuristics:
- Both mention the same tool, library, or concept
- Both address the same category (testing, formatting, imports, naming)
- The instructions would conflict if both were followed literally

**Version drift:** Same instruction updated in one file but not another. Check
modification dates — if file A was modified recently and file B hasn't been
touched in months, B may be stale.

**Convention drift:** The coding style section says one thing but the examples
in other sections demonstrate something different. Internal inconsistency
within a single file.

## Producing Recommendations

For each issue found, produce a recommendation in this format:

```
File: /path/to/CLAUDE.md
Lines: 45-62
Category: redundancy | bloat | staleness | extractability | drift | calibration
Priority: P0 (do now) | P1 (do soon) | P2 (nice to have)
Action: remove | shorten | extract | update | merge | move
Detail: Specific description of what to change and why
Token savings: ~X tokens
```

### Priority Guidelines

**P0 — Do now:**
- Instructions that are factually wrong or contradict current behavior
- Redundancies in global files (highest cost — loaded on every conversation)
- Stale model references that cause the agent to use wrong calibration
- Token bloat >100 tokens in global files

**P1 — Do soon:**
- Redundancies in project files
- Extractable content >20 lines
- Calibration issues (ALL-CAPS emphasis, anti-laziness language)
- Cross-platform drift

**P2 — Nice to have:**
- Minor wording improvements
- Whitespace cleanup
- Reordering sections for clarity
- Adding missing but non-critical instructions
