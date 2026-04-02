---
name: excel-mastery
description: >
  Use this skill whenever Excel is the working surface or final deliverable.
  Load only the reference files that match the task. Triggers on: building or
  editing spreadsheets, financial models, lab data analysis in Excel, pivot
  tables, chart formatting, dashboard design, workbook audits, Excel formula
  architecture, publication-quality Excel figures, grant budgets in Excel,
  reconciliation workbooks, or any task where spreadsheet design quality
  matters. This skill guides design decisions and best practices — pair it
  with the xlsx scripting skill for programmatic file generation when needed.
  Supersedes the public xlsx skill for design guidance; the public xlsx skill
  handles low-level file scripting mechanics.
version: 3.0
tags:
  - excel
  - spreadsheet-design
  - data-visualization
  - financial-modeling
  - statistics
  - research
---

# Excel Mastery Skill

Use this skill whenever you are building, editing, auditing, analyzing, or presenting work inside Excel. Treat Excel as both a calculation engine and a communication surface: the workbook must be understandable to someone other than you, survive review, and make mistakes easier to detect rather than easier to hide.

This skill is deliberately modular. Start with the file or files that match the task, then expand only if the work crosses domains. A financial model does not need the full scientific-analysis guide; a publication figure does not need the full accounting section. Progressive loading keeps your working memory focused. Avoid loading more than 3 reference files simultaneously — beyond that, instruction density degrades.

Your default posture: preserve the workbook's existing house style unless redesign is requested, separate inputs from calculations and outputs, keep logic transparent, label units and time periods, and leave visible checks behind. If the workbook will be reviewed, printed, exported, or inherited, design for that now rather than as cleanup at the end.

## Feedback loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior sessions.

1. **Detect** — After completing a task, note anything that didn't land: a guideline missed the mark, a reference file lacked needed depth, a routing choice was wrong, or a pattern emerged that isn't covered.
2. **Search** — Check `FEEDBACK.md` for existing entries on the same issue.
3. **Scope** — One actionable observation per entry.
4. **Draft-and-ask** — Propose the entry: "I noticed [issue]. Want me to log this?"
5. **Write-on-approval** — Append with date and category tag.
6. **Compact-at-75** — Merge duplicates, promote recurring patterns into reference files, archive resolved. Reset to ~30 entries.

## Progressive loading table

| Task | Load |
|---|---|
| Building a new workbook from scratch | `workbook-architecture.md` + `visual-design.md` |
| Making charts or figures | `charts-and-visualization.md` + `visual-design.md` |
| Statistical analysis or pivot tables | `data-science-statistics.md` |
| Lab data, calibration, PK analysis, release kinetics | `engineering-scientific.md` |
| Financial models, budgets, forecasts | `finance-accounting.md` |
| Writing or auditing formulas | `formulas-calculations.md` |
| Reviewing or improving an existing workbook | `anti-patterns.md` + the relevant domain file |
| Publication-quality figure export | `charts-and-visualization.md` + `visual-design.md` + `review-readiness.md` |
| Final QA, accessibility, handoff, reviewer-proofing | `review-readiness.md` + the relevant domain file |
| Restructuring a messy workbook before any domain work | `workbook-architecture.md` + `anti-patterns.md` |
| Cleaning a CSV/TSV and structuring it for Excel | `workbook-architecture.md` + `data-science-statistics.md` |
| Building a dashboard or KPI report | `workbook-architecture.md` + `visual-design.md` + `charts-and-visualization.md` |
| Importing or migrating from Google Sheets or another tool | `workbook-architecture.md` + the relevant domain file |
| VBA, macros, or automation requests | Out of scope — flag that VBA/macro work needs a different workflow. Suggest using the xlsx skill's scripting capabilities or a dedicated VBA resource. |
| Large-scale data profiling before structuring | Hand off to exploratory-data-analysis first, then return here for Excel formatting. |
| Generating .xlsx files programmatically | `production-patterns.md` + the relevant design reference file |
| Auditing an existing workbook (automated) | Run `scripts/audit_workbook.py` on the file first, then load `anti-patterns.md` + relevant domain file |

All paths are in `references/`. Loading 3+ files simultaneously should be a deliberate choice, not a default.

## Universal rules for all Excel work

These are strong defaults, not mandates. When the workbook context, user preference, or established house style clearly calls for a different approach, use your judgment. The goal is a workbook that serves its purpose well — not one that mechanically follows a checklist.

1. **Preserve local conventions first.** If the workbook already has a house style, match it unless the user asked for a redesign.
2. **Separate what users edit from what the workbook calculates.** Inputs, calculations, checks, and outputs should be easy to distinguish.
3. **Keep logic dynamic and inspectable.** Put assumptions in cells, not inside formulas, unless the number is a true constant.
4. **Make units, dates, and definitions visible where the eye needs them.** A table or chart without scope is a liability.
5. **Favor clarity over cleverness.** Short formulas, helper columns, direct labels, and readable layouts beat compact tricks.
6. **Assume spreadsheets fail quietly.** Add checks, tie-outs, flags, and reasonableness tests.
7. **Store meaning in data, not formatting.** Color, bold, or position may support meaning, but the underlying category or status should exist as an explicit field.
8. **Design for the next owner.** Document refresh date, purpose, limitations, and anything fragile.
9. **Use the lightest formatting that still communicates.** Signal hierarchy and exceptions; decoration without information is noise.
10. **Leave no silent surprises.** Broken links, hidden logic, stale dates, and masked errors are handoff failures.

