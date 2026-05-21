# Pandas Styler Reference

Formatting and styling DataFrames for notebooks, reports, and publication tables.


## Contents

- [Core Concept](#core-concept)
- [Formatting Values](#formatting-values)
- [Built-in Highlighting](#built-in-highlighting)
- [Background Gradient (Heatmap)](#background-gradient-heatmap)
- [Bar Charts in Cells](#bar-charts-in-cells)
- [Custom Styling Functions](#custom-styling-functions)
- [Table Structure and Presentation](#table-structure-and-presentation)
- [Export](#export)
- [Common Patterns](#common-patterns)
- [Performance Notes](#performance-notes)

## Core Concept

`df.style` returns a `Styler` object. Chain methods to build up styling, then render or export. Styling is **display only** — the underlying data is never modified.

```python
import pandas as pd
import numpy as np

styled = (df.style
    .format(precision=2)
    .highlight_max(color='lightgreen')
    .set_caption('Table 1: Summary Statistics'))
styled  # renders in Jupyter
```

## Formatting Values

### format()

```python
# Fixed precision
df.style.format(precision=3)

# Per-column formatting
df.style.format({
    'price': '${:.2f}',
    'change': '{:+.1%}',
    'volume': '{:,.0f}',
    'date': lambda x: x.strftime('%Y-%m-%d'),
})

# Missing values
df.style.format(na_rep='—', precision=2)

# Thousands separator
df.style.format(thousands=',', decimal='.', precision=2)
```

### format_index()

```python
df.style.format_index(str.upper, axis=1)          # uppercase column headers
df.style.format_index('{:.1f}'.format, axis=0)     # format row index
```

### relabel_index()

```python
df.style.relabel_index(['Row A', 'Row B', 'Row C'], axis=0)
df.style.relabel_index(['Col 1', 'Col 2'], axis=1)
```

## Built-in Highlighting

### Extreme values

```python
df.style.highlight_max(color='lightgreen', axis=0)   # max per column
df.style.highlight_min(color='lightcoral', axis=0)    # min per column
df.style.highlight_max(subset=['score', 'value'])      # specific columns only

# Both together
df.style.highlight_max(color='#c6efce').highlight_min(color='#ffc7ce')
```

### Range highlighting

```python
df.style.highlight_between(left=0.5, right=1.5, color='lightyellow')
df.style.highlight_between(subset=['pH'], left=6.8, right=7.4, color='lightgreen')
```

### Quantile highlighting

```python
df.style.highlight_quantile(q_left=0.0, q_right=0.25, color='lightblue', axis=0)
```

### Null highlighting

```python
df.style.highlight_null(color='red')
```

## Background Gradient (Heatmap)

```python
# Full DataFrame heatmap
df.style.background_gradient(cmap='Blues')

# Specific columns
df.style.background_gradient(subset=['temp', 'pressure'], cmap='RdYlBu_r')

# By row (axis=1) instead of column
df.style.background_gradient(cmap='viridis', axis=1)

# Custom range (vmin/vmax)
df.style.background_gradient(cmap='coolwarm', vmin=-1, vmax=1, subset=['correlation'])

# Text color gradient (instead of background)
df.style.text_gradient(cmap='RdYlGn', subset=['change'])
```

**Colormap selection:**
- Sequential: `Blues`, `Greens`, `Oranges`, `Purples`, `viridis`, `plasma`
- Diverging: `RdYlBu_r`, `coolwarm`, `RdBu_r`, `PiYG` (center on zero)
- Use `_r` suffix to reverse any colormap

## Bar Charts in Cells

```python
# Basic bars
df.style.bar(subset=['score'], color='steelblue', width=80)

# Dual-color for positive/negative
df.style.bar(subset=['change'], color=['#d65f5f', '#5fba7d'],
             align='mid', width=70)

# With custom range
df.style.bar(subset=['value'], vmin=0, vmax=100, color='lightblue')
```

## Custom Styling Functions

### map() — elementwise

```python
def color_negative(val):
    color = 'red' if val < 0 else 'black'
    return f'color: {color}'

df.style.map(color_negative, subset=['profit', 'change'])

# Lambda version
df.style.map(lambda v: 'font-weight: bold' if v > 100 else '', subset=['score'])
```

### apply() — column/row-wise

```python
def highlight_above_mean(series):
    mean = series.mean()
    return ['background-color: lightgreen' if v > mean else '' for v in series]

df.style.apply(highlight_above_mean, subset=['value'])

# Row-wise (axis=1)
def highlight_max_in_row(row):
    is_max = row == row.max()
    return ['font-weight: bold' if v else '' for v in is_max]

df.style.apply(highlight_max_in_row, axis=1)
```

### Returning CSS strings

Style functions must return strings of `'property: value'` pairs or `''` for no style.

```python
# Multiple CSS properties
def style_cell(val):
    if val > 90:
        return 'background-color: #c6efce; color: #006100; font-weight: bold'
    elif val < 50:
        return 'background-color: #ffc7ce; color: #9c0006'
    return ''
```

## Table Structure and Presentation

### Caption

```python
df.style.set_caption('Table 1: Experimental results for polymer degradation study')
```

### Table-level CSS

```python
df.style.set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#f0f0f0'),
                                  ('font-weight', 'bold'),
                                  ('text-align', 'center')]},
    {'selector': 'td', 'props': [('text-align', 'right'),
                                  ('padding', '4px 8px')]},
    {'selector': 'caption', 'props': [('caption-side', 'top'),
                                       ('font-style', 'italic')]},
])
```

### Cell-level properties

```python
df.style.set_properties(**{
    'text-align': 'center',
    'border': '1px solid #ddd',
})

# Specific columns
df.style.set_properties(subset=['name'], **{'text-align': 'left', 'font-weight': 'bold'})
```

### Hiding index/columns

```python
df.style.hide(axis='index')                    # hide row index
df.style.hide(subset=['internal_id'], axis=1)  # hide specific columns
```

### Table attributes

```python
df.style.set_table_attributes('class="my-table" style="width: 100%"')
```

## Export

### HTML

```python
# HTML string
html = df.style.format(precision=2).to_html()

# Standalone HTML file
html = df.style.format(precision=2).to_html(doctype_html=True)
with open('table.html', 'w') as f:
    f.write(html)

# Without style IDs (cleaner HTML)
html = df.style.to_html(exclude_styles=True)
```

### LaTeX

```python
latex = df.style.format(precision=3).to_latex(
    caption='Experimental Results',
    label='tab:results',
    position='htbp',
    position_float='centering',
    hrules=True,                    # \toprule, \midrule, \bottomrule
    column_format='lrrr',           # LaTeX column alignment
)

with open('table.tex', 'w') as f:
    f.write(latex)
```

**Note:** LaTeX export supports a subset of styling. Background colors and gradients work. Complex CSS does not transfer. For best results, keep LaTeX tables simple and add formatting in LaTeX directly.

### Excel (styled)

```python
# Conditional formatting transfers to Excel via openpyxl
df.style.background_gradient(cmap='Blues').to_excel('output.xlsx', engine='openpyxl')
```

### Image (screenshot)

No built-in method. Options:
1. Export HTML, then use `imgkit` or `selenium` to screenshot
2. Use `dataframe_image` package: `pip install dataframe_image`
3. In matplotlib: render as table artist (see below)

```python
# matplotlib table rendering
fig, ax = plt.subplots(figsize=(8, 3))
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns,
                 cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.auto_set_column_width(col=list(range(len(df.columns))))
fig.savefig('table.png', dpi=200, bbox_inches='tight')
```

## Common Patterns

### Summary statistics table

```python
summary = df.describe().T
styled = (summary.style
    .format(precision=2)
    .background_gradient(subset=['mean'], cmap='Blues')
    .background_gradient(subset=['std'], cmap='Oranges')
    .bar(subset=['count'], color='lightblue')
    .set_caption('Table: Descriptive Statistics')
)
```

### Correlation matrix with highlighting

```python
corr = df.select_dtypes(include='number').corr()
styled = (corr.style
    .background_gradient(cmap='coolwarm', vmin=-1, vmax=1)
    .format(precision=3)
    .set_caption('Correlation Matrix')
)
```

### Comparison table (before/after, treatment/control)

```python
def highlight_improvement(row):
    styles = [''] * len(row)
    if row['after'] > row['before']:
        styles[row.index.get_loc('after')] = 'background-color: #c6efce'
    elif row['after'] < row['before']:
        styles[row.index.get_loc('after')] = 'background-color: #ffc7ce'
    return styles

df.style.apply(highlight_improvement, axis=1)
```

### Lab results with threshold coloring

```python
thresholds = {'pH': (6.8, 7.4), 'temperature': (20, 25), 'conductivity': (0, 500)}

def flag_out_of_range(val, col):
    if col in thresholds:
        low, high = thresholds[col]
        if val < low or val > high:
            return 'background-color: #ffc7ce; font-weight: bold'
    return ''

for col in thresholds:
    df.style.map(lambda v, c=col: flag_out_of_range(v, c), subset=[col])
```

## Performance Notes

- Styler is designed for **small-to-medium DataFrames** (hundreds of rows, not millions).
- For large data: style `df.head(50)` or aggregate first, then style the summary.
- Each `.map()` / `.apply()` call iterates over cells — chaining many is fine for small data but slow for large.
- HTML output size grows with cell count. Tables >1000 rows may be slow to render in browsers.