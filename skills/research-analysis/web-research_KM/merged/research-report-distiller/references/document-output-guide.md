# Document Output Guide

How to transform distilled items into a standalone reference document. Read this during Pass 4 when the output format is "reference document."

## Document Structure

```markdown
# [Title]

## How to use this document
## Core principles
## [Domain section 1]
## [Domain section 2]
## ...
## Reference tables
## Decision aids
## Confidence notes
## Sources
```

Every section below is required unless explicitly marked optional.

## Section Details

### Title

Descriptive, specific, and scannable. Include the domain and scope.

Good: "Data Visualization Best Practices for Dashboard Design"
Bad: "Comprehensive Guide to Data Visualization" (too broad)
Bad: "Research Summary" (says nothing)

### How to Use This Document

2-3 paragraphs covering:
- **Who this is for.** What role, skill level, and context the reader should have.
- **How it's organized.** Brief description of the section structure and how to navigate.
- **What's NOT covered.** Explicit scope boundaries. Prevents the reader from searching for content that isn't here.
- **How to read it.** "Read Core Principles first. Then jump to the section matching your current task. Reference Tables are for quick lookup."

### Core Principles

5-10 high-level rules that shape everything downstream. Each principle is 3-5 sentences:
1. The rule itself (imperative voice)
2. Why it matters (1-2 sentences of rationale)
3. How it manifests in practice (concrete example or pointer to relevant sections)

**Selection criteria:** A principle belongs here if it applies across 3+ domain sections. If it only applies to one section, it's a section-level rule, not a core principle.

**Ordering:** Most foundational first. If Principle 2 depends on understanding Principle 1, Principle 1 comes first.

### Domain Sections

The bulk of the document. Each section covers one coherent topic area. Internal structure depends on the architecture template chosen in Pass 3 (see `references/architecture-patterns.md`).

**Typical internal structure:**
```markdown
## [Section Title]

[1-2 sentence context: when this section applies]

### [Sub-topic]
[Rules, specifications, and guidance for this sub-topic.
Each rule is 1-3 sentences. Specifications include concrete values.
Cross-reference other sections where relevant.]

### Pitfalls
[Common mistakes for this section's domain. Each pitfall names
the problem, explains why it happens, and gives a concrete fix.]
```

**Sizing:** Each domain section should be 30-80 lines. Under 30 → consider merging with an adjacent section. Over 80 → split into sub-sections or spin out a reference table.

### Reference Tables (optional but recommended)

Consolidated lookup tables for specifications, comparisons, or format codes that are referenced from multiple sections. Put them here instead of repeating in each section.

**Table format:**
```markdown
## Reference Tables

### [Table Title]

[1-2 sentence caption explaining what this table contains and how to read it]

| [Column 1] | [Column 2] | [Column 3] | [Column 4] |
|---|---|---|---|
| ... | ... | ... | ... |
```

Every table needs a caption. Columns need clear headers. Include units where applicable.

### Decision Aids (optional)

Decision trees, selection matrices, or flowcharts that help the reader make choices. These may also appear inline within domain sections — put them here if they span multiple sections.

### Confidence Notes

Required. Covers:
- **Items with thin sourcing:** Claims that made it into the document but rely on a single source or the distiller's judgment rather than cross-report consensus. "The recommendation to use X for Y is based on a single practitioner report [R3]. Consider verifying independently."
- **Unresolved conflicts:** Cases where reports disagreed and the distiller chose a position but the disagreement is worth noting. "R1 and R4 disagree on whether X affects Y. This document follows R1's position based on [reasoning], but R4's counterargument has merit."
- **Areas needing follow-up:** Topics where the research was thin and the document's coverage is acknowledged as incomplete. "Coverage of Z is limited to what R2 provided. A dedicated research run on Z would strengthen this section."
- **Dated items:** Recommendations tied to specific tool versions, market conditions, or technical states that may change. "The comparison of A vs B reflects their state as of [date]. Re-evaluate if either has had a major release."

### Sources

List the contributing reports with their quality scores and what they primarily contributed.

```markdown
## Sources

| Report | Quality Score | Primary Contribution |
|---|---|---|
| [Report 1 name/title] | [composite/5.0] | [1-sentence description of what it contributed] |
| [Report 2 name/title] | [composite/5.0] | [1-sentence description] |
```

If the user wants the original reports linked or attached, note their file locations. Don't reproduce report content here — this section is metadata only.

## Length Calibration

The final document should be **30-50% of total input length** for a good distillation. This is a rough guide, not a hard rule.

| Total input | Expected output | Notes |
|---|---|---|
| 10k tokens (~2 reports) | 3-5k tokens | Tight distillation. Every line matters. |
| 30k tokens (~3-5 reports) | 10-15k tokens | Standard distillation. Room for examples. |
| 60k tokens (~5-8 reports) | 20-30k tokens | Comprehensive. May need reference tables. |
| 100k+ tokens (8+ reports) | 30-50k tokens | Large reference. Consider skill format instead. |

If the output is under 25% of input, you may be over-filtering — check the loss audit. If over 60%, you may be under-filtering — check for surviving slop and redundancy.

## Quality Checks Before Delivery

- [ ] "How to use this document" section is present and accurate
- [ ] Core principles are 5-10, each with rationale and concrete guidance
- [ ] No empty sections
- [ ] All cross-references point to real sections (ctrl-F every "see" and "above" and "below")
- [ ] Reference tables have captions
- [ ] Confidence notes section is present and substantive (not just "some items may be uncertain")
- [ ] Sources section lists all contributing reports with scores
- [ ] Language is tightened (average <25 words/sentence)
- [ ] Terminology is consistent throughout
- [ ] The document could be handed to someone unfamiliar with the distillation process and they could use it immediately
