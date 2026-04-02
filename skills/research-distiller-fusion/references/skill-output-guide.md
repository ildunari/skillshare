# Skill Output Guide

How to transform distilled items into a properly structured skill package. Read this during Pass 4 when the output format is "skill."

## Skill Package Structure

```
skill-name/
├── SKILL.md              # Routing hub. Under 500 lines.
├── FEEDBACK.md           # Standard header, empty entries.
└── references/
    ├── [domain-1].md     # Detailed reference per domain/task type
    ├── [domain-2].md     # Each under 300 lines
    ├── [tables].md       # Consolidated reference tables and specs
    └── [examples].md     # Before/after examples, templates, case studies (optional)
```

## SKILL.md Construction

The SKILL.md is a routing hub, not a comprehensive manual. It tells the LLM what to do and where to find details. The actual depth lives in reference files.

### Required Sections

**1. Frontmatter (~5 lines)**

```yaml
---
name: [kebab-case-name]
description: >
  [Aggressive trigger description. Over-trigger rather than under-trigger.
  Include 5-10 trigger phrases. Cover synonyms and indirect references.
  2-4 sentences.]
---
```

Write the description as if you're programming a classifier. Every way a user might phrase a request for this skill should be covered. Look at design-maestro, deep-research-prompting, and humanize-ai-content frontmatter for calibration.

**2. One-line summary + core metaphor (~5-10 lines)**

What this skill does in one sentence. If the distillation produced a good metaphor or mental model, include it.

**3. Always-on rules (~15-25 lines)**

The 5-10 most important principles from the distillation. These are the rules that apply regardless of which reference file is loaded. They're the "if you read nothing else, read this" items.

Selection criteria for always-on rules:
- Applies across 3+ task types or reference files
- Violation would produce obviously wrong output
- Not obvious to an LLM without explicit instruction (don't waste lines on "be helpful")
- Can be stated in 1-3 sentences

**4. Routing table (~15-25 lines)**

Maps task types to reference files. Format:

```markdown
| Task / Phase | Load These |
|---|---|
| [task description] | `references/[file].md` |
| [task description] | `references/[file1].md`, `references/[file2].md` |
```

Every reference file must appear in at least one routing table row. If a reference file doesn't have a clear trigger, either it should be merged into another file or the routing table needs a better task description.

**5. Feedback loop (~10-15 lines)**

Standard section. Copy the pattern from any existing skill.

**6. Brief inline reference (~20-40 lines, optional)**

For the most commonly needed specs — things that would be annoying to look up in a reference file every time. Game-dev has "Key Formulas," design-maestro has quick spacing/typography values. If the distillation produced a set of values that are referenced constantly, put them here.

**7. Commands (~5-10 lines, optional)**

If the skill has distinct modes triggered by slash commands.

### Line Budget

| Section | Target Lines |
|---|---|
| Frontmatter | 5 |
| Summary + metaphor | 5-10 |
| Always-on rules | 15-25 |
| Routing table | 15-25 |
| Feedback loop | 10-15 |
| Inline reference (optional) | 20-40 |
| Commands (optional) | 5-10 |
| **Total** | **75-130** (up to 200 for complex skills, hard cap 500) |

## Reference File Construction

### What goes in a reference file

Each reference file covers one coherent task type, domain area, or workflow phase. It contains the items from the distillation that apply to that area, organized for quick consumption by an LLM.

### How to organize items within a reference file

1. **Open with a 1-2 line purpose statement.** What task this file supports. When to load it.
2. **Rules and specifications first.** The concrete directives, organized by sub-topic.
3. **Decision trees and comparisons.** Choice points the LLM will face when applying the rules.
4. **Failure modes and pitfalls.** What goes wrong, organized near the rules they relate to.
5. **Examples last.** Before/after demonstrations of the rules in action.
6. **Quick-reference table at the bottom** (if applicable). Lookup values for rapid access.

### Sizing guidance

Under 300 lines per reference file. If a file exceeds 300:
- Split into two files by sub-domain
- Move examples to a shared `examples.md` and cross-reference
- Move lookup tables to a shared `tables.md` and cross-reference

Under 50 lines per file suggests the file should be merged with a related one.

### Naming convention

Use descriptive kebab-case names that match the routing table entries:
- `typography-rules.md` not `ref1.md`
- `chart-selection.md` not `charts.md`
- `error-handling.md` not `errors.md`

## FEEDBACK.md

Use the standard header:

```markdown
# [Skill Name] — Feedback Log

**MUST READ** before every use of this skill.

[1-2 sentences: what this file captures and why it matters.]

## Categories

- `[category-1]` — [brief description]
- `[category-2]` — [brief description]
[3-8 categories, adapted to the skill's domain]

## Entries

(none yet)
```

Categories should reflect the skill's main task types or failure modes. Don't use generic categories — tailor them.

## Quality Checks Before Delivery

- [ ] SKILL.md under 500 lines
- [ ] Every reference file under 300 lines
- [ ] Every reference file appears in the routing table
- [ ] Frontmatter description triggers on relevant user phrases (test mentally: "if a user said X, would this trigger?")
- [ ] Always-on rules are genuinely cross-cutting (not specific to one reference file)
- [ ] No orphaned cross-references (links to files or sections that don't exist)
- [ ] FEEDBACK.md has domain-specific categories
- [ ] The skill could be dropped into `/mnt/skills/user/` and used immediately
