# Analysis Framework

Reference file for Phases 3-6 of the Skill Library Curator. Load when
entering Phase 3 (Relationship Map) and keep available through Phase 6.

## Relationship Types

### Designed Pairs

Two skills built to divide a single domain along a clear seam. The classic
pattern: one skill owns *what* (design decisions, aesthetics, content
strategy) and the other owns *how* (implementation technique, tool
selection, rendering pipeline).

**Detection signals:**
- One skill's SKILL.md explicitly references the other as a companion
- The user's system prompt routing table pairs them for specific task types
- They share a domain keyword but have clearly different output types
- One is "load alongside X when..." rather than "use instead of X"

**Rule:** Never merge designed pairs. If the boundary between them is
blurry, recommend sharpening their descriptions — not collapsing them.

**Examples from a typical library:**
- design-maestro (aesthetics) + ui-motion-wiki (animation engineering)
- design-maestro (what it looks like) + game-dev (rendering/physics)
- word-docx-production (Word file mechanics) + document-design-mastery (document design
  intelligence)
- skill-creator (deep audit or iteration for one skill) + skill-library-curator (audit the whole
  library)

### Override Chains

A user skill that explicitly supersedes a public or example skill. The user
version exists *because* the default wasn't good enough.

**Detection signals:**
- User skill name is a variant of a public skill name (e.g., docx-enhanced
  overrides public docx, pptx-master overrides public pptx)
- User's system prompt contains "supersedes" or "replaces" declarations
- Both skills handle the same file type or workflow

**Rule:** The user override is always the keeper. Flag the override
relationship in the inventory but don't treat it as duplication.

### Command Bindings

Skills bound to slash commands (`/game`, `/design`, `/tts`, etc.) in the
user's system prompt. These have an external contract — changing or removing
them breaks the user's muscle memory.

**Detection signals:**
- Skill name appears in a command table in the user's system prompt
- SKILL.md references a specific invocation pattern

**Rule:** Command-bound skills cannot be silently merged or removed. If a
merge is warranted, the command must rebind to the merged skill, and the
system prompt impact section must document this.

### Dependency Clusters

Skills that reference each other's conventions, outputs, or existence.

**Detection signals:**
- Skill A's instructions say "use skill B for..." or "see skill B"
- Skill A produces output that skill B consumes
- Both skills reference a shared convention (e.g., FEEDBACK.md format,
  .skill packaging, scratchpad protocol)

**Rule:** Dependency clusters should be audited together. Removing one
member may break another. Document the dependency in the relationship map.

### Platform-Scoped Skills

Skills targeting different execution environments even if they share a
domain.

**Detection signals:**
- One skill assumes Claude.ai artifacts (React JSX, browser sandbox)
- Another assumes Claude Code (filesystem access, subagents, CLI tools)
- Another assumes Codex CLI or OpenClaw (AGENTS.md, different conventions)

**Rule:** Platform-scoped skills are distinct even if they do "the same
thing." A prompt-writing skill for Claude (claude-prompt-architect) and one for
GPT (gpt-prompt-architect) are not duplicates — they're calibrated for
different model families.

## Similarity Decision Matrix

For each candidate pair, evaluate:

| # | Dimension | Same? | Weight |
|---|-----------|-------|--------|
| 1 | Primary job-to-be-done | | 3 |
| 2 | Input types and sources | | 1 |
| 3 | Output artifact shape | | 2 |
| 4 | Core decision workflow | | 3 |
| 5 | Tools and scripts used | | 1 |
| 6 | Trigger phrase overlap | | 2 |
| 7 | Target platform/environment | | 2 |

Weighted score interpretation:
- **12-14**: Near-certain duplicate or version chain. Merge unless
  relationship map shows designed-pair or platform-scope difference.
- **8-11**: Significant overlap. Inspect manually — may be
  general/specialist, designed pair, or genuine merge candidate.
- **4-7**: Adjacent but distinct. Keep separate. Consider whether
  descriptions need sharpening to reduce trigger ambiguity.
- **0-3**: Unrelated. No action needed between these two.

## Staleness Heuristics

Flag a skill as potentially stale if it matches any of these:

**Model references:**
- Mentions Claude 3, 3.5, Opus 4.1, Sonnet 3.5, or older model names
  without also mentioning current models
- Mentions GPT-4, GPT-4 Turbo, or older OpenAI models as current
- Hardcodes model strings that may have rotated

