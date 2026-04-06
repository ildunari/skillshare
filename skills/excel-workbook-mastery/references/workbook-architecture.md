# Workbook Architecture & Structure

This file covers workbook-level design: how to organize sheets, separate inputs from calculations and outputs, name things clearly, validate inputs, protect editable areas, document assumptions, and structure error handling so a workbook is understandable and auditable.

See also: `visual-design.md` for formatting choices, `formulas-calculations.md` for formula patterns, `anti-patterns.md` for repair triage, and `review-readiness.md` for final QA and handoff checks.

## Working posture

You are not just filling cells. You are building a tool for reasoning, communication, and review. Treat every workbook as something a stranger may inherit five minutes before a meeting, an audit, a submission deadline, or a board packet.

Use this skill for new workbooks, existing templates, dashboards, scientific analyses, financial models, operational trackers, and publication figures.

## Core operating rules

The universal rules in SKILL.md apply here. These additional rules are specific to workbook architecture:

1. **Leave zero visible errors.** Resolve `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NUM!`, `#N/A`, and broken chart ranges before handoff unless the user is explicitly debugging them.
2. **Keep assumptions outside formulas.** Put assumptions in cells and calculations in formulas. A true constant (12 months in a year) can stay inline if documented; a business assumption (tax rate, growth rate) belongs in a labeled cell.
3. **EuSpRIG-style caution.** Spreadsheets fail quietly. Build visible checks — control totals, balance tests, reasonableness flags — rather than assuming formulas are correct because they look right.

### Default workflow

Use this sequence unless the user’s workbook clearly requires a different one:

1. Inspect before editing: sheet order, hidden sheets, formulas, named ranges, Tables, PivotTables, print setup, existing styles, and any obvious control checks.
2. Decide the workbook pattern: data-entry sheet, analysis model, dashboard, reconciliation, financial model, lab worksheet, or publication figure.
3. Choose the structure: Tables for maintained datasets, formulas for transparent calculations, PivotTables for summarization, Power Query for repeatable ingestion and cleanup when available, named ranges only where they improve readability.
4. Build logic plainly: short formulas, helper rows or columns, visible assumptions, consistent references.
5. Format last, but design early: structure and readability come first; polish should reinforce logic.
6. QA before handoff: error scan, unit check, totals check, chart-label check, print check, and “could a new reader follow this in one pass?”

## Workbook Architecture & Structure

**Contents:** Organize multi-sheet workbooks · Naming conventions · Tables vs raw ranges vs named ranges · Data validation and input protection · Make editable cells unmistakable · Document the workbook inside the workbook · Error handling patterns · Structured error cascades · When to split into multiple workbooks

### Organize multi-sheet workbooks in layers

Your default architecture should be:

- `00_README` or `00_Cover`
- `01_Inputs`
- `02_RawData`
- `03_Calc`
- `04_Checks`
- `05_Output` or `05_Dashboard`
- `06_Archive` or supporting schedules if needed

For larger models, use this pattern instead:

- **Cover / README:** purpose, owner, refresh date, key assumptions, change log
- **Inputs:** user-editable assumptions and scenario selectors
- **Raw data:** imported or pasted source data, left as untouched as practical
- **Transform / staging:** cleanup, mapping, normalization, helper fields
- **Calculations:** the model proper
- **Checks:** tie-outs, control totals, balance tests, reasonableness tests
- **Outputs:** management tables, charts, print-ready views
- **Archive:** old scenarios, deprecated outputs, or frozen snapshots

Avoid `Sheet1`, `Final`, `Final_v2`, `New Sheet`, or tabs that hide meaning. Use names that answer what the sheet is for. If sheet order tells a story, the workbook is easier to audit.

### Naming conventions

Use short, plain, durable names.

- **Sheets:** prefix with order numbers if sequence matters: `01_Assumptions`, `02_SalesData`, `03_Model`, `04_Checks`, `05_Charts`
- **Tables:** noun-based names such as `tblSales`, `tblPatients`, `tblGL`, `tblPK`
- **Named ranges:** reserve them for true anchors like `TaxRate`, `DiscountRate`, `Scenario`, `ReportDate`
- **Cells / labels:** spell out units in adjacent labels or headers, such as `Revenue ($m)` or `Concentration (ng/mL)`

Do not create dozens of cryptic names. Named ranges should reduce ambiguity, not create it.

### When to use Excel Tables vs raw ranges vs named ranges

Use an **Excel Table** when:

- the data is row-based,
- users will add or remove records over time,
- filters, slicers, or structured references will help,
- downstream charts, PivotTables, or formulas should expand automatically.

Good fits: transactions, experiments, survey rows, GL detail, CRM exports, sample logs.

Use a **raw range** when:

- the content is a carefully designed report layout,
- the block is small and fixed,
- the sheet is presentation-oriented rather than data-oriented,
- the layout depends on custom spacing or bespoke formatting.

