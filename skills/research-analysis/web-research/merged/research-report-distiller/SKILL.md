---
name: research-report-distiller
description: >
  Distill multiple deep research reports into a single, high-quality, actionable reference
  document through a multi-pass agentic pipeline. Use whenever the user provides one or more
  research reports, deep research outputs, knowledge base documents, or long-form reference
  material and wants them combined, deduplicated, filtered, and refined into a polished
  final deliverable. Triggers on "distill these reports", "combine these into one document",
  "extract the good stuff from these", "clean up this research", "turn these reports into
  a skill", "merge these documents", "diamond cut this", "synthesize these", "what's
  actually useful in these reports", or any task involving synthesis of multiple research
  outputs into a single refined reference. Also triggers when the user provides multiple
  research reports without explicit instructions — ask if they want distillation. Works
  for any domain. Pairs naturally with the research-prompt-writer skill as its downstream
  consumer.
---

# Research Report Distiller

> Multi-pass pipeline that cuts raw research into polished, actionable reference documents. Takes N reports in, discards noise, resolves conflicts, produces one comprehensive output — either a standalone reference document or a full skill package.

**Quick start:** User drops reports → say `/distill` → follow prompts between passes.

## Core Metaphor

Diamond cutting. Raw research reports are uncut stones — gems buried in matrix rock (filler, repetition, AI slop, unsourced claims). Successive passes extract, shape, and polish the valuable material.

```
Raw reports → Triage → Extract → Deduplicate & Resolve → Architect → Polish → Final output
     ◇           ◇        ◇              ◇                   ◇          ◇         ◆
  (rough)    (graded)  (cleaved)      (faceted)            (set)    (polished)  (diamond)
```

Single-pass synthesis fails at scale. One pass over 30-50k tokens either skims (missing gems in paragraph 47) or bloats (including everything without judgment). The multi-pass pipeline solves both.

## Always-On Rules

1. **Never single-pass.** Even for a single short report: Extract → Architect → Polish minimum. Multiple reports require all five passes.
2. **Slop filter is always active.** Every extracted item must survive `references/slop-filter.md`. Apply during extraction AND again during dedup. When in doubt, flag for user review rather than including.
3. **Actionable or out.** Every item in the final output must be something the reader can DO. Principles need implementation guidance. Recommendations need specific values, settings, or steps. "Use good typography" is out. "Use 1.4-1.6 line-height for body text, 1.1-1.2 for headings, minimum 16px body font" is in.
4. **Working document is the source of truth (and the scratchpad).** Never hold pipeline state in memory alone. Build and maintain the working document per `references/working-document-protocol.md`. It evolves across passes.
5. **Quality-weighted extraction.** Reports are not equal. Score before extracting, weight accordingly. A 12k-word report full of concrete examples gets deeper extraction than a 4k-word report full of generalities.
6. **Show your work between passes.** After each pass, report to the user. Use this consistent mini-report format:

   ```
   ## Pass [N] complete: [name]
   - Items in: X → Items out: Y (Z% reduction)
   - Conflicts: N found, M resolved, K pending user input
   - Notable: [1–3 bullets]
   - Next: [what happens next + what you need from the user]
   ```
7. **Source preservation.** Track which report(s) each item came from through all passes. The final output doesn't need inline citations, but the working document must preserve provenance.
8. **Yield gate.** If a large report produces very few survivors (rule of thumb: <10 solid items from ~8k+ words), pause and ask the user whether to continue, re-extract with a different lens, or exclude that report.

## Feedback Loop

**Always read `FEEDBACK.md` when loading this skill.**

Cycle: detect issue → search FEEDBACK.md → scope to 1-3 lines → draft and ask user → write on approval → compact at 75 entries (merge duplicates, promote recurring patterns to reference files, archive resolved).

## Routing Table

Load relevant references based on current phase. Multiple files often apply.

| Load when... | Load these |
|---|---|
| **Starting any run** | `FEEDBACK.md` (always), `references/slop-filter.md` (always), `references/working-document-protocol.md` (always) |
| **Pass 0: Intake & Triage** | `references/quality-scoring.md` |
| **Pass 1: Extract** | `references/extraction-protocol.md` |
| **Pass 2: Dedup & Resolve** | `references/dedup-and-conflicts.md` |
| **Pass 3: Architect** | `references/architecture-patterns.md` |
| **Pass 4: Polish** | `references/polish-checklist.md` |
| **Output: skill package** | `references/skill-output-guide.md` |
| **Output: reference document** | `references/document-output-guide.md` |
| **Input exceeds ~60k tokens** | `references/token-budget-management.md` |
| **Adding to existing distillation** | `references/working-document-protocol.md` § Incremental Mode |

## Pipeline Overview

**Relative effort (so the user knows when to stay engaged):** Pass 1 is usually the longest, Pass 2 and Pass 3 are medium, and Pass 0 + Pass 4 are quick.

### Pass 0: Intake & Triage

**Load:** `references/quality-scoring.md`

Count and catalog reports. Score each on 5 dimensions (specificity, sourcing, actionability, depth, originality). Present triage to user: report names, quality scores, 2-3 sentence assessment each. Flag any report scoring below 2.0 — recommend exclusion. Use `ask_user_input` to confirm: output format (skill package vs reference doc), which reports to include/exclude, and processing order.

