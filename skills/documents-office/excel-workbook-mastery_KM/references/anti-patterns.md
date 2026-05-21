# Common Mistakes & Anti-Patterns

This file covers spreadsheet failure modes: how to recognize them, how bad they are, and what to do about them. Use it whenever reviewing, auditing, or inheriting a workbook that feels fragile, confusing, or untrustworthy.

See also: `workbook-architecture.md` for how to rebuild structure, `formulas-calculations.md` for safer logic patterns, and `review-readiness.md` for final auditing before handoff.

## Rapid assessment protocol

When inheriting a messy workbook, spend the first pass on triage rather than fixing. Work through this sequence:

1. **Sheet scan.** Count sheets, check for hidden sheets (right-click sheet tabs → Unhide), note naming quality. Sheets named `Sheet1`, `Copy of Final`, or `DO NOT DELETE` are warning signs.
2. **Formula scan.** Select a few key output cells and trace precedents (Ctrl+[). If the chain bounces across 4+ sheets or references external files, note the complexity.
3. **Error scan.** Use Ctrl+G → Special → Formulas → Errors to find all visible errors. Count them. Zero errors in a large workbook may mean errors are being masked.
4. **Structure scan.** Is there a clear flow from inputs → calculations → outputs? Or is everything mixed together on one sheet?
5. **Formatting scan.** Does formatting carry meaning consistently, or is it decorative noise?
6. **Date/version check.** When was this last updated? Is there any documentation of assumptions or sources?

After the scan, classify the workbook as: **Healthy** (minor cleanup), **Sick** (structural problems but salvageable), or **Terminal** (rebuild from scratch is faster than repair). Report findings by severity before touching anything.

## Anti-pattern catalog

### Critical — fix before trusting any output

#### Hardcoded values buried in formulas

**What it looks like:** `=B5*0.21+B5*1500*0.035` where 0.21 and 0.035 are tax rates and 1500 is a threshold — none of which appear in labeled cells.

**Why it's dangerous:** These values are invisible to reviewers, impossible to update safely, and guaranteed to drift from reality without anyone noticing.

**Repair:** Extract every magic number into a labeled cell in an Inputs or Assumptions section. Reference the cell instead.

Before: `=B5*0.21`
After: `=B5*TaxRate` (where `TaxRate` is a named range pointing to a clearly labeled cell showing `21%`)

#### Hidden critical logic

Rows, columns, or entire sheets that contain essential calculations are hidden from view. The workbook appears simpler than it is, and anyone editing the visible parts risks breaking the hidden parts.

**Repair:** Unhide everything. If the hidden content is genuinely intermediate, move it to a clearly labeled calculation sheet rather than hiding it on the output sheet.

#### Blanket IFERROR masking

**What it looks like:** `=IFERROR(VLOOKUP(A2,Data!A:F,4,0),"")` wrapped around every formula, returning blank strings for all failures.

**Why it's dangerous:** This hides broken lookups, missing data, type mismatches, and structural errors behind a wall of empty cells. The workbook looks clean while silently producing wrong answers.

**Repair:** Replace with specific error handling. Use `IFNA` when the only expected failure is "key not found." Let other errors surface.

Before: `=IFERROR(VLOOKUP(A2,Data!A:F,4,0),"")`
After: `=IFNA(XLOOKUP(A2,Data!A2:A1000,Data!D2:D1000,"[No match]"),"[No match]")`

The `[No match]` label makes missing data visible rather than invisible.

#### Circular references used accidentally

Unintentional circular references produce wrong results or zero values depending on Excel's iteration settings. They're especially dangerous because Excel may not show a warning after the first dismissal.

**Repair:** Check File → Options → Formulas → Enable Iterative Calculation. If it's on and nobody knows why, trace the loop and break it. If the circularity is deliberate (interest-on-interest loops, tax-on-EBIT models), document the loop, the convergence behavior, and the expected iteration count.

### Important — fix before sharing or relying on outputs

#### Merge cell abuse in data regions

Merged cells break sorting, filtering, copying, and programmatic access. A merged header row means no one can sort the table below it without first unmerging.

**Repair:** Use "Center Across Selection" (Format Cells → Alignment) for spanning headers. It looks identical but preserves cell independence.

Before: Cells A1:D1 merged with "Q3 Revenue Summary"
After: "Q3 Revenue Summary" in A1, Center Across Selection applied to A1:D1

#### Formatting used as data

Red cells mean "urgent," bold rows mean "approved," yellow means "needs review" — but none of this information exists in any actual data field. One wrong format paste and the meaning is gone.

**Repair:** Add an explicit Status column. Keep the color as a visual reinforcement via conditional formatting tied to the Status field, so the formatting is generated from data rather than replacing it.

#### Inconsistent formatting that signals nothing

Bold sometimes means "total," sometimes means "input," sometimes means "I wanted emphasis here." The formatting system has no grammar.

**Repair:** Define a simple formatting grammar and apply it consistently. Example: bold = totals/subtotals, blue font = editable inputs, light gray fill = disabled/locked areas. Document the convention on a README sheet or at the top of each major sheet.

#### Mixed data types in columns

A column contains numbers, text notes, dates, and `N/A` strings mixed together. Formulas operating on this column will silently skip non-numeric values or return errors.

**Repair:** Separate data from commentary. Put notes in an adjacent column. Standardize the data column to a single type. If missing values exist, use a consistent representation (blank cell, or a specific sentinel value documented in the README).

#### Fragile external links

The workbook references `C:\Users\jsmith\Desktop\Budget_Final_v3.xlsx` — a path that exists only on one person's machine. When the file moves, every linked formula breaks.

**Repair:** Decide whether the link is essential. If yes, move the source file to a shared location and update the reference. If the linked data is static, paste it as values into a RawData sheet and document the source. Break links that serve no current purpose (Data → Edit Links → Break Link).

#### Static outputs with no refresh context

A dashboard shows "Revenue: $4.2M" but there's no date stamp, no source reference, and no indication of when the data was last updated. The number could be from yesterday or last year.

**Repair:** Add an as-of date cell that updates when data is refreshed. If the refresh is manual, make the date a manual input with a validation rule or conditional formatting that flags staleness (e.g., turns red if more than 7 days old).

### Minor — fix when cleaning up, not urgent

#### Over-formatting

Heavy fills on every row, thick borders around every cell, multiple font sizes, decorative gradients, and cell comments used as decoration. The workbook looks busy but communicates less than a clean one would.

**Repair:** Strip back to the minimum formatting that communicates structure: section borders, header emphasis, input highlighting, and total lines. Everything else is noise.

#### Too many decimal places

Cells showing `0.0847263519` when the measurement precision is ±5%. The false precision implies confidence the data doesn't support.

**Repair:** Format to display the number of significant figures the data actually supports. Calculate with full precision internally; round only at the display layer.

#### Sheets with no documentation

A new user opens the workbook and has no idea what it does, what period it covers, what units are used, or which cells are safe to edit.

**Repair:** Add a README sheet or a documentation block at the top of the primary sheet. Include: purpose, owner, as-of date, key assumptions, source systems, known limitations, and editing instructions.

#### Pie charts and 3D effects

3D charts distort area perception. Exploded pie charts add visual complexity without adding information. Both make exact comparison harder.

**Repair:** Replace 3D charts with 2D equivalents. Replace pie charts with sorted horizontal bar charts when there are more than 3-4 categories or when values are close together. Keep pie charts only when there are 2-3 dominant slices and the audience only needs a rough part-to-whole impression.

#### Unlabeled axes and charts

A chart exists with no title, no axis labels, no units, and a legend that says "Series1." The reader has to reverse-engineer what they're looking at.

**Repair:** Add a descriptive title (the point, not just the subject: "Revenue growth slowed after Q2" instead of "Revenue"). Label axes with units. Use direct labels instead of legends when feasible.

## Triage order

When a workbook has multiple problems, fix them in this order:

1. **Structural errors** — hidden logic, circular references, broken links. These affect whether outputs are correct at all.
2. **Data integrity** — mixed types, formatting-as-data, masked errors. These affect whether inputs are trustworthy.
3. **Transparency** — hardcoded values, missing documentation, no checks. These affect whether the workbook is auditable.
4. **Presentation** — formatting inconsistency, chartjunk, over-decoration. These affect whether the workbook communicates clearly.

Resist the urge to fix formatting first — it's the most visible but least important category.
