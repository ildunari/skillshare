---
name: skill-review
description: >
  Multi-stage audit pipeline for Claude skills. Performs structural analysis,
  technical review, prompt/instruction quality evaluation, cohesion analysis,
  and generates a severity-triaged report with copy-paste fixes. Use whenever
  the user wants to review, audit, evaluate, or quality-check a skill.
  Triggers on: "/skill-review", "review this skill", "audit my skill",
  "what's wrong with this skill", "evaluate this skill", "skill quality check",
  or any request to assess a skill's effectiveness or architecture. Also use
  when supplementary research or reference material is provided alongside a
  skill for incorporation. Supersedes generic code review and claude-prompt-architect
  when the target is a skill directory with SKILL.md. For standalone prompts
  (system prompts, CLAUDE.md, task prompts not part of a skill), use
  claude-prompt-architect instead.
---

# Skill Review Pipeline

A staged audit pipeline that systematically evaluates a Claude skill across four
dimensions: structural integrity, technical quality, instruction/prompt
effectiveness, and cohesion. Produces a severity-triaged report with specific,
actionable recommendations.

## Feedback Loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior reviews.

1. **Detect** — After completing a review, note anything that didn't land: a stage
   missed something, severity was miscalibrated, the report format didn't serve the
   user well, or a pattern emerged that the pipeline doesn't currently check.
2. **Search** — Check `FEEDBACK.md` for existing entries on the same issue.
3. **Scope** — One actionable observation per entry.
4. **Draft-and-ask** — Propose the entry: "I noticed [issue]. Want me to log this?"
5. **Write-on-approval** — Append with date and category tag.
6. **Compact-at-75** — Merge duplicates, promote patterns to reference files, archive
   resolved. Reset to ~30 entries.

## Pipeline Overview

The review runs in five stages. Each stage loads its reference file only when
active — never preload all references at once.

```
┌─────────────────────────────┐
│ STAGE 0: INTAKE             │  Read target skill. Identify scope.
│                             │  Start Scratchpad artifact.
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ STAGE 1: STRUCTURAL REVIEW  │  Skill anatomy, progressive disclosure,
│  → references/stage-1.md    │  writing quality, description triggering.
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ STAGE 2: TECHNICAL REVIEW   │  Scripts, code quality, architecture,
│  → references/stage-2.md    │  bundled resources, dependencies.
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ STAGE 3: PROMPT REVIEW      │  Instruction calibration, constraint
│  → references/stage-3.md    │  quality, failure mode hardening,
│                             │  agentic flow, determinism.
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ STAGE 4: COHESION ANALYSIS  │  Internal consistency, edge cases,
│  → references/stage-4.md    │  adversarial inputs, gap analysis,
│                             │  cross-stage conflict detection.
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ STAGE 5: REPORT             │  Synthesize Scratchpad into final
│  → references/report.md     │  severity-triaged report with
│                             │  specific edit recommendations.
└─────────────────────────────┘
```

## How to Run

### Stage 0: Intake

No reference file needed. This stage establishes context.

1. **Read the target skill.** Read `SKILL.md` and list the skill's directory
   structure. Do not read reference files or scripts yet — just note what exists.

2. **Read FEEDBACK.md** from this skill (skill-review) to apply lessons learned.

3. **Identify review scope.** Determine what the skill does, what type it is
   (workflow, document creation, code generation, research, design, etc.), and
   whether the user provided supplementary material (research reports, competitor
   skills, reference docs). Note these for later stages.

4. **Start the Scratchpad artifact.** Name it "Scratchpad — [skill-name]
   Audit" to avoid collision with other active Scratchpads. Initialize with:
   - Skill name and path
   - Skill type / domain
   - Supplementary materials provided (if any)
   - File inventory (what's in the skill directory)
   - Review scope notes

   Example Scratchpad finding entry:

   ```
   [STRUCTURAL] Important — Description doesn't mention competing skills.
   Where: SKILL.md frontmatter, description field.
   Impact: Users asking "review my skill's prompts" may trigger claude-prompt-architect
   instead of this skill.
   Fix: Add "supersedes claude-prompt-architect when the review target is a skill
   directory with SKILL.md" to the description.
   ```

5. **Brief the user.** Summarize what you'll review and confirm scope. If the
   skill is very large (5+ reference files, multiple scripts), ask which areas
   to prioritize. If the skill's total content exceeds what can be loaded
   across stages (roughly 2000+ lines of reference material), prioritize
   SKILL.md and the reference files most relevant to the user's stated
   concerns. Note unreviewed files in the report under "Review Scope" so the
   user knows what wasn't covered.

Then proceed to Stage 1.

### Stage 1: Structural Review

**Load `references/stage-1.md` now.** Follow its checklist. Update Scratchpad
with findings tagged `[STRUCTURAL]`.

### Stage 2: Technical Review

**Load `references/stage-2.md` now.** Read the skill's scripts and reference
files as needed during this stage (not before). Update Scratchpad with findings
tagged `[TECHNICAL]`.

If the skill has no scripts or bundled code, note this and move to Stage 3. A
skill with only SKILL.md and reference docs may still have technical findings
(e.g., reference files that should be scripts, missing automation opportunities).

If the user provided supplementary research or reference material, incorporate
relevant technical insights during this stage.

### Stage 3: Prompt Review

**Load `references/stage-3.md` now.** This is typically the highest-leverage
stage. Re-read the skill's SKILL.md and reference files with prompt-quality eyes.
Update Scratchpad with findings tagged `[PROMPTING]`.

### Stage 4: Cohesion Analysis

**Load `references/stage-4.md` now.** This stage looks across all previous
findings and the skill as a whole for systemic issues. Update Scratchpad with
findings tagged `[COHESION]`.

### Stage 5: Report Generation

**Load `references/report.md` now.** Synthesize the Scratchpad into a final
deliverable. Present the report to the user.

## Adapting the Pipeline

Not every skill needs the full five stages at full depth.

**Small skill (SKILL.md only, <100 lines):** Stages 1 + 3 are primary. Stage 2
is minimal (note absence of scripts/references). Stage 4 is light. Combine into
a single pass if the skill is simple enough.

**Script-heavy skill:** Stage 2 gets more weight. Read and evaluate scripts
during that stage.

**Prompt-heavy skill (lots of behavioral instructions, few scripts):** Stage 3
is the core of the review. Spend the most time here.

**User says "just the highlights":** Run all stages at reduced depth — check the
first 2-3 items per checklist section rather than exhaustively evaluating all
items. Focus on Critical and Important findings only, skip Minor. Report can be
shorter.

**User provides research reports alongside the skill:** Incorporate as
supplementary context. Cross-reference research findings against the skill's
current approach. Note gaps where research suggests improvements the skill
doesn't implement.

## What This Pipeline Does NOT Do

- It does not run the skill against test cases (use skill-creator for that)
- It does not optimize the description for triggering (use skill-creator's
  description optimization loop)
- It does not produce a full rewrite of the skill — it produces a diagnostic
  report with targeted replacement text for individual findings. Implementing
  all fixes as a cohesive rewrite is a separate step the user can request
  after reviewing the report.
- It does not evaluate skills for other AI platforms (the prompt review stage is
  calibrated for Claude 4.5/4.6 behavior)