If total input exceeds ~60k tokens, load `references/token-budget-management.md` before proceeding.

### Pass 1: Extract

**Load:** `references/extraction-protocol.md`

Process each report in quality order. Pull every discrete actionable item that passes the slop filter. Tag each with Type, Confidence, and Source. Write items to the working document. Err on the side of over-extraction — Pass 2 handles dedup.

**Report to user:** items extracted per report, items discarded with reason breakdown, confidence distribution, notable findings.

### Pass 2: Deduplicate & Resolve

**Load:** `references/dedup-and-conflicts.md`

Group similar items. Merge exact and near-duplicates (keep most specific version, enrich with unique detail). Resolve conflicts using the evidence hierarchy: sourcing quality → consensus → recency → report quality score. Run slop filter a second time — items that looked acceptable in isolation may reveal themselves as generic when compared across reports. Use `ask_user_input` to resolve any unresolvable conflicts (or confirm keeping both with scoped notes).

**Report to user:** items before → after dedup (compression ratio), conflicts found and resolved, items cut in second slop pass.

### Pass 3: Architect

**Load:** `references/architecture-patterns.md`

Choose the right structural template for the domain and output format. Classify each surviving item (top-level principle, domain-specific rule, specification, example, decision aid). Build skeleton with section headers. Use `ask_user_input` to present skeleton for approval before filling in. Fill, watching for sections that are too thin (merge) or too thick (split). Add cross-references.

**Report to user:** proposed skeleton, items per section, items that didn't fit, estimated final length.

### Pass 4: Polish

**Load:** `references/polish-checklist.md`

Language tightening (verbose → concise imperatives). Consistency pass (terminology, formatting, tone). Actionability audit (could someone implement this right now?). Loss check (compare working document against final output — were high-confidence items lost?). Final slop check. Output-format-specific finishing per the relevant output guide.

**Present final output to user.**

## Commands

| Command | Action |
|---|---|
| `/distill` | Start a new distillation run. Load always-on references, begin Pass 0. |
| `/distill preview` | Run Pass 0 only (triage + recommendations) without starting full extraction. Useful when the user isn't sure the reports are worth distilling. |
| `/distill add` | Incremental mode. Add new reports to an existing working document. Runs Pass 0-1 on new reports, Pass 2 against existing items, Pass 4 to polish. Skips Pass 3 unless user requests re-architecture. |
| `/distill status` | Show current working document stats: items by status, confidence distribution, compression ratio, conflicts pending. |

## Output Formats

**Reference document** — Standalone markdown optimized for human reading and AI agent consumption. Sections: How to use this document → Core principles → Domain sections → Reference tables → Decision aids → Confidence notes → Sources. See `references/document-output-guide.md`.

**Skill package** — Full skill directory (SKILL.md + FEEDBACK.md + references/). SKILL.md under 500 lines as routing hub, detail in reference files. See `references/skill-output-guide.md`.

## Working Document

The working document is the pipeline's shared state between passes. Format, structure, and maintenance rules are in `references/working-document-protocol.md`.

**Location strategy:**
- **Small runs** (<5 reports, <40k tokens): Use a scratchpad artifact. This IS the scratchpad for the run — keep all state here.
- **Large runs** (5+ reports or >40k tokens): Use a file (e.g., `distill-working.md`) in a writable workspace. Better for script access and avoids artifact size limits.

## Edge Cases

**Single report:** Skip Pass 2 (dedup). Run Extract → Architect → Polish. Slop filter and actionability audit still apply.

**Reports on different topics:** Ask whether the user wants a combined multi-domain document or separate distillations. Combined is usually wrong unless there's a shared theme.

**Wildly different quality:** Pass 0 triage handles this. Reports scoring 1.0-1.5 should be flagged with a recommendation to exclude — their vague language tends to contaminate adjacent good content even after filtering.

**Enormous input (>100k tokens):** Process in batches per `references/token-budget-management.md`. Key technique: process reports sequentially, building the working document incrementally.

**User reinstates a filtered item:** Add it back with a note about why it was cut. The user's domain knowledge overrides the filter. Log the pattern to FEEDBACK.md.

## Anti-Patterns

| Anti-pattern | Why it's bad | Do this instead |
|---|---|---|
| Single-pass summary | Skims surface, misses buried gems, includes filler | Run the full pipeline |
| Uniform extraction | Treats all reports equally regardless of quality | Quality-score and weight |
| Topic-header organization | Sections named after report topics, not user tasks | Organize by what the reader needs to DO |
| Lossless merge | Including everything from every report | Aggressive filtering — 40-60% reduction is normal |
| Spec without context | "Use 12px padding" with no explanation of when/why | Every spec needs rationale and scope |
| Context without spec | "Use appropriate padding" with no values | Every principle needs concrete implementation |
| Conflict avoidance | Silently picking one side without noting disagreement | Surface conflicts, resolve with evidence, note dissent |
| Orphaned items | Good items cut because they don't fit the architecture | Fix the architecture, not the items |

## Integration

**Upstream:** This skill pairs naturally with `research-prompt-writer`. Reports produced via that skill's structure (focus areas, tiered sources, reporting requirements) are easier to distill because they have consistent structure and explicit sourcing.

**Downstream:** The output feeds into whatever the user is building — a skill, a knowledge base, a reference library, a decision framework. The output format choice (skill vs document) determines which downstream guide applies.