## Handling conflicts and limits

When auditing or reviewing a workbook, lead with what needs fixing rather than what's working. The user needs an honest assessment — identify issues by severity (Critical / Important / Minor) and give concrete repair steps.

When the user's request conflicts with these guidelines, explain the tradeoff briefly and offer both options: "I can merge those cells as requested, but it'll break sorting and filtering on that range. Want me to use center-across-selection instead, or go ahead with the merge?"

When a task clearly exceeds what manual Excel work can handle well — large-scale data transformation, complex automation, anything requiring VBA or Power Query beyond basic use — flag it and suggest the appropriate tool rather than forcing a brittle Excel-only solution.

## Before you start

Run this checklist on every Excel task before making changes:

- Identify the workbook type: data-entry template, analysis model, dashboard, reconciliation, scientific worksheet, financial model, or publication figure.
- Inspect the current structure: sheet order, hidden sheets, named ranges, Tables, PivotTables, filters, print setup, and obvious control checks.
- Decide whether you are preserving an existing pattern or building a new one.
- Determine which cells are true inputs, which are imported data, which are formulas, and which are presentation outputs.
- Confirm units, reporting periods, source systems, and whether an as-of date or refresh date needs to be shown.
- Check whether the task is high-consequence: audit, regulatory, publication, board, investor, grant, or executive use.
- Load only the reference files that match the actual task.
- If the workbook already looks fragile, start with `references/anti-patterns.md`.
- If the workbook will be handed off or exported, finish with `references/review-readiness.md`.
- If the task changes midstream, expand scope deliberately instead of improvising.

## Quick decision rules

### Existing workbook
Honor the workbook's house style first. Improve clarity and correctness without casually redesigning established patterns.

### New general-purpose workbook
Default to: README, Inputs, Raw Data, Calc, Checks, Output. Use Tables for row-based data and keep formatting restrained.

### Financial model
Use a disciplined assumptions-driven structure, finance color conventions, explicit checks, consistent formulas across periods, and clean statement layouts.

### Scientific analysis
Keep raw data intact, make units and replicates explicit, separate calibration and fit assumptions from results, and round only at presentation.

### Dashboard or management report
Aim for one-screen comprehension, a small number of KPIs, sparing color, direct chart labels, and a clear message per visual.

### Publication-quality figure
Design at final size, strip chartjunk, use scatter/line/bar appropriately, ensure font and axis readability, and export at publication-safe quality.

### Data-entry template
Prioritize validation, protection, controlled vocabularies, obvious input zones, instructions, and clean downstream structure.

## Load escalation rules

- If you start in a domain file and realize the workbook itself is badly organized, add `references/workbook-architecture.md`.
- If a formula task turns into a readability or performance problem, add `references/formulas-calculations.md`.
- If a model is becoming presentation-facing, add `references/visual-design.md`.
- If charts are going to a manuscript, board deck, or formal PDF, add `references/review-readiness.md`.
- If an existing workbook feels unsafe or confusing, add `references/anti-patterns.md` even if the domain seems obvious.

## When to hand off to another skill

- **Programmatic .xlsx generation:** If the task is primarily about scripting a spreadsheet file (building it from data, automating repetitive generation), use the xlsx skill for production mechanics. This skill guides design decisions; xlsx handles the code.
- **Complex statistical analysis:** If the analysis exceeds Excel's built-in tools (mixed models, survival analysis, advanced regression diagnostics), hand off to statistical-analysis or python-visualization.
- **Publication figures beyond Excel's capabilities:** If the figure needs custom styling, multi-panel layouts, or molecular visualization, hand off to python-visualization.
- **Large-scale data exploration:** If the dataset needs profiling, automated outlier detection, or correlation matrices before being structured in Excel, start with exploratory-data-analysis.
- **When Excel isn't the answer:** If the data volume exceeds Excel's practical limits (~500K+ rows with formulas), the analysis needs reproducible scripting, or the workflow requires version control, recommend Python/R, a database, or Power BI instead. Say so directly rather than forcing a fragile Excel solution.

## File map

- `references/workbook-architecture.md` — workbook structure, naming, workflow, validation, protection, and error-handling architecture
- `references/visual-design.md` — typography, color, alignment, number formats, conditional formatting, print layout, accessibility-aware presentation
- `references/charts-and-visualization.md` — chart selection, chart formatting, Tufte/IBCS application, export and publication-quality visuals
- `references/data-science-statistics.md` — cleaning, descriptive stats, PivotTables, regression, hypothesis testing, common statistical errors
- `references/engineering-scientific.md` — lab data structure, units, calibration, dose-response, PK, nanoparticle characterization, uncertainty, GxP awareness, grant budgets
- `references/finance-accounting.md` — modeling structure, statements, sensitivities, reconciliations, audit trails, finance conventions
- `references/formulas-calculations.md` — formula readability, dynamic arrays, lookups, named ranges, volatility, circular references, version compatibility
- `references/anti-patterns.md` — spreadsheet failure modes with severity ratings, triage order, repair steps, and rapid assessment protocol
- `references/review-readiness.md` — accessibility, publication readiness, and final QA checklist for handoff
- `references/production-patterns.md` — openpyxl implementation patterns that apply the skill's design guidelines programmatically
- `scripts/audit_workbook.py` — automated workbook audit: scans sheet structure, formula complexity, errors, validation coverage, and naming quality
