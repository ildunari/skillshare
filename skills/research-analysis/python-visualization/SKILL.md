---
name: python-visualization
description: "Unified toolkit for all Python data visualization. Use when creating any Python plot, chart, visualization, animation, molecular structure, or styled table. Covers: matplotlib (static plots, OO interface), seaborn (statistical graphics), Plotly (interactive charts, 3D, dashboards, HTML export), matplotlib animations (GIF/MP4 export via FuncAnimation), pandas Styler (formatted DataFrames, heatmap tables, HTML/LaTeX export), RDKit/py3Dmol (molecular rendering, 2D/3D structures, similarity maps), biomedical plots (dose-response, PK profiles, drug release kinetics, Kaplan-Meier), and LaTeX figure integration (text.usetex, PGF backend, font matching, subfigure export). Triggers on: any Python plot, interactive chart, Plotly, animated figure, GIF from matplotlib, styled DataFrame, molecular visualization, RDKit, drug delivery plot, pharmacokinetics, LaTeX figure, publication figure."
---

# Python Visualization

> Unified skill for all Python data visualization: matplotlib, seaborn, Plotly, animations, pandas Styler, RDKit molecular rendering, biomedical plots, and LaTeX integration. One skill, one routing table.

## Startup Checklist

Before writing code, complete these steps:

1. **Read `FEEDBACK.md`** if it exists — prior corrections apply immediately.
2. **Identify required libraries** from the task. Run a dependency check (see below) before generating code that imports a library you haven't confirmed is installed.
3. **Determine output target**: interactive notebook, headless script, or CI/server. Choose backend accordingly.

### Dependency check (run before generating imports)

```bash
python - <<'PY'
import importlib, sys
libs = {
    'matplotlib': '3.7', 'seaborn': '0.12', 'plotly': '5.0',
    'pandas': '1.5', 'numpy': '1.23', 'scipy': '1.10',
    'rdkit': None, 'py3Dmol': None, 'pillow': None, 'kaleido': None,
}
for lib, min_ver in libs.items():
    try:
        m = importlib.import_module(lib)
        ver = getattr(m, '__version__', 'unknown')
        status = f"OK ({ver})"
    except ImportError:
        status = "MISSING"
    print(f"{lib:20s} {status}")
PY
```

Only import libraries confirmed as installed. If a required library is missing, show the install command before proceeding: `pip install <package>`.

**Known install names that differ from import names:**
- `import PIL` → `pip install pillow`
- `import plotly` + static images → `pip install kaleido`
- `import rdkit` → `pip install rdkit` (or `conda install -c conda-forge rdkit`)
- GIF export → `pip install pillow` (writer='pillow')
- MP4 export → requires system `ffmpeg` (`brew install ffmpeg` / `apt install ffmpeg`)

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

**Applying style assets:** Use an absolute path derived from this skill's location, not a bare relative path. Bare `plt.style.use('assets/nature.mplstyle')` only works if the script's CWD is the skill root.

```python
from pathlib import Path
SKILL_DIR = Path(__file__).parent  # or set explicitly
plt.style.use(str(SKILL_DIR / 'assets' / 'nature.mplstyle'))
```

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

## Backend and Environment

Set the backend **before** importing `pyplot`. Scripts that run headlessly (servers, CI, cron) must use a non-interactive backend or they will either hang or fail.

```python
import matplotlib
matplotlib.use('Agg')  # must come before: import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
```

In Jupyter notebooks, the backend is managed by the kernel; do not call `matplotlib.use()` in notebook cells. Use `%matplotlib inline` or `%matplotlib widget` instead.

**`plt.show()` vs `fig.savefig()`:**
- In scripts: call `fig.savefig(...)` and skip `plt.show()` — `show()` blocks the process in interactive mode and does nothing headlessly.
- In notebooks: `plt.show()` is acceptable but `display(fig)` is more explicit.
- Always call `plt.close(fig)` after saving in loops or batch jobs to avoid memory accumulation.

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

## Anti-Patterns

Avoid these — each causes silent failures or produces wrong output:

