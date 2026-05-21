# Extraction Protocol

Detailed procedure for Pass 1: pulling discrete actionable items from each report.

## Processing Order

Always process reports in descending quality score order. The highest-quality report sets the baseline — its items become the standard against which later reports' items are compared. This prevents low-quality content from establishing the bar.

## What Counts as an Item

An "item" is a discrete, extractable unit of actionable information. Each should stand alone — someone reading just this item should understand what to do without needing the surrounding paragraphs.

### Item Types

| Type | Definition | Example |
|---|---|---|
| **rule** | A concrete directive with specific conditions and values | "Tables should have 8-12px cell padding, with header cells using 12px and data cells using 8px" |
| **specification** | A precise value, format, configuration, or schema | A JSON schema for a config file, a CSS custom property set, exact API parameters |
| **template** | A reusable pattern, boilerplate, or starter structure | A prompt template with placeholders, a document skeleton, a code pattern |
| **decision-tree** | A branching logic for choosing between options | "If data has <7 series → bar chart. If 7-12 → grouped bar. If >12 → heatmap" |
| **comparison** | A structured evaluation of alternatives with tradeoffs | "XlsxWriter: better chart API, can't read files. openpyxl: reads and writes, weaker charts" |
| **failure-mode** | A known problem with diagnosis and fix | "3D charts reduce comprehension by 30% vs 2D — use 2D unless showing actual 3D spatial data" |
| **example** | A before/after, case study, or concrete illustration | A code snippet showing the wrong way then the right way, with explanation of what changed |
| **metric** | A benchmark, threshold, or measurable standard | "Charts with >7 data series become unreadable per Cleveland & McGill 1984" |
| **tool-rec** | A specific tool recommendation with use case and constraints | "Use Plotly for interactive charts that need hover tooltips; falls back gracefully to static PNG" |

### Extraction Decision Tree

For each candidate passage in a report:

```
Is this a concrete rule with specific values or conditions?
  → YES: Extract as rule or specification
  → NO: Continue

Is this a decision framework with branching logic?
  → YES: Extract as decision-tree
  → NO: Continue

Is this a comparison of alternatives with named tradeoffs?
  → YES: Extract as comparison
  → NO: Continue

Is this a known failure with diagnosis and fix?
  → YES: Extract as failure-mode
  → NO: Continue

Is this a before/after or concrete case study?
  → YES: Extract as example
  → NO: Continue

Is this a measurable benchmark or threshold?
  → YES: Extract as metric
  → NO: Continue

Is this a general principle with no concrete implementation guidance?
  → YES: Flag it. Can it be enriched with specifics from another report?
    → If yes: extract as rule with [NEEDS-ENRICHMENT] tag
    → If no: check slop filter. Probably cut.
  → NO: Continue

Does it fail the slop filter?
  → YES: Do not extract. Log to Cut Items with reason.
  → NO: Something unusual. Re-read. Either it's a novel item type or it's noise you haven't categorized yet.
```

## Tagging

Every extracted item gets three tags:

### Type
One of the nine types above. If an item spans two types (e.g., a rule that includes a comparison), pick the primary type and note the secondary in the content.

### Confidence

| Level | Criteria |
|---|---|
| **high** | Sourced (citation, URL, named expert), specific (concrete values), and consistent with other reports or established practice |
| **medium** | Reasonable and specific but unsourced, OR sourced but somewhat general, OR sourced and specific but from a single source with no corroboration |
| **low** | Vague, unsourced, hedged, or contradicted by another report. Extracting because it might be enriched in Pass 2 |

### Source
Format: `R[n] § [section name or paragraph description]`

Example: `R2 § "Typography for data tables" ¶3` (Report 2, Typography for data tables section, third paragraph)

Approximate location is fine — the goal is traceability, not page-level precision.

## Extraction Depth by Quality Score

The report's quality score (from Pass 0) determines how deeply to extract:

| Quality Score | Extraction Depth |
|---|---|
| 4.0 - 5.0 | **Exhaustive.** Extract every item that passes the slop filter. Include medium-confidence items. Look for buried gems in examples, footnotes, and asides. |
| 3.0 - 3.9 | **Standard.** Extract high and medium confidence items. Skim examples and footnotes for unusually specific content. |
| 2.0 - 2.9 | **Selective.** Extract only high-confidence items with concrete values or citations. Skip anything that requires enrichment — it probably won't get it from this report. |
| 1.0 - 1.9 | **Minimal or excluded.** If the user chose to include this report despite the low score, extract only items that are both high-confidence AND not covered by any higher-quality report. |

## Cross-Reference Extraction

When the same claim, source, or recommendation appears in multiple reports:

1. **Same claim, same source cited:** Note the agreement. This increases confidence. Extract from the version that's most specific. Tag: `[corroborated by R[n]]`
2. **Same claim, different sources cited:** Strong signal. Extract the most specific version, note all sources. Confidence: high.
3. **Contradictory claims, same topic:** Extract both. Create a CONFLICT entry in the working document. Do NOT resolve here — that's Pass 2's job.
4. **Same source cited, different claims extracted:** The reports interpreted the source differently. Extract both, flag for Pass 2 verification.

## Common Extraction Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Extracting section headers as items | The header sounds like a rule ("Responsive Design Patterns") | Headers are navigation, not content. Extract what's UNDER them |
| Extracting introductory context | "In the modern data landscape, visualization is crucial..." | This is motivation, not instruction. Skip to actual recommendations |
| Splitting one item into many | A paragraph with a rule + rationale + example gets split into 3 items | Keep together. The unit of extraction is the complete actionable item with its context |
| Merging distinct items | Two different recommendations in the same paragraph get combined | If they're independently actionable, they're separate items |
| Over-extracting from high-quality reports | "This report is great, everything is gold" | Even 5.0 reports are 40-60% scaffolding. Apply the slop filter uniformly |
| Under-extracting from low-quality reports | "This report is weak, skip it" | Low-quality reports may contain 2-3 gems. Extract those, discard the rest |

## Per-Report Procedure

For each report (in quality order):

1. Read the full report (or process in chunks if it exceeds context — see `references/token-budget-management.md`)
2. Apply the extraction decision tree to each substantive passage
3. For each extracted item:
   a. Check against slop filter (`references/slop-filter.md`)
   b. If it passes: assign ID, tag (type, confidence, source), write to working document Active Items
   c. If it fails: write to Cut Items with reason
4. After finishing the report: update the Report Registry in the working document (items extracted, status → processed)
   - If the report is long but yielded very few solid survivors (rule of thumb: <10 from an ~8k+ word report), note it explicitly and recommend either excluding that report or rerunning extraction with a narrower question.
5. Update Pipeline Stats

## Reporting to User After Pass 1

Present a summary after all reports are processed:

```
## Pass 1 Complete: Extraction Summary

| Report | Quality | Items Extracted | Items Cut | Notes |
|---|---|---|---|---|
| [name] | [score] | [count] | [count] | [any notable findings] |

**Totals:** [extracted] items extracted, [cut] items cut
**Confidence distribution:** [high]H / [medium]M / [low]L
**Slop filter rejections:** [count] ([top 2-3 rejection reasons])
**Cross-references found:** [count] corroborations, [count] conflicts

[Notable findings: any surprises, unusually rich sections, or gaps worth mentioning]

Ready for Pass 2 (Dedup & Resolve)?
```

Wait for user acknowledgment before proceeding. The user may want to review the working document, adjust extraction from specific reports, or add guidance for Pass 2.
