# Stage 1: Structural Review

Evaluate the skill's anatomy, organization, progressive disclosure, description
quality, and writing patterns. This stage answers: "Is this skill well-organized
and does it load efficiently?"

## Checklist

Work through each section. For each item, note **pass**, **concern**, or **fail**
with specific evidence from the skill. Add findings to the Scratchpad tagged
`[STRUCTURAL]` with a severity (Critical / Important / Minor).

### 1.1 Directory Structure

A well-structured skill follows this anatomy:

```
skill-name/
├── SKILL.md (required — instructions and routing)
├── FEEDBACK.md (recommended — feedback loop entries)
└── Bundled resources (optional)
    ├── scripts/    — Executable code for deterministic/repetitive tasks
    ├── references/ — Docs loaded into context as needed
    └── assets/     — Files used in output (templates, icons, fonts)
```

**Check:**
- Does SKILL.md exist with valid YAML frontmatter (name + description)?
- Are scripts, references, and assets separated into appropriate directories?
- Are there files at the root that should be in subdirectories?
- Are there unnecessary files (temp outputs, test artifacts, editor configs)?
- If the skill has evals, are they in an `evals/` directory?

### 1.2 Progressive Disclosure

Skills use a three-level loading system. Violations cause context waste.

| Level | What | Budget |
|---|---|---|
| Metadata | name + description in frontmatter | ~100 words, always in context |
| SKILL.md body | Core instructions and routing table | Under 500 lines ideal |
| Bundled resources | Reference files, scripts, assets | Loaded on demand, unlimited |

**Check:**
- Is SKILL.md under 500 lines? If over, is the excess justified or should
  content move to reference files?
- Does the routing table clearly indicate when to load each reference file?
  (Vague pointers like "see references/" without guidance = concern)
- Are reference files loaded only when needed, or does the skill instruct
  reading everything upfront?
- For reference files over 300 lines: do they have a table of contents?
- Could any SKILL.md content be moved to reference files to reduce the
  always-loaded footprint?
- Is there content in reference files that should be in SKILL.md (frequently
  needed instructions buried in optional references)?

### 1.3 Description Quality

The description field is the primary triggering mechanism. It determines whether
Claude invokes the skill at all.

**Check:**
- Does the description explain both WHAT the skill does AND WHEN to use it?
- Does it include specific trigger phrases and contexts?
- Is it "pushy" enough? Skills tend to undertrigger rather than overtrigger.
  A good description includes phrases like "Use this skill whenever..." and
  lists concrete trigger scenarios.
- Does it mention competing skills and when THIS skill should win?
- Is it too long? Descriptions should be comprehensive but not a full paragraph
  of prose — aim for 3-6 sentences covering purpose + trigger conditions.
- Would a user asking a reasonable question in this skill's domain actually
  trigger it? (Imagine 3-4 realistic user messages and assess)

### 1.4 SKILL.md Writing Quality

These patterns produce more effective skills. Evaluate against each.

**Imperative form:** Instructions should use imperative form ("Read the file",
"Check for errors") not passive or suggestive ("The file should be read",
"It might be helpful to check for errors").

**Explain the why:** Instructions that explain their rationale produce better
generalization than bare commands. "Use sentence case for headings — this
matches standard editorial conventions and reduces inconsistency" is better
than "Use sentence case for headings." If the skill uses heavy-handed MUST/ALWAYS
language without explaining why, that's a concern.

**Examples over abstractions:** Concrete examples of input/output, format
specifications with templates, and before/after pairs are more effective than
abstract descriptions. Check whether the skill provides examples for its most
important behaviors.

**Avoid over-specification:** Skills that try to control every decision produce
rigid, brittle behavior. Good skills define the what and why, then trust the
model's judgment for the how. If you see extensive step-by-step micro-management
for tasks the model can handle with general guidance, flag it.

**Theory of mind:** Does the skill address the model at the right level? It
should not explain things the model already knows (basic Python syntax, how to
read files) but should explain domain-specific conventions, non-obvious
requirements, and the reasoning behind unusual choices.

### 1.5 Feedback Loop

**Check:**
- Does the skill have a FEEDBACK.md file?
- Does SKILL.md reference it with instructions to read it before every use?
- Is the feedback loop process defined (detect → search → scope → draft → write)?
- If FEEDBACK.md exists, are there entries? Are they actionable and tagged?
- If entries exceed ~75, has compaction been done?

### 1.6 Repeated Work Detection

Read through the skill's workflow and imagine it being invoked 10 times on
different inputs.

**Check:**
- Are there tasks the model would need to do every single invocation that could
  be bundled as a script? (e.g., a consistent file parsing step, a validation
  routine, a formatting pass)
- Are there reference lookups or data that every invocation needs that could be
  pre-computed or cached?
- Does the skill reinvent standard patterns that could use established libraries?

## Output

Update the Scratchpad with all structural findings. Each finding should include:
- Tag: `[STRUCTURAL]`
- Severity: Critical / Important / Minor
- What: specific issue
- Where: file and line/section
- Why it matters
- Suggested fix

Then proceed to Stage 2.