Good fits: print-ready statements, variance bridges, board-report tables, manuscript figures.

Use **named ranges** when:

- a single input or output is referenced many times,
- the name makes a formula self-documenting,
- the location may move but the meaning should stay fixed.

Do not use named ranges as a substitute for structure. If you are naming every other cell, the workbook is probably under-designed.

### Data validation rules and input protection

Apply data validation to every user-editable cell. Users will eventually type the wrong thing — validation catches it at the point of entry rather than downstream.

Default validation patterns:

- drop-down lists for controlled categories,
- whole number or decimal bounds for quantities,
- dates restricted to a valid period,
- custom validation for unique IDs or required prefixes,
- input messages for what belongs in the cell,
- error alerts that block invalid entries when the consequence matters.

Examples:

- Scenario selector: only `Base`, `Upside`, `Downside`
- Probability: between 0% and 100%
- Fiscal month: one of the valid month labels
- Experimental group: must match the controlled group list

Store list values on a dedicated support sheet instead of hardcoding long drop-downs directly into validation rules.

### Make editable cells unmistakable

Use more than one signal.

For user inputs, default to:

- unlocked cells,
- light fill or blue font if that convention is already in use,
- a nearby note if the input is non-obvious,
- protection enabled on formula areas when the workbook is meant for handoff.

Do not rely on color alone to indicate editability. Some users print in grayscale; some users are color-blind; some never read the legend. Pair color with location, borders, notes, or sheet zoning.

### Document the workbook inside the workbook

Every serious workbook should contain at least one of these:

- a `README` sheet,
- a visible note block at the top of the main output sheet,
- a change log section,
- or all three.

Include:

- workbook purpose,
- owner or preparer,
- version date,
- latest refresh date,
- source systems or source documents,
- key assumptions,
- limitations,
- known exclusions,
- and a quick “how to use this” note.

A minimal change log should have: date, editor, what changed, and why.

**Example README sheet layout:**

| | A | B |
|---|---|---|
| 1 | **Workbook:** | Q3 2025 Revenue Model |
| 2 | **Purpose:** | Forecast Q3 revenue by product line from assumptions |
| 3 | **Owner:** | Finance team / J. Smith |
| 4 | **Version:** | 2.3 |
| 5 | **Last updated:** | 2025-09-12 |
| 6 | **Data refreshed:** | 2025-09-10 (Salesforce export) |
| 7 | **Key assumptions:** | Growth rates in 01_Assumptions; see cells B4:B12 |
| 8 | **Known limitations:** | Does not include APAC pipeline; excludes deals <$10K |
| 9 | **How to use:** | Edit blue cells on 01_Assumptions only. All other sheets are calculated. |

| | A | B | C | D |
|---|---|---|---|---|
| 11 | **Change Log** | | | |
| 12 | **Date** | **Editor** | **Change** | **Reason** |
| 13 | 2025-09-12 | JS | Updated APAC exclusion note | Per CFO review |
| 14 | 2025-09-01 | JS | Added scenario selector | Board requested upside/downside |

### Error handling patterns

Do not scatter error handling randomly. Use a deliberate pattern.

Preferred order:

1. prevent invalid inputs,
2. create explicit checks,
3. use formulas that fail clearly when they should,
4. wrap only the user-facing output when a graceful message is better than an ugly error.

Use `IFNA` for missing lookups when the only expected failure is “not found.” Use `IFERROR` only when you are comfortable masking all error types for that specific output. Do not wrap entire models in blanket `IFERROR` just to hide problems.

Good pattern:

- calculation area shows real logic and real exceptions,
- check area counts missing keys, negatives where impossible, unbalanced totals, or broken assumptions,
- final output sheet shows friendly labels such as `Missing mapping` or `No data for selected period` where appropriate.

### Structured error cascades

For multi-step models, build checks in layers:

- **Input checks:** invalid dates, blanks in required fields, duplicates in keys
- **Transformation checks:** row counts before and after mapping, unmatched joins, unexpected categories
- **Calculation checks:** totals tie, balance sheet balances, percentages sum correctly, no divide-by-zero traps
- **Output checks:** chart ranges populated, print areas complete, labels match selected scenario or period

A `Checks` sheet should not be optional in a high-consequence workbook.

### When to split into multiple workbooks

Keep one workbook when:

- the dataset is moderate,
- the workflow is linear,
- the audience is one team,
- the model benefits from keeping assumptions, logic, and outputs together.

Split into multiple workbooks when:

- file size or calculation time becomes painful,
- confidential inputs should be separated from broad distribution outputs,
- different teams own different components,
- a stable published report should be isolated from a volatile source model,
- or external links would otherwise become a maintenance nightmare.

As a rule: split for governance, performance, or security. Do not split just because the workbook feels busy.
