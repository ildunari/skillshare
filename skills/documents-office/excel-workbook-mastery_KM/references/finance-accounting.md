# Accounting, Finance & Business Analysis

This file covers assumptions-driven modeling, statement layouts, finance formatting conventions, reconciliations, scenario and sensitivity analysis, audit trails, and the structural discipline used in professional financial modeling.

See also: `workbook-architecture.md` for workbook flow, `formulas-calculations.md` for formula discipline, `visual-design.md` for presentation standards, and `review-readiness.md` for final checks.

### Standard workbook structure for models

Use professional model separation:

- assumptions / drivers,
- historical data,
- operating schedules,
- core statements,
- debt or cap table schedules if relevant,
- valuation or scenario outputs,
- checks and sensitivities.

This aligns with FAST-style transparency and the broader financial modeling discipline used by Operis and F1F9: consistent structure, simple formulas, clear flow, and visible assumptions.

### Assumption-driven modeling

Keep all major assumptions separate from calculations: growth, margins, tax rates, discount rates, working-capital days, valuation multiples, price assumptions, headcount, utilization. Put these in a dedicated Assumptions sheet or a clearly labeled block at the top of the model.

**Example assumptions block layout:**

| | A | B (blue font) | C | D |
|---|---|---|---|---|
| 1 | **Operating Assumptions** | **Base** | **Upside** | **Downside** |
| 2 | Revenue growth | 8.0% | 12.0% | 3.0% |
| 3 | Gross margin | 62.0% | 64.0% | 58.0% |
| 4 | OpEx growth | 5.0% | 5.0% | 5.0% |
| 5 | Tax rate | 21.0% | 21.0% | 21.0% |
| 6 | | | | |
| 7 | **Working Capital** | | | |
| 8 | DSO (days) | 45 | 40 | 55 |
| 9 | DPO (days) | 35 | 35 | 30 |
| 10 | Inventory turns | 6.0x | 6.5x | 5.0x |

Blue font on the value cells signals "editable input" per finance convention. A scenario selector cell elsewhere (e.g., a dropdown choosing "Base," "Upside," or "Downside") can drive the model via `INDEX`/`MATCH` against this block.

The goal: the cell containing revenue growth is editable once and referenced everywhere needed. Changing an assumption should ripple through the entire model without hunting for hardcoded values.

### Statement layout defaults

#### Income statement

Use a top-down flow:

- revenue
- direct costs / cost of sales
- gross profit
- operating expenses by major group
- operating income / EBIT
- interest and other non-operating items
- pre-tax income
- tax
- net income

**Example layout (dates left-to-right, amounts in $000s):**

| | FY2023A | FY2024A | FY2025E | FY2026E |
|---|---|---|---|---|
| **Revenue** | 12,400 | 13,400 | 14,472 | 15,630 |
| Cost of Sales | (4,712) | (5,092) | (5,499) | (5,940) |
| **Gross Profit** | **7,688** | **8,308** | **8,973** | **9,690** |
| *Gross Margin* | *62.0%* | *62.0%* | *62.0%* | *62.0%* |
| | | | | |
| SG&A | (3,100) | (3,255) | (3,418) | (3,589) |
| R&D | (1,800) | (1,890) | (1,985) | (2,084) |
| **Operating Income** | **2,788** | **3,163** | **3,571** | **4,017** |
| Interest Expense | (120) | (110) | (100) | (90) |
| **Pre-Tax Income** | **2,668** | **3,053** | **3,471** | **3,927** |
| Tax @ 21% | (560) | (641) | (729) | (825) |
| **Net Income** | **2,108** | **2,412** | **2,742** | **3,103** |

Formatting conventions: historical years suffixed with "A" (actual), forecast with "E" (estimated). Negatives in parentheses. Subtotals in bold with a top border. Margins in italics below their parent line. Blank rows separate major sections.

#### Balance sheet

Group clearly:

- current assets
- non-current assets
- current liabilities
- non-current liabilities
- equity

Always include a balance check.

#### Cash flow statement

Make the method obvious and keep reconciliation clean. If indirect, start from net income and bridge to operating cash flow. Tie ending cash to the balance sheet.

### Finance formatting conventions

Use the standard finance color system (see also `visual-design.md` for the full color language):

- blue font for hardcoded inputs,
- black font for formulas,
- green font for internal links or carried references,
- red font for external links or manual overrides,
- parentheses for negatives,
- dashes for zeros,
- units in headers,
- dates running left to right,
- row labels left-aligned and numerical columns right-aligned.

For banking-style models, hide gridlines, use strong section headers sparingly, and put a clear horizontal border above totals. Totals should generally sum the cells immediately above them, not a grab bag from around the sheet.

### Reconciliation layouts

For reconciliations, use a simple, auditable layout such as:

- item,
- source A,
- source B,
- difference,
- explanation,
- status.

Put unresolved differences in a flagged section. A good reconciliation sheet lets an auditor see what matches, what does not, and why.

### Sensitivity analysis and scenarios

Use one-variable and two-variable data tables or clean scenario blocks when the user needs sensitivity views. Keep the scenario driver cells isolated and clearly named. Label the base case visibly.

For executive reporting, do not dump a giant matrix. Present a focused view: what changed, by how much, and which assumptions drive the movement.

### Audit trail best practices

Document source dates, source systems, and any manual overrides. If a value is hand-entered from a filing, contract, or management input, note the source nearby or in a dedicated assumptions log. High-consequence models should have a checks sheet with obvious pass/fail indicators.

### One formula per row / column discipline

Adopt the Operis-style instinct: across a logical block, formulas should usually be consistent left-to-right or top-to-bottom. If one column breaks the pattern, there should be a reason you can explain immediately.
