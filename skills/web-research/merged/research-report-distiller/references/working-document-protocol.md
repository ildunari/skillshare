# Working Document Protocol

The working document is the pipeline's shared state. It evolves across all passes and is the single source of truth between them. Never hold pipeline state in memory alone.

Treat this document as the run's scratchpad: if you'd normally keep a scratchpad artifact, this is it.

## Location Decision

| Condition | Location | Reason |
|---|---|---|
| <5 reports AND <40k tokens total | Scratchpad artifact | Visible to user, persistent across turns, editable |
| 5+ reports OR >40k tokens | File (e.g., `distill-working.md`) in a writable workspace | No artifact size limits, scriptable |
| User preference overrides | Whatever they ask for | User knows their workflow |

If using scratchpad: name it "Distillation Working Document" and update it after every pass. If using file: write after every pass and confirm to user.

## Document Format

```markdown
# Distillation Working Document

## Metadata
- **Title:** [Descriptive name for this distillation]
- **Started:** [ISO 8601]
- **Current pass:** [0-4]
- **Output format:** [skill | reference-doc | undecided]
- **Reports processed:** [count]
- **Total input tokens:** [estimate]

### Report Registry
| # | Report Name | Quality Score | Items Extracted | Status |
|---|---|---|---|---|
| R1 | [name] | [composite/5.0] | [count] | [processed | pending | excluded] |
| R2 | ... | ... | ... | ... |

### Pipeline Stats
| Metric | Value |
|---|---|
| Items extracted (Pass 1) | [count] |
| Items after dedup (Pass 2) | [count] |
| Compression ratio | [percentage] |
| Conflicts resolved | [count] |
| Conflicts pending user input | [count] |
| High confidence items | [count] |
| Medium confidence items | [count] |
| Low confidence items | [count] |

## Active Items

### ITEM-001 — [Brief descriptive title]
- **Type:** [rule | specification | template | decision-tree | comparison | failure-mode | example | metric | tool-rec]
- **Confidence:** [high | medium | low]
- **Source:** R[n] § [section or approximate location]
- **Status:** [extracted | enriched | merged-from-[IDs] | flagged]

[Content: the actual item. 1-5 lines. Concrete, specific, actionable.]

### ITEM-002 — [Title]
...

## Cut Items

Items removed during processing, preserved for loss auditing and user review.

### CUT-001 — [Title]
- **Original ID:** ITEM-[n]
- **Cut in:** Pass [n]
- **Reason:** [slop-hard | slop-soft | duplicate-of-ITEM-[n] | low-confidence | not-actionable | superseded-by-ITEM-[n] | user-decision]
- **Content:** [the item that was cut, for reference]

## Pending Conflicts

Unresolved contradictions between sources, awaiting user decision.

### CONFLICT-001
- **Topic:** [what the disagreement is about]
- **Position A:** ITEM-[n] (from R[n]) says: [claim]
- **Position B:** ITEM-[n] (from R[n]) says: [claim]
- **Evidence assessment:** [which position has better support and why]
- **Recommendation:** [which to keep, or keep both with scope notes]
- **Status:** [pending | resolved: kept [A|B|both]]

## Architecture Skeleton

Populated during Pass 3. Empty before then.

### [Section Title]
- Items assigned: ITEM-[n], ITEM-[n], ...
- Estimated length: [short | medium | long]

### [Section Title]
...
```

## Maintenance Rules

1. **Update after every pass.** The working document must reflect the current state after each pass completes.
2. **Never delete items silently.** Moving an item from Active to Cut requires a reason. The user should be able to trace any item's fate.
3. **Keep metadata current.** Pipeline stats should reflect the actual counts at all times.
4. **Item IDs are permanent.** Once assigned, an item's ID never changes. Merged items get the surviving item's ID with a note about what was merged in.
5. **Conflicts are first-class.** Don't bury disagreements in item notes. Give them their own section with structured fields so they're easy to present to the user.

## Incremental Mode

When adding reports to an existing distillation (`/distill add`):

1. Load the existing working document
2. Run Pass 0 on new reports only (triage, quality score)
3. Run Pass 1 on new reports only (extract to working document, continuing ITEM numbering)
4. Run Pass 2: dedup new items against ALL existing items (not just other new items)
5. Skip Pass 3 unless the user requests re-architecture or new items don't fit the existing skeleton
6. Run Pass 4 on the updated output

The working document's Report Registry grows. Pipeline Stats update to reflect the combined state.

## Size Management

If the working document grows past ~8k tokens (typical for 5+ reports with 100+ items), compress it:

- Active Items: keep only the title, type, confidence, source, and a 1-line summary (not the full content). Store full content in a separate overflow section or file.
- Cut Items: keep only the ID, reason, and 1-line summary. Drop the full content.
- Pipeline Stats: always keep in full.

For very large runs, the working document becomes a lightweight index that points to full content stored in companion files.
