# Writing Effective Skill Instructions

A skill body is a **routing-and-execution layer**, not documentation. The
description decides whether the skill triggers. The body decides which branch
to take, what reference file to load, and what output to produce. Everything
else belongs in `references/` or `scripts/`.

## Core Principle

Add only context Claude does not already have. Every extra token competes
with the live task in the context window. If a paragraph only restates intent
without changing behavior, cut it.

## What Claude Follows Reliably

There is no single magical format. Match the instruction form to the task's
fragility:

- **Plain imperative** for concrete actions: "Create the plugin directory."
- **Numbered sequences** when order matters: "1. Validate manifest. 2. Create
  components. 3. Package."
- **Decision branches** when the task has distinct modes: "If creating a new
  plugin, start at Phase 1. If customizing an existing plugin, start at
  Phase C1."
- **Output templates** when format drift hurts usefulness: "Return these
  sections: Decision, Files, Body, Open Questions."
- **Examples** when tone, structure, or judgment are hard to describe abstractly.

The winning instruction pattern is:

> "Do X when Y is true, because Z matters."

That gives Claude a rule, a trigger, and a reason.

### What Causes Drift

- Vague action language: "Improve the plugin as needed" — Claude improvises.
- Missing branch logic: "Create or customize the plugin" without explaining
  how to choose — Claude picks arbitrarily.
- Too many equal options: "You may use A, B, C, D, or E" — Claude burns
  tokens comparing or mixes them. Give a **default and an escape hatch**.
- Motivational filler: "Be thorough. Think deeply. Don't skip steps." —
  concrete done-conditions outperform motivation. Claude 4.5/4.6 responds
  more strongly to system prompts than earlier models, so heavy emphasis
  (CRITICAL / MUST / ALWAYS) can cause fixation instead of compliance.

## Progressive Disclosure Execution

SKILL.md should act like an **index**, not a textbook. The handoff text to
reference files is critical.

**Weak pattern:**

```
See `references/` for more details.
```

Claude has no idea which file to read or when. It either ignores the folder
or reads too much too early.

**Strong pattern:**

```
Before adding or editing a component schema, read `references/component-schemas.md`.
Before changing package metadata or release artifacts, read `references/packaging.md`.
Do not read both unless the request spans both concerns.
```

This gives Claude a branch condition, a file, and a stopping rule.

### What Goes Where

| Put it in… | What belongs there | What does NOT belong there |
|---|---|---|
| Description | Trigger boundary, when to use, when not to use | Detailed workflow, examples, long caveats |
| SKILL.md body | Core workflow, selection logic, reference index, output contract | Long API docs, giant examples, vendor catalogs |
| `references/` | Deep domain material, variant-specific guidance, schemas | Routing logic Claude needs every invocation |
| `scripts/` | Deterministic repeatable work (validation, packaging) | Human judgment or decision heuristics |

### Reference File Organization

Organize by **decision boundary**, not by file type.

Good: `components.md`, `packaging.md`, `triggers.md`
Bad: `examples1.md`, `examples2.md`, `notes.md`, `misc.md`

Claude can choose among reference files only if the boundaries are
semantically obvious. Keep references one level deep — nested references
risk partial reads.

When you have 5+ reference files, add a routing table in SKILL.md:

```
| File | Read when… |
|------|-----------|
| `references/components.md` | Creating or editing component schemas |
| `references/packaging.md` | Packaging, manifests, or versioning |
| `references/triggers.md` | Writing or debugging skill descriptions |
```

## Writing Skill Descriptions

The description is the routing surface. It becomes more important as the
skill count grows — descriptions compete for a character budget, and excluded
skills stop being discoverable.

### Good Description Anatomy

Include: what it does, when to use it (with natural user language), and when
NOT to use it.

**Too broad:**
```yaml
description: Helps create Claude plugins and skills.
```

**Too narrow:**
```yaml
description: Creates Cowork plugins with component-schema.json and package
  metadata for versioned releases.
```

**Better:**
```yaml
description: >
  Create, customize, and package Cowork and Claude Code plugins. Use when
  the task involves creating plugins, adding skills or MCP servers,
  packaging .plugin files, debugging plugin triggering, or editing
  plugin.json manifests. Do not use for general prompt writing unrelated
  to plugins, or for application code that merely mentions Claude.
```

### Description Debugging

If a skill doesn't trigger:
- Add the keywords users actually say
- Check "What skills are available?" in session
- Check `/context` for excluded skills (budget exceeded)
- Try direct invocation (`/plugin:skill`) to isolate load vs. routing

If a skill triggers too often:
- Make the description more specific
- Add explicit "do not use when…" boundaries
- Check for overlap with other installed skills

## Body Length Guidelines

Official ceiling: ~500 lines. Practical sweet spots:

| Skill type | Target lines |
|---|---|
| Simple workflow | 60–120 |
| Complex workflow with 2–4 branches | 100–200 |
| Anything larger | Turn SKILL.md into a router, push detail out |

The test: **does a new paragraph change behavior, or just restate intent?**
If it only restates intent, cut it.

## Common Anti-Patterns

### Documentation voice instead of operational voice

Skills that explain concepts, teach background, and narrate principles but
never tell Claude what to do next. The fix: reserve the body for actions,
branches, defaults, and outputs. Move exposition into references only when
Claude truly needs domain knowledge it cannot infer.

### Silent skills

Skills that "should" match but never fire. Causes: weak description, missing
user-language keywords, competition from similar skills, or
`disable-model-invocation: true` set unintentionally.

### Hijacker skills

Broad descriptions like "helps with project setup" that hijack unrelated
tasks. Fix: include "when not to use it" boundaries.

### Drift in long conversations

Context compaction can lose skill details. For anything catastrophic if
skipped (publishing, deleting, sending), move enforcement into hooks,
scripts, or manual invocation gates — not prose alone.

## Six Instruction Rewrites

### 1. Vague action → explicit branch

Bad: `Validate the plugin config before continuing.`

Better:
```
Before generating or editing plugin files, validate the manifest.
Read `references/component-schemas.md` for required fields.
If required fields are missing, stop and list exactly which fields are missing.
If only optional fields are missing, continue with documented defaults.
```

### 2. Weak reference handoff → explicit routing

Bad: `See the references folder for more details.`

Better:
```
Read exactly one reference file before acting:
- `references/component-schemas.md` for component definitions
- `references/packaging.md` for folder structure and versioning
Do not read multiple files unless the task clearly spans them.
```

### 3. Over-broad scope → explicit limits

Bad: `Improve the skill where needed.`

Better:
```
Implement only the behavior the user requested.
Do not rename unrelated files, refactor adjacent sections, or expand scope
unless the request explicitly includes cleanup or restructuring.
```

### 4. Too many options → default plus escape hatch

Bad: `You may use JSON, YAML, or TOML for metadata. Choose the best one.`

Better:
```
Default to the existing metadata format in the target project.
If no existing convention, use YAML frontmatter in SKILL.md and JSON for
plugin manifests. Only introduce a second format when the platform requires it.
```

### 5. Ambiguous output → explicit template

Bad: `Return a polished response.`

Better:
```
Return exactly these sections:
1. Decision — what you are creating or changing
2. Files — files to create or edit
3. Body — the proposed content
4. Open questions — only if required information is missing
```

### 6. Motivational filler → concrete done-conditions

Bad: `Be thorough. Think deeply. Don't skip steps.`

Better:
```
Stop after:
1. identifying the correct branch,
2. reading any required reference file,
3. producing the requested artifact,
4. listing unresolved inputs only if they block correctness.
```