| Anti-pattern | Problem | Fix |
|---|---|---|
| `plt.figure()` + `plt.subplot()` for multi-panel | Stateful — panels can bleed into each other | Use `fig, axes = plt.subplots(nrows, ncols)` |
| `plt.show()` before `fig.savefig()` | `show()` clears the figure on some backends | Always `savefig()` first |
| Hardcoded annotation offsets in data units | Breaks when scale changes | Use axes-fraction or relative offsets |
| `from figure_export import save_publication_figure` without sys.path setup | ImportError unless scripts/ is on PYTHONPATH | Add `sys.path.insert(0, str(SKILL_DIR / 'scripts'))` first |
| `plt.style.use('assets/nature.mplstyle')` with bare path | FileNotFoundError unless CWD is skill root | Use absolute path via `Path(__file__).parent` |
| `ani.save('out.gif', writer='pillow')` without confirming pillow installed | Runtime error at save time | Run dependency check first |
| `ani.save('out.mp4', writer='ffmpeg')` without ffmpeg on PATH | Runtime error; ffmpeg is a system binary | Confirm `ffmpeg -version` succeeds |
| Not filtering `None` from `Chem.MolFromSmiles(...)` | Crash in `Draw.MolsToGridImage` | Filter: `mols = [m for m in mols if m is not None]` |
| Creating many figures in a loop without `plt.close(fig)` | Memory leak, eventually OOM | Always `plt.close(fig)` after saving |

## Core Patterns

### Standard matplotlib figure

```python
import matplotlib
matplotlib.use('Agg')  # omit in Jupyter; required in headless scripts
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6.5, 4))  # general-purpose size; use 3.5 for single-col journal
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
plt.close(fig)
```

**Verify the output exists:**
```bash
python -c "from pathlib import Path; p=Path('figure.png'); print(p, p.stat().st_size, 'bytes')"
```

### Seaborn statistical plot

```python
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset('tips')
fig, ax = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day', ax=ax)
fig.savefig('tips_scatter.png', dpi=150, bbox_inches='tight')
plt.close(fig)
```

### Publication-ready figure

```python
import sys
from pathlib import Path
SKILL_DIR = Path('/path/to/python-visualization')  # set to actual skill path
sys.path.insert(0, str(SKILL_DIR / 'scripts'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use(str(SKILL_DIR / 'assets' / 'nature.mplstyle'))

from figure_export import save_publication_figure

fig, ax = plt.subplots(figsize=(3.5, 2.5))  # Nature single-column width
# ... plotting code ...
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
plt.close(fig)
```

### Interactive Plotly chart

```python
import plotly.express as px

df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop",
                 color="continent", hover_name="country", log_x=True)
fig.write_html("figure.html")  # save first; use fig.show() only in interactive sessions
```

**For static image export** (requires `pip install kaleido`):
```python
fig.write_image("figure.png", width=800, height=600, scale=2)
```

### Animated matplotlib → GIF

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.1, 1.1)
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return (line,)

def animate(i):
    line.set_data(x[:i+1], np.sin(x[:i+1]))
    return (line,)

ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(x), interval=30, blit=True)
ani.save('sine.gif', writer='pillow', fps=30)
plt.close(fig)
```

**Verify:** `python -c "from pathlib import Path; p=Path('sine.gif'); print(p.stat().st_size, 'bytes')"` — should be > 0.

### Styled pandas table

```python
import pandas as pd
import numpy as np

# Construct or load your DataFrame first
df = pd.DataFrame({'A': np.random.rand(5), 'B': np.random.rand(5), 'value': np.arange(5)})

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

smiles_list = ['CCO', 'c1ccccc1', 'CC(=O)O', 'INVALID_SMILES']
mols_raw = [Chem.MolFromSmiles(s) for s in smiles_list]
mols = [m for m in mols_raw if m is not None]  # filter invalid SMILES

if not mols:
    raise ValueError("No valid molecules — check SMILES strings")

img = Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(300, 300))
img.save('molecules.png')
```

## Verification Checklist

After generating and running code, confirm:

- [ ] Output file exists and is non-zero bytes: `ls -lh <output_file>`
- [ ] No import errors (run `python -c "import <lib>"` for each dependency used)
- [ ] For GIF: file opens in an image viewer or `file sine.gif` shows "GIF data"
- [ ] For Plotly HTML: `grep -c 'plotly' figure.html` returns > 0
- [ ] For publication figures: `identify -verbose figure.png | grep 'Resolution'` (ImageMagick) confirms DPI ≥ 300
- [ ] For RDKit grids: molecule count in output matches `len(mols)` after filtering

## Feedback Loop

This skill uses a feedback log to improve over time. The cycle:

1. **Read first** — Always read `FEEDBACK.md` before starting any task (covered in Startup Checklist).
2. **Detect** — After completing a task, note anything suboptimal.
3. **Search** — Check `FEEDBACK.md` for prior entries on the same topic.
4. **Scope** — Keep entries to 1–3 lines: category tag, what happened, what should change.
5. **Draft & Ask** — Draft the entry and show it to the user before writing.
6. **Write on Approval** — Append to `FEEDBACK.md`.
7. **Compact at 75** — When `FEEDBACK.md` reaches 75 entries, draft a summary of the oldest 25 into a single "Batch N summary" entry. Ask the user before deleting or rewriting the originals; if unattended, append the summary and leave originals intact.
