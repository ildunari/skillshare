---
name: python-visualization
description: "Unified toolkit for all Python data visualization. Use when creating any Python plot, chart, visualization, animation, molecular structure, or styled table. Covers: matplotlib (static plots, OO interface), seaborn (statistical graphics), Plotly (interactive charts, 3D, dashboards, HTML export), matplotlib animations (GIF/MP4 export via FuncAnimation), pandas Styler (formatted DataFrames, heatmap tables, HTML/LaTeX export), RDKit/py3Dmol (molecular rendering, 2D/3D structures, similarity maps), biomedical plots (dose-response, PK profiles, drug release kinetics, Kaplan-Meier), and LaTeX figure integration (text.usetex, PGF backend, font matching, subfigure export). Triggers on: any Python plot, interactive chart, Plotly, animated figure, GIF from matplotlib, styled DataFrame, molecular visualization, RDKit, drug delivery plot, pharmacokinetics, LaTeX figure, publication figure."
---

# Python Visualization

> Unified skill for all Python data visualization: matplotlib, seaborn, Plotly, animations, pandas Styler, RDKit molecular rendering, biomedical plots, and LaTeX integration. One skill, one routing table.

## When to Use This Skill

- Creating any plot or chart in Python (line, scatter, bar, histogram, heatmap, contour, 3D, etc.)
- Statistical visualizations (distributions, regressions, categorical comparisons)
- Publication-ready figures for journal submission
- Multi-panel figures with consistent styling
- Colorblind-accessible visualizations
- Exporting figures at correct resolution and format
- Interactive/web-based charts with hover, zoom, pan (Plotly)
- Animated plots, GIF/MP4 export for presentations or supplementary materials
- Styled pandas DataFrames with conditional formatting, heatmaps, bar charts in cells
- Molecular structure visualization (2D grids, 3D interactive, similarity maps)
- Biomedical-specific plots (dose-response, PK curves, release kinetics, survival curves)
- LaTeX-integrated figures with matched fonts, exact column widths, PGF/PDF export

## Routing Table

Load only the references needed for the task. Multiple files often apply.

### Matplotlib (core)

| Task | Load |
|---|---|
| API lookup (functions, parameters, return types) | `references/matplotlib-api.md` |
| Choosing a plot type | `references/matplotlib-plot-types.md` |
| Styling, colors, fonts, themes | `references/matplotlib-styling.md` |
| Debugging common issues | `references/matplotlib-common-issues.md` |

### Seaborn (statistical)

| Task | Load |
|---|---|
| Function reference (all plot types, parameters) | `references/seaborn-functions.md` |
| Modern objects interface (ggplot2-style declarative) | `references/seaborn-objects-interface.md` |
| Usage examples and patterns | `references/seaborn-examples.md` |

### Publication Quality

| Task | Load |
|---|---|
| General publication best practices | `references/publication-guidelines.md` |
| Journal-specific requirements (Nature, Science, Cell, etc.) | `references/journal-requirements.md` |
| Colorblind-safe palettes and accessibility | `references/color-palettes.md` |
| Publication figure examples | `references/publication-examples.md` |

### Plotly (interactive)

| Task | Load |
|---|---|
| Plotly Express vs Graph Objects decision + API reference | `references/plotly-api.md` |
| Interactive features (hover, buttons, dropdowns, sliders, animations) | `references/plotly-interactivity.md` |
| 3D plots, subplots, and dashboard layouts | `references/plotly-advanced.md` |
| Export (HTML, static image via Kaleido, PDF) | `references/plotly-export.md` |

### Animations

| Task | Load |
|---|---|
| FuncAnimation / ArtistAnimation patterns + GIF/MP4 export | `references/animation-guide.md` |
| Plotly animated figures (frames, sliders, play buttons) | `references/plotly-interactivity.md` |

### Pandas styled tables

| Task | Load |
|---|---|
| Styler API, conditional formatting, heatmaps, bar-in-cell, export | `references/pandas-styler.md` |

### Biomedical visualization

| Task | Load |
|---|---|
| RDKit 2D molecular drawing (grids, substructure highlighting, SVG) | `references/rdkit-visualization.md` |
| 3D molecular visualization (py3Dmol, conformer rendering) | `references/molecular-3d.md` |
| PK/PD curves, dose-response, drug release kinetics, Kaplan-Meier | `references/biomedical-plots.md` |

### LaTeX integration