**Tool references:**
- References tools or APIs that have been deprecated or significantly
  changed (check with web search if uncertain)
- References CDN URLs that may have changed or been blocked
- Contains workarounds for bugs that may have been fixed

**Convention drift:**
- No FEEDBACK.md when the user's current convention requires it
- Uses placeholder patterns the user has since banned
- References workflow conventions (file paths, naming, packaging) that
  have changed
- Description doesn't follow current routing-logic style

**Activity signals:**
- No evidence of recent use or iteration (no FEEDBACK.md entries, no
  references from other skills)
- The user's system prompt doesn't reference it anywhere

Staleness alone is not grounds for removal. A stale skill with a unique
job should be marked KEEP+REWRITE. A stale skill that duplicates a fresh
one is an archive candidate.

## Bloat Detection

Flag a skill for potential splitting if:

- SKILL.md exceeds 500 lines and has few or no reference files (the body
  is doing too much — content should flow into references)
- The description lists 4+ distinct trigger contexts that don't share a
  common workflow
- The skill contains branching logic for fundamentally different output
  types (e.g., "if the user wants a report... if the user wants a
  dashboard... if the user wants a slide deck")
- Reference files exceed 20 and many are domain-specific variants that
  suggest the skill is a Swiss army knife

A large skill is not inherently bloated. A skill with 15 reference files
organized by progressive disclosure is fine — that's the architecture
working as intended. Bloat is when SKILL.md itself tries to hold
everything.

## Trigger Collision Detection

Two skills have a trigger collision when a user query could reasonably
activate either one. This is distinct from functional overlap — skills
can have colliding triggers but do different things.

**How to detect:**
1. Extract all trigger phrases and contexts from each skill's description
2. For each skill pair, identify shared trigger words and phrases
3. Check whether the descriptions provide clear disambiguation

**Resolution approaches (prefer in order):**
1. Add "don't use when" boundaries to both descriptions
2. Add "supersedes X when Y" declarations
3. Rename one skill to create stronger conceptual separation
4. If the skills genuinely do the same thing, merge them

## Cross-Location Relationships

Skills that exist in multiple agent runtimes have a distribution relationship
that is distinct from functional relationships. Handle with care.

### Synced Copies

Skills managed by a sync system (e.g., skillsync manifest). Changes should
flow through the sync pipeline, not be made independently in each location.

**Detection signals:**
- Same directory name appears in multiple `~/.craft-agent/workspaces/*/skills/`
- Listed in `~/.craft-agent/shared/skill-sync/manifest.json`
- Content hashes are identical across locations

**Rule:** Synced copies are not duplicates. Don't recommend merging or removing
one copy — recommend syncing if they've drifted.

### Global Pool → Agent Symlinks

Skills in `~/.agents/skills/` are often symlinked into agent-specific
directories (`~/.claude-profiles/skills/`, etc.).

**Detection signals:**
- `is_symlink: true` in discovery output
- Canonical path resolves to `~/.agents/skills/`

**Rule:** Symlinked skills are a single file. Changes to the global pool copy
automatically propagate. Don't count these as separate skills in the audit.

### Independent Copies

Same skill name in different locations with no symlink or sync relationship.
May have diverged over time.

**Detection signals:**
- Same directory name, different content hashes
- No symlink relationship
- Not in skillsync manifest

**Rule:** Identify the newest/best version. Recommend consolidating to one
canonical copy and syncing or symlinking from there.

## Category Taxonomy

These categories are starting points. The actual taxonomy should emerge
from the library's contents, not be forced onto it.

| Category | Description |
|----------|-------------|
| **authoring** | Document creation, editing, formatting (Word, PDF, slides) |
| **research** | Literature search, evidence synthesis, deep research |
| **frontend** | UI/UX, web components, visual design, artifacts |
| **code-infra** | Code generation, review, debugging, architecture |
| **data** | Spreadsheets, EDA, statistical analysis, visualization |
| **science** | Domain-specific scientific workflows (brainstorming, critical thinking, databases) |
| **prompting** | Prompt engineering, skill creation, system prompt design |
| **media** | Image generation, TTS, algorithmic art, photography |
| **automation** | MCP servers, agent builders, workflow orchestration |
| **meta** | Skills about skills — this skill and skill-creator |

Skills can have one primary category and optional secondary tags.
Don't force everything into these buckets — if a skill genuinely straddles
two categories, note both and move on.
