# Charts & Data Visualization

This file covers chart selection, chart formatting, visual storytelling, Tufte and IBCS-informed reporting discipline, small multiples, sparklines, and publication-quality figure export.

See also: `visual-design.md` for typography and color choices, `data-science-statistics.md` for analytical context behind charts, and `review-readiness.md` for final publication and handoff checks.

**Contents:** Chart selection rules (bar, column, line, scatter, histogram, box plot, waterfall, combo, pie, area, small multiples, sparklines) · Format charts for fast reading (titles, legends, gridlines, data labels, axes, reference lines) · Tufte and IBCS · Anti-patterns · Publication-quality export

### Start with the analytical question

Start with the relationship that must be visible, then choose the chart type that reveals it best.

- **Comparison across categories:** bar or column
- **Change over time:** line, column, or sparkline
- **Part-to-whole:** stacked bar/column only when total and components both matter; otherwise use a table or bar chart
- **Distribution:** histogram or box plot
- **Relationship between variables:** scatter plot
- **Bridge from one total to another:** waterfall
- **Actual vs target or actual vs prior:** bar/column with a reference line or variance markers

If exact values matter more than pattern, a table may beat a chart.

### Chart selection rules

#### Bar charts

Use horizontal bars for category comparison, especially when labels are long or there are many categories. Sort deliberately: descending for ranking, logical order for process steps, fixed order for known categories.

Best for:

- top and bottom performers,
- market share by category,
- budget vs actual across departments,
- survey responses by item.

Start bar chart axes at zero — bar length encodes magnitude, and a truncated axis exaggerates small differences.

#### Column charts

Use columns for comparisons when categories are short, limited in number, or naturally ordered in time. For monthly or yearly values, columns are acceptable, but if the message is trend rather than discrete comparison, a line chart is often cleaner.

Best for:

- quarterly revenue,
- year-over-year counts,
- actual vs budget for a few periods.

Avoid crowded clustered columns with too many series. If you have more than three or four series, rethink the design.

#### Line charts

Use lines for time series and ordered sequences. Keep the time axis honest and regular. Line charts are usually the best default for trend, direction, seasonality, and turning points.

Best for:

- monthly sales trends,
- patient response over time,
- headcount growth,
- cumulative performance.

Use markers only when points are sparse or individually important. Heavy markers on dense lines add clutter.

#### Scatter plots

Use scatter plots for relationships between two quantitative variables. This is the right choice for correlation, calibration curves, method comparison, residual review, and dose-response exploratory views.

Best for:

- concentration vs signal,
- height vs weight,
- price vs demand,
- forecast error vs volume.

Do not use line charts when the x-axis is numeric but irregular. Use scatter plots.

#### Histograms

Use histograms for distribution shape: skew, spread, multimodality, and unusual tails. Show bin width deliberately. A bad bin choice can tell a false story.

Best for:

- turnaround times,
- assay measurements,
- transaction amounts,
- residual distributions.

#### Box plots / box-and-whisker charts

Use box plots when comparing distributions across groups and you need median, spread, and potential outliers. They are excellent for side-by-side comparisons but require a statistically literate audience.

Best for:

- treatment groups,
- department performance variability,
- instrument variability across runs.

If the audience is non-technical, pair the box plot with a short note explaining what the box and whiskers represent.

#### Waterfall charts

Use waterfalls for bridges: opening to closing balance, budget to actual, EBITDA bridge, cash bridge, or driver decomposition.

Best for:

- variance analysis,
- bridge from prior year to current year,
- change in net income from drivers.

Label subtotals clearly. Use color with consistent meaning: increase, decrease, subtotal. Do not make the reader guess.

#### Combo charts

Use combo charts only when two display forms genuinely clarify the story, such as columns for actual values plus a line for target. Most dual-axis charts are abused. If the second axis exists only to make two unrelated lines look correlated, do not do it.

Best use:

- actual monthly revenue as columns with target as a line,
- volume columns with capacity line when both scales are plainly labeled.

#### Pie and doughnut charts

Default to sorted bar charts instead of pies. Pie charts work only when there are 2-3 dominant slices, the total equals 100%, and the audience needs just a rough part-to-whole impression.

For anything with many slices, similar values, or a need for precise comparison, a sorted horizontal bar chart communicates the ranking faster and more accurately.

#### Area charts

Use area charts sparingly. They can work for cumulative totals or stacked composition over time, but they often obscure comparisons. If the message is in the total trend, a line chart is cleaner. If the message is in the components, consider small multiples.

#### Small multiples

When comparing many similar time series, use small multiples instead of one spaghetti chart. Give each panel the same axis scale unless there is a very strong reason not to. Tufte’s small-multiple principle is one of the best upgrades you can bring to Excel.