| Task | Load |
|---|---|
| text.usetex, PGF backend, font matching, journal column widths | `references/latex-integration.md` |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/plot_template.py` | Starter template for matplotlib figures |
| `scripts/style_configurator.py` | Programmatic style configuration |
| `scripts/figure_export.py` | Multi-format export (PDF, PNG, SVG) with DPI control |
| `scripts/style_presets.py` | Journal-specific style presets |
| `scripts/plotly_template.py` | Plotly Express + Graph Objects starter templates with export helpers |
| `scripts/animation_template.py` | FuncAnimation boilerplate with GIF/MP4 save helpers |
| `scripts/styled_table.py` | Pandas Styler presets (summary stats, correlation, comparison) |
| `scripts/rdkit_helpers.py` | Molecular grid generation, SMILES validation, property overlay |
| `scripts/biomedical_templates.py` | Dose-response, PK, drug release, Kaplan-Meier templates with fitting |
| `scripts/latex_figure.py` | Journal width calculator, LaTeX-compatible export, subfigure batch |

## Style Assets

Pre-configured matplotlib style files in `assets/`:

| File | Use |
|---|---|
| `assets/nature.mplstyle` | Nature journal specifications |
| `assets/publication.mplstyle` | General publication defaults |
| `assets/presentation.mplstyle` | Larger fonts/lines for slides |
| `assets/color_palettes.py` | Colorblind-safe palette definitions |
| `assets/latex.mplstyle` | LaTeX-compatible defaults (usetex, Computer Modern, tight sizing) |
| `assets/latex-arial.mplstyle` | LaTeX + Arial for Nature and similar bio journals |
| `assets/plotly_publication.py` | Plotly template matching publication aesthetics |
| `assets/biomedical_palettes.py` | Color palettes for biomedical figures (treatment groups, organs) |

Apply with `plt.style.use('assets/nature.mplstyle')` or via `scripts/style_presets.py`.

## Decision Guide

**Which library for the task?**

| Situation | Use |
|---|---|
| Quick single plot, full control over every element | matplotlib (OO interface) |
| Statistical relationships, distributions, categories | seaborn |
| Faceted multi-panel with automatic grouping | seaborn `relplot`/`catplot`/`displot` |
| ggplot2-style declarative layering | seaborn objects interface |
| Journal submission with specific requirements | matplotlib + publication style presets |
| Colorblind-accessible scientific figure | matplotlib + `color-palettes.md` |
| Interactive chart with hover/zoom/pan | Plotly Express (simple) or Graph Objects (custom) |
| Dashboard with multiple linked interactive panels | Plotly subplots + shared axes |
| 3D scatter/surface needing rotation | Plotly (interactive) or matplotlib (static publication) |
| Animated plot for presentation/supplementary | matplotlib FuncAnimation → GIF/MP4 |
| Animated interactive chart (web) | Plotly frames + slider |
| Styled summary table in notebook or report | pandas Styler |
| Export formatted table to LaTeX doc | pandas Styler `.to_latex()` |
| Molecular structure grid (2D, from SMILES) | RDKit `Draw.MolsToGridImage` |
| Interactive 3D molecule viewer | py3Dmol |
| Dose-response / IC50 curve | matplotlib + scipy curve_fit → `biomedical-plots.md` |
| PK profile (concentration vs time) | matplotlib with semi-log → `biomedical-plots.md` |
| Drug release kinetics | matplotlib with model overlays → `biomedical-plots.md` |
| Figures matching LaTeX document fonts exactly | matplotlib + `text.usetex: True` + PGF backend |
| Figures sized to journal column width | matplotlib + `latex-integration.md` width calculator |

**Always prefer the matplotlib Object-Oriented interface** (`fig, ax = plt.subplots()`) over the pyplot stateful interface for anything beyond a throwaway one-liner.

**Seaborn builds on matplotlib.** You can always drop down to matplotlib for fine-tuning after creating a seaborn plot — they share the same Figure/Axes objects.

## Label Placement Rules

LLM-generated matplotlib code has a systematic blind spot: **labels are generated without visual feedback**, so small errors accumulate and produce collisions that are invisible in code but immediately obvious in the rendered figure. Follow these rules for every chart with text annotations.

### Offsets must be relative, not hardcoded

Never use hardcoded data-unit offsets for annotations. Hardcoded values work for example data and break silently when units or scale change.

```python
# BAD — breaks when y-axis is 0-1 or 0-10000
ax.annotate('IC50', xy=(ic50, mid_y), xytext=(ic50*5, mid_y + 15))

