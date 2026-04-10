# Accessibility, Publication, and Review Readiness

This file covers final-stage discipline: accessibility defaults, publication readiness, reviewer-proofing, final QA, task-specific quick decision rules, and the overall standard the workbook should meet before it leaves your hands.

See also: `visual-design.md` for accessibility-aware formatting, `charts-and-visualization.md` for figure export, and the relevant domain file for subject-matter-specific checks.

### Accessibility defaults

Confirm these before handoff (see `visual-design.md` for the detailed accessibility rules):

- descriptive sheet names,
- strong contrast,
- no color-only meaning,
- simple navigation order,
- clear headers,
- limited merged cells,
- alt text or adjacent explanation for critical graphics,
- and color choices that survive grayscale printing.

### Publication readiness

Before calling a figure or table publication-ready, check:

- labels readable at final size,
- units present,
- axes titled where needed,
- fonts consistent,
- line weights not too thin,
- colors distinguishable to color-blind readers,
- no unnecessary borders or chartjunk,
- raster output high enough resolution if vector is unavailable,
- and the figure matches journal or sponsor expectations.

### Review readiness

Before handoff, act like the next person is skeptical and busy.

Ask:

- Are source assumptions easy to find?
- Can a reviewer reproduce key outputs from visible inputs?
- Do totals tie?
- Do charts match the data table beneath them?
- Is there any hidden logic that would surprise an auditor?
- Are scenario labels, dates, and units consistent everywhere?

## Final QA Checklist

Run this checklist mentally or explicitly before you finish.

### Structure

- Sheet order makes sense.
- Inputs, calculations, checks, and outputs are separated.
- Sheet names are descriptive.
- README or usage notes exist for non-trivial workbooks.

### Inputs and logic

- Editable cells are obvious.
- Validation exists where bad inputs are likely.
- Hardcoded assumptions are visible, not buried.
- Formulas are consistent across repeating ranges.

### Errors and checks

- No visible Excel errors remain.
- Control totals tie.
- Balance or reconciliation checks pass.
- Missing mappings or blanks are flagged.

### Formatting

- Number formats fit the data.
- Units and periods are shown.
- Borders and fills are restrained.
- Print layout works.

### Charts

- Chart type matches the question.
- Titles say the point.
- Axes, labels, and units are clear.
- No decorative clutter remains.

### Domain-specific review

- Financial statements tie and key assumptions are isolated.
- Scientific tables show units, replicates, and methods clearly.
- Statistical outputs are interpreted, not dumped raw.
- Reconciliations show differences and explanations.

### Handoff

- Refresh or as-of date is shown when relevant.
- Known limitations are documented.
- The workbook could survive a new owner.

## Bottom line

Build Excel work that is easy to read, easy to audit, hard to break, honest in what it shows, and respectful of the next person who has to use it. Default to transparency, consistency, and restraint. When forced to choose, choose the design that makes mistakes easier to spot.