Best for:

- sales by region over time,
- KPIs by product family,
- assay response by condition.

#### Sparklines and in-cell visuals

Use sparklines when the goal is compact pattern recognition inside a table. They are especially strong for dashboards, executive summaries, and side-by-side trend comparisons.

Use sparklines when:

- the chart only needs to show direction and volatility,
- many rows must be compared in a compact space,
- a full chart would waste room.

Add reference markers sparingly. A sparkline should remain a micro-view, not a tiny cluttered chart.

### Format charts for fast reading

#### Titles

A chart title should say the point, not the subject.

**Title rewrites — weak → strong:**

| Weak (describes subject) | Strong (states the point) |
|---|---|
| Revenue by Quarter | Revenue growth slowed after Q2 |
| Patient Response Over Time | Response peaked at week 4 and declined |
| Budget vs Actual | Marketing overspent by 12%; R&D under by 8% |
| Nanoparticle Size Distribution | Batch NP-003 shows bimodal distribution — possible aggregation |
| Release Profile | Burst release of 15% in first hour, then sustained over 72h |

If the workbook already explains context nearby, a subtitle with units and period may be enough.

#### Legends

Use direct labels whenever possible — legends force the eye to travel back and forth between the data and the key.

**Direct label example:** Instead of a legend box reading "Series: North, South, West," place the region name at the endpoint of each line in the chart. In Excel: click a single data point in a series → Add Data Label → position the label at the line end → delete the legend.

If there are only 1-2 series, you can often put the label in the chart title or subtitle instead of using a legend at all.

#### Gridlines

Keep only the minimum needed. Light gray major gridlines are often enough. Minor gridlines are usually clutter.

#### Backgrounds and borders

Remove chart backgrounds, dark fills, drop shadows, bevels, and ornamental borders. Tufte would call most of that chartjunk, and he would be right.

#### Data labels

Use labels when exact values matter or when they eliminate the need for a legend. Do not label every point in a dense line chart. Label endpoints, peaks, lows, or the values central to the message.

#### Axes

Label axes with units. Use sensible tick intervals. Avoid overly granular decimal labels on broad business charts. Bar axes should usually start at zero; line charts may use a narrower range when the purpose is to show change, but do not exaggerate tiny differences.

#### Reference lines

Use reference lines for targets, averages, thresholds, control limits, or prior-period baselines. Make them subtle but readable. A well-placed target line often says more than another data series.

### Apply Tufte and IBCS on purpose

Use Tufte’s principles as defaults:

- maximize data-ink ratio,
- remove chartjunk,
- prefer direct labeling,
- use small multiples for repeated comparisons,
- use sparklines for dense summaries,
- and let information, not decoration, dominate the canvas.

Use IBCS SUCCESS rules for business reporting:

- **Say:** each exhibit should have one message,
- **Unify:** keep notation, scales, colors, and periods consistent,
- **Condense:** show only what supports the message,
- **Check:** ensure correctness and consistency,
- **Express:** choose the right visual form,
- **Simplify:** reduce non-essential content,
- **Structure:** organize reports in a logical story.

Adopt IBCS-style notation where helpful:

- actual = solid dark,
- prior year = muted or gray,
- forecast/plan = outlined or otherwise consistently distinguished,
- variances = explicit plus/minus treatment.

Do not imitate IBCS halfway. The power comes from consistency across the workbook.

### Chart defaults that protect against common mistakes

Default to 2D chart types — 3D distorts area perception and adds no information. Use sorted horizontal bar charts instead of pie charts when comparing more than 3 categories. Choose a restrained palette of 3-5 colors with accessible contrast instead of rainbow schemes.

Start bar chart axes at zero, since bar length encodes magnitude. Use direct labels instead of legends when there are fewer than 4 series. For dual-axis charts, verify that the two scales tell a real story — if they exist only to force unrelated lines onto the same chart, use separate panels instead.

Label every axis with units. Strip decorative shadows, gradients, bevels, and glossy effects — Tufte would call them chartjunk, and reviewers will too. If a chart shows the same information as the adjacent table without adding analytical insight (trend, pattern, comparison), remove the chart or redesign it to reveal something the table doesn't.

### Publication-quality export settings

For journal or report figures:

- design at final figure size,
- use clean sans-serif text,
- make labels readable at final size,
- prefer vector export when accepted,
- if raster is required, 300 dpi is a safe floor and 600 dpi is better for line work or small text,
- use color-blind-safe contrasts,
- embed or preserve fonts when the workflow allows,
- avoid pasted screenshots of charts.

If a figure is going to Nature-, Science-, Cell-, or PLOS-style review, assume the reviewer will zoom in and judge every axis label, tick mark, unit, and legend choice.