# GOOD — stays on-canvas for any scale
ylo, yhi = ax.get_ylim()
y_offset = 0.15 * (yhi - ylo)
ax.annotate('IC50', xy=(ic50, mid_y), xytext=(ic50*5, mid_y + y_offset))

# EVEN BETTER — use axes fraction for text, data coords for the arrow target
ax.annotate('Cmax', xy=(tmax, cmax), xytext=(0.6, 0.85),
            xycoords='data', textcoords='axes fraction',
            arrowprops=dict(arrowstyle='->'))
```

### Stagger labels at the same x/y position

When multiple vertical or horizontal lines share the same label y/x position, stagger them:

```python
# BAD — all three at identical y → collision when lines are close
for val, lbl in [(d10,'D10'), (d50,'D50'), (d90,'D90')]:
    ax.text(val, ax.get_ylim()[1]*0.95, lbl, ha='center')

# GOOD — alternating lanes
ylo, yhi = ax.get_ylim()
y_levels = [0.92, 0.76, 0.60]
for (val, lbl), y_frac in zip([(d10,'D10'),(d50,'D50'),(d90,'D90')], y_levels):
    ax.text(val, ylo + y_frac*(yhi - ylo), lbl, ha='center',
            bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.6, lw=0))
```

### Gate per-cell annotations on matrix dimensions

Dense heatmaps with text annotations on every cell become illegible fast. Only annotate if both dimensions are ≤ 15:

```python
rows, cols = matrix.shape
if rows <= 15 and cols <= 15:
    fontsize = max(5, 9 - max(rows, cols) // 3)
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, f'{matrix[i,j]:.2f}', ha='center', va='center',
                    fontsize=fontsize)
```

### Significance brackets: derive position from data

```python
yhi = ax.get_ylim()[1]
bar_top = bar_height + error
y = bar_top + 0.04 * yhi    # 4% breathing room
h = 0.02 * yhi              # bracket arm height
ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], 'k-', lw=0.8)
ax.text((x1+x2)/2, y+h, '***', ha='center', va='bottom', fontsize=7)
```

### Panel labels: know when to increase x-offset

Standard offset `-0.15` in axes fraction works for short y-labels. If your y-axis label is long (e.g., "Plasma Concentration (ng/mL)"), use `-0.25` or more to avoid overlap:

```python
ax.text(-0.15, 1.05, 'A', transform=ax.transAxes, fontsize=10, fontweight='bold')
# With long y-label: use -0.25 or -0.30
```

## Core Patterns

### Standard matplotlib figure

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
```

### Seaborn statistical plot

```python
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset('tips')
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()
```

### Publication-ready figure

```python
import matplotlib.pyplot as plt
plt.style.use('assets/nature.mplstyle')

fig, ax = plt.subplots(figsize=(3.5, 2.5))  # Nature single-column width
# ... plotting code ...
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

### Interactive Plotly chart

```python
import plotly.express as px

df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop",
                 color="continent", hover_name="country", log_x=True)
fig.show()
fig.write_html("figure.html")
```

### Animated matplotlib → GIF

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot([], [])
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-1, 1)

def animate(i):
    line.set_data(x[:i], np.sin(x[:i]))
    return line,

ani = animation.FuncAnimation(fig, animate, frames=len(x), interval=30, blit=True)
ani.save('sine.gif', writer='pillow', fps=30)
```

### Styled pandas table

```python
import pandas as pd

styled = (df.style
    .format(precision=2)
    .highlight_max(color='lightgreen')
    .highlight_min(color='lightcoral')
    .background_gradient(subset=['value'], cmap='Blues'))
styled.to_html('table.html')
```

### RDKit molecular grid

```python
from rdkit import Chem
from rdkit.Chem import Draw

smiles = ['CCO', 'c1ccccc1', 'CC(=O)O']
mols = [Chem.MolFromSmiles(s) for s in smiles]
img = Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(300, 300))
img.save('molecules.png')
```

## Feedback Loop

This skill uses a feedback log to improve over time. The cycle:

1. **Detect** — After completing a task, note anything suboptimal.
2. **Search** — Check `FEEDBACK.md` for prior entries on the same topic.
3. **Scope** — Keep entries to 1–3 lines: category tag, what happened, what should change.
4. **Draft & Ask** — Draft the entry and show it to the user before writing.
5. **Write on Approval** — Append to `FEEDBACK.md`.
6. **Compact at 75** — Summarize older entries when the file reaches 75 entries.

**Always read `FEEDBACK.md` when reading this skill.**
