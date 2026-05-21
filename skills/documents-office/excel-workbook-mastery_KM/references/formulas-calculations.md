# Formulas & Calculation Best Practices

This file covers formula readability, helper-column discipline, structured references, dynamic arrays, LET and LAMBDA usage, lookup strategy, defensive formula design, volatile functions, circular references, and cross-sheet link hygiene.

See also: `workbook-architecture.md` for overall model flow, `finance-accounting.md` for modeling conventions, and `anti-patterns.md` for failure modes caused by fragile formulas.

### Formula readability first

Prefer helper columns or rows over heroic nested formulas. A workbook that needs genius to maintain is a bad workbook.

**Example — nested formula vs helper columns:**

Nested (hard to audit):
`=IF(AND(VLOOKUP(A2,Rates!A:B,2,0)>0.1,B2>1000),B2*VLOOKUP(A2,Rates!A:B,2,0)*1.05,B2*0.03)`

Same logic with helper columns (easy to audit):

| A: Customer | B: Revenue | C: Rate | D: Qualifies? | E: Final |
|---|---|---|---|---|
| Acme Corp | 1500 | `=XLOOKUP(A2,Rates!A:A,Rates!B:B)` | `=AND(C2>0.1, B2>1000)` | `=IF(D2, B2*C2*1.05, B2*0.03)` |

Each step is independently verifiable. The intermediate columns act as documentation.

Good formula design:

- one clear step per line of logic,
- reusable intermediate calculations,
- short formulas copied consistently across ranges,
- visible assumptions,
- comments or notes for non-obvious logic.

### Use structured references and named anchors to self-document

In Tables, structured references often read better than raw cell addresses. Use them when they improve clarity. Use named ranges for major assumptions or switches. Reserve named ranges for values referenced in multiple places — naming every cell creates clutter rather than clarity.

### Dynamic arrays: use them, but control the spill

Modern Excel functions like `FILTER`, `SORT`, `UNIQUE`, `SEQUENCE`, `TAKE`, `DROP`, `CHOOSECOLS`, `LET`, and `LAMBDA` are powerful. Use them when they simplify the workbook materially.

But manage them carefully:

- leave room for spill ranges,
- label the output clearly,
- do not let a spill silently overwrite a carefully designed report area,
- and avoid dynamic-array cleverness in sheets meant for low-skill maintenance if a normal Table or PivotTable would be clearer.

### LET and LAMBDA

Use `LET` when it makes a repeated expression readable and faster to audit. Use `LAMBDA` only for logic that is genuinely reused and can be named and documented. If the custom logic becomes more opaque than the original formula, do not use it.

### Lookup decision tree

Default choices:

- Use `XLOOKUP` for most single-key lookups in modern Excel.
- Use `INDEX` with `XMATCH` or `MATCH` when you need positional control, two-way lookup behavior, or backward compatibility logic.
- Use `VLOOKUP` only for simple legacy models where left-to-right lookup is acceptable and stability is not a concern.
- Use `SUMIFS`, `COUNTIFS`, `AVERAGEIFS`, or `SUMPRODUCT` when aggregation is the real need — a conditional aggregate is often cleaner than a lookup.

**Lookup comparison — same task, three approaches:**

Task: Find the price for product "Widget-X" from a product table.

| Approach | Formula | Notes |
|---|---|---|
| XLOOKUP (preferred) | `=XLOOKUP("Widget-X", Products[Name], Products[Price], "Not found")` | Clean, handles not-found gracefully, no column index to break |
| INDEX/MATCH (compatible) | `=INDEX(Products[Price], MATCH("Widget-X", Products[Name], 0))` | Works in Excel 2016+, positional flexibility |
| VLOOKUP (legacy) | `=VLOOKUP("Widget-X", A2:D100, 3, FALSE)` | Fragile — inserting a column changes the result silently |

### Version compatibility

Several functions used throughout this skill require Excel 365 or Excel 2021+. When building workbooks for users who may be on older versions, choose compatible alternatives.

| Function | Minimum version | Legacy alternative |
|---|---|---|
| `XLOOKUP` | 365 / 2021 | `INDEX` + `MATCH` |
| `FILTER`, `SORT`, `UNIQUE` | 365 / 2021 | PivotTables, helper columns with formulas, or Advanced Filter |
| `LET` | 365 / 2021 | Nested formula (less readable) or helper columns |
| `LAMBDA` | 365 / 2021 | Named formulas or VBA UDFs |
| `SEQUENCE` | 365 / 2021 | ROW()-based sequences |
| `TAKE`, `DROP`, `CHOOSECOLS` | 365 (late 2022+) | INDEX-based extraction |
| `XMATCH` | 365 / 2021 | `MATCH` (fewer match modes) |
| Dynamic array spill | 365 / 2021 | Ctrl+Shift+Enter array formulas (CSE) |

When the target audience's Excel version is unknown, default to `INDEX`/`MATCH` and avoid dynamic array functions. Note the version assumption in the README sheet.

### Defensive formula patterns

Use formula defenses deliberately:

- guard division by zero,
- distinguish true blanks from zeros,
- surface missing mappings,
- keep text beginning with `=` from being mistaken for formulas when literal text is intended,
- and separate user-facing friendliness from underlying error visibility.

Let errors surface in calculation areas so problems are visible. Reserve friendly error messages for user-facing output cells only.

### Volatile functions and performance

Avoid volatile functions such as `INDIRECT`, `OFFSET`, `NOW`, `TODAY`, `RAND`, and `RANDBETWEEN` unless the workbook truly needs their behavior. They recalculate more often and can make large models fragile or slow.

When performance matters, prefer:

- Tables instead of volatile dynamic ranges,
- `INDEX`-based references instead of `OFFSET`,
- explicit scenario selectors instead of indirect text-based addressing,
- and simpler calculation chains.

### Circular references

Avoid circular references by default. Use them only when the model truly needs iterative logic, such as certain interest or tax loops, and then document the loop clearly. A deliberate circular model should contain a note explaining the dependency and expected iteration behavior.

### Cross-sheet links

Keep link flow directional when possible: inputs to calculations to outputs. Random back-and-forth links make models harder to audit. If a calculation on one sheet depends on another, make the dependency obvious and avoid chains that bounce around the workbook unnecessarily.
