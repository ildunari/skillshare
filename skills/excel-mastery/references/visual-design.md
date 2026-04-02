# Visual Design & Formatting

This file covers how to make a workbook readable at speed: typography, color systems, alignment, borders, number formats, conditional formatting, print layout, and accessibility-aware presentation.

See also: `charts-and-visualization.md` for chart-specific guidance, `workbook-architecture.md` for structural decisions, and `review-readiness.md` for final export and handoff checks.

### Typography defaults

Use a professional sans-serif font by default. Aptos, Calibri, Arial, or Helvetica-like fonts are safe. Stick to a single font family unless the workbook has an established brand system that uses multiple.

Good defaults:

- workbook title: 14–16 pt, bold
- section headers: 11–12 pt, bold
- body data: 10–11 pt
- notes / footnotes: 9–10 pt
- chart text: 8–10 pt depending on final size

For publication figures, design at final output size. Tiny chart labels that only look readable when zoomed to 200% are not publication-ready.

### Use color as a language, not decoration

Keep the palette small. Most workbooks need one neutral base, one emphasis color, one caution color, and one error color. More colors usually reduce meaning.

Default general-purpose color logic:

- dark text for labels and formulas,
- one accent color for true emphasis,
- muted gray for secondary scaffolding,
- orange or amber for warnings or review items,
- red only for errors or urgent exceptions,
- green only when it carries a defined meaning, not as generic “pretty.”

For finance, the widely recognized convention is:

- **Blue font:** hardcoded inputs
- **Black font:** formulas and calculations
- **Green font:** internal links or carried references
- **Red font:** external links or exceptional manual overrides
- **Yellow fill:** key assumptions needing review

Use that convention when building finance models unless the user’s house style overrides it. But still do not rely on color alone; pair it with sheet zoning, labels, or notes.

### Accessibility rules

Follow accessible defaults:

- Maintain strong text contrast.
- Pair color with a secondary signal (text, icons, position) so meaning survives grayscale.
- Avoid red/green-only distinctions for critical comparisons.
- Prefer blue/orange, navy/gold, or dark/light contrasts that remain distinct in grayscale.
- Use simple shapes, direct labels, and patterns or markers when charts must differentiate series.
- Keep sheet names unique and descriptive so screen readers and navigation tools are usable.

If a chart or shape is central to understanding and the file is meant for digital sharing, add concise alternative text or an adjacent text explanation.

### Alignment, whitespace, and borders

Use alignment to show data type and role.

- text labels: left-aligned
- dates: consistent alignment within the table
- numbers: right-aligned
- percentages and currencies: right-aligned
- titles: left-aligned unless a formal cover layout demands otherwise

Prefer whitespace and subtle hierarchy over border spam.

- use borders to separate sections, totals, or final outputs,
- avoid boxing every filled cell,
- leave blank rows or columns between major sections,
- freeze panes where headers should stay visible,
- set row heights and column widths so content fits without huge dead space.

If every cell has a border, none of the borders mean anything.

### Number formats

Number format communicates meaning. Use it deliberately.

Default rules:

- dates should look like dates, not serial numbers,
- percentages usually one decimal place unless the scale demands otherwise,
- currency should include the symbol or the unit in the header,
- counts generally no decimals,
- rates and scientific measures should show only precision the data supports,
- large units should be stated in the header: `Revenue ($m)`, `Volume (000s)`, `Mass (mg)`.

Finance defaults:

- negative numbers in parentheses,
- zeros often displayed as dashes,
- multiples as `x`,
- years shown as plain year labels,
- totals visually separated with a top border and bold label.

Show only the precision the data supports. A measurement with ±5% uncertainty displayed to 10 digits misleads the reader.

### Conditional formatting: when it helps vs when it clutters

Use conditional formatting when it reveals a pattern faster than reading the numbers.

Good uses:

- highlight missing required values,
- flag out-of-bounds inputs,
- show top/bottom performers in a ranking,
- show variance signs with a restrained diverging scale,
- identify duplicates,
- show milestone deadlines or overdue items,
- use icon sets sparingly for status dashboards.

Weak uses:

- rainbow heatmaps on small tables with no legend,
- applying color scales to precision tables where exact values matter,
- highlighting every row in a dense dataset,
- conditional formatting layered so heavily that nobody knows what rule won.

Rule design guidance:

- Keep the number of rules small.
- Prefer formula-based rules only when simple built-ins cannot express the logic.
- Use subtle fills, not neon.
- If the format has meaning, include a legend or a nearby note.
- Test performance on large sheets; conditional formatting can make a workbook sluggish.

### Print layout and page design

Excel often ends up on paper or in PDF. Design for that reality.

Always check:

- page orientation,
- margins,
- scaling,
- repeating row or column headers,
- page breaks,
- print area,
- header/footer,
- file title and date stamp if needed.

For print-ready sheets:

- keep each major table intact on a page if possible,
- repeat column headers on subsequent pages,
- put units and period labels on every printed page,
- avoid giant blank regions caused by careless scaling,
- make sure charts are legible at actual print size.

### Clear vs pretty

A workbook communicates clearly when:

- the eye knows where to start,
- inputs and outputs are obvious,
- totals are easy to find,
- related items are grouped,
- a reader can scan it in seconds,
- and no formatting choice requires explanation.

“Pretty” that slows interpretation is failure. Tufte’s data-ink ratio principle applies here too: remove non-informative ink.
