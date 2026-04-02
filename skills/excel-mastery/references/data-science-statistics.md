# Data Science & Statistical Analysis

This file covers data cleaning, descriptive statistics, outlier handling, PivotTables, regression, hypothesis testing, sample-size caution, and common analytical mistakes that Excel users make when moving too fast.

See also: `charts-and-visualization.md` for displaying statistical results, `engineering-scientific.md` for lab-specific analysis patterns, and `review-readiness.md` for final QA before results are handed off.

### Clean the data before analysis

Clean before analyzing. Use a checklist to catch issues before they contaminate results.

Check for:

- duplicate rows or duplicate keys,
- blanks in required fields,
- mixed data types within a column,
- inconsistent date formats,
- units mixed in the same field,
- hidden leading or trailing spaces,
- category spelling variants,
- impossible values,
- outliers that may be entry errors,
- and rows outside the intended population or time window.

Keep raw data intact if possible. Clean in a staging area, not by destructively rewriting the source.

If the import/cleanup will repeat, use Power Query when available rather than redoing manual steps every time.

### Build proper summary tables

A good descriptive statistics table usually includes:

- `n`,
- mean,
- median,
- standard deviation,
- interquartile range when skew matters,
- minimum,
- maximum,
- and missing count when missingness is relevant.

When the distribution is clearly skewed, report median and IQR rather than (or alongside) the mean. For grouped comparisons, place metrics in rows and groups in columns or vice versa, but keep the structure consistent.

### Outlier identification

Treat outliers as a workflow, not a cosmetic problem.

Use outlier review to ask:

- is it a data entry error?
- a measurement error?
- a valid but rare observation?
- a different subpopulation?

Show the effect of the outlier on the result when the conclusion could change. Keep outliers unless there is a documented, defensible reason for exclusion (data entry error, known instrument failure, different population). If excluded, state the rule and show the effect on results with and without the point.

### PivotTables: when they are right and when they are not

Use PivotTables for fast summarization of clean, tabular data. They are excellent for:

- aggregation by category or period,
- quick exploratory analysis,
- drill-down summaries,
- interactive slicing by segment,
- crosstabs for counts, sums, averages, and shares.

Design PivotTables well:

- start from a clean Table,
- keep field names short and unambiguous,
- set number formats inside the PivotTable,
- rename value fields to human-readable labels,
- group dates thoughtfully,
- sort deliberately,
- add slicers only when someone will actually use them.

Do not use PivotTables as hidden business logic. If the transformation must be fully transparent and reproducible line by line, use explicit formulas or Power Query instead.

### Calculated fields and grouping

Use calculated fields only for simple arithmetic inside the PivotTable. If the logic is more complex than that, calculate it upstream. Group dates into months, quarters, or years only when the analytical question calls for aggregation.

Be careful with averages in pivots; averages of averages are often wrong. Weighting matters.

### Regression and correlation

Use correlation to describe association, not causation. Inspect a scatter plot before trusting a correlation coefficient — outliers, nonlinearity, and clustering can all distort the number.

For regression work:

- inspect the scatter first,
- check for nonlinearity,
- review residuals if the decision matters,
- look for influential points,
- know whether the intercept should be forced or estimated,
- and report units and interpretation in plain language.

Do not claim “X drives Y” from a simple regression unless the study design supports a causal statement.

### Using the Analysis ToolPak correctly

The Analysis ToolPak is fine for standard procedures, but you still need judgment. Verify:

- the data range is correct,
- labels are identified correctly,
- missing data is handled consistently,
- grouping variables are aligned with observations,
- and the output is placed somewhere readable.

Interpret ToolPak output before including it in a final report — raw statistical tables without context are noise to non-technical readers.

### Hypothesis testing in Excel

Use Excel tests only when the assumptions are understood.

- **t-tests:** check independence or pairing, variance assumption, and whether the tails match the question.
- **ANOVA:** check grouping logic and whether comparing means across groups is actually the right question.
- **Chi-square:** use counts, not percentages or means, and ensure expected counts are not absurdly small.

Always pair the test result with effect size, direction, and sample size. Statistical significance without context is weak reporting.

### Common errors to catch

Catch these before the user has to:

- correlation mistaken for causation,
- averaging percentages without weighting,
- Simpson’s paradox across subgroups,
- base-rate neglect,
- comparing groups with very different `n` as if precision were equal,
- cherry-picking periods,
- p-hacking through repeated slicing until something becomes “significant,”
- reporting only favorable models,
- treating `p > 0.05` as proof of no effect.

### Sample size and power

If the sample is small, say so. If the analysis is underpowered, say so. A non-significant result in a tiny sample is not strong evidence of absence. When planning or reviewing studies, note whether the design can reasonably detect the effect size that matters.
