# LaTeX Figure Integration

Matching matplotlib figures to LaTeX documents: font matching, exact sizing, PGF backend, and journal column widths.


## Contents

- [Why This Matters](#why-this-matters)
- [The Core Recipe](#the-core-recipe)
- [Journal Column Widths](#journal-column-widths)
- [Font Matching](#font-matching)
- [PGF Backend](#pgf-backend)
- [Subfigure Export](#subfigure-export)
- [mplstyle Files](#mplstyle-files)
- [Common Gotchas](#common-gotchas)

## Why This Matters

When you `\includegraphics[width=\columnwidth]{figure.pdf}` in LaTeX, the figure is **scaled**. Scaling changes font sizes, line widths, and proportions — your carefully-crafted 10pt labels become 7pt or 14pt. The fix: create figures at the exact final dimensions so no scaling occurs.

## The Core Recipe

1. Get the exact column width from your LaTeX document
2. Create the figure at that exact size in matplotlib
3. Enable LaTeX text rendering (optional but recommended)
4. Match fonts to your document
5. Save as PDF or PGF

```python
import matplotlib.pyplot as plt
import numpy as np

# 1. Column width (Nature single column = 89mm = 3.504in)
fig_width = 3.504  # inches
fig_height = fig_width * 0.618  # golden ratio

# 2-4. Configure matplotlib
plt.rcParams.update({
    'figure.figsize': (fig_width, fig_height),
    'font.size': 8,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica'],
    'axes.labelsize': 9,
    'axes.titlesize': 9,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'axes.linewidth': 0.5,
    'lines.linewidth': 1.0,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.format': 'pdf',
})

# Optional: enable LaTeX rendering (requires LaTeX installed)
# plt.rcParams.update({
#     'text.usetex': True,
#     'text.latex.preamble': r'\usepackage{amsmath}\usepackage{amssymb}',
# })

# Plot
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label=r'$\sin(x)$')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude (mV)')
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 5. Save
fig.savefig('figure1.pdf')
```

## Journal Column Widths

| Journal | Single column | 1.5 column | Double column |
|---|---|---|---|
| Nature | 89mm / 3.504in | — | 183mm / 7.205in |
| Science | 85mm / 3.346in | — | 175mm / 6.890in |
| Cell | 85mm / 3.346in | 114mm / 4.488in | 174mm / 6.850in |
| PNAS | 87mm / 3.425in | 114mm / 4.488in | 178mm / 7.008in |
| ACS journals | 84mm / 3.307in | — | 175mm / 6.890in |
| PLOS ONE | 83mm / 3.268in | — | 173mm / 6.811in |
| Elsevier (general) | 90mm / 3.543in | 140mm / 5.512in | 190mm / 7.480in |
| RSC journals | 84mm / 3.307in | — | 171mm / 6.732in |
| Wiley (general) | 84mm / 3.307in | — | 174mm / 6.850in |

### Width from LaTeX document

If not in the table above, get the exact width from your `.tex` file:

```latex
% Add to your document temporarily:
\the\columnwidth   % prints column width in points
\the\textwidth     % prints text width in points
```

Then convert: `width_inches = width_points / 72.27`

### Width calculator

```python
def journal_figsize(journal='nature', columns=1, aspect=0.618):
    """Get figure dimensions for a journal.

    Parameters
    ----------
    journal : str
        Journal name (nature, science, cell, pnas, acs, plos, elsevier, rsc, wiley)
    columns : float
        1 for single column, 1.5 for 1.5-column, 2 for double column.
    aspect : float
        Height/width ratio. Default 0.618 (golden ratio).

    Returns
    -------
    tuple : (width_inches, height_inches)
    """
    widths_mm = {
        'nature':   {1: 89, 2: 183},
        'science':  {1: 85, 2: 175},
        'cell':     {1: 85, 1.5: 114, 2: 174},
        'pnas':     {1: 87, 1.5: 114, 2: 178},
        'acs':      {1: 84, 2: 175},
        'plos':     {1: 83, 2: 173},
        'elsevier': {1: 90, 1.5: 140, 2: 190},
        'rsc':      {1: 84, 2: 171},
        'wiley':    {1: 84, 2: 174},
    }
    w_mm = widths_mm[journal.lower()][columns]
    w_in = w_mm / 25.4
    return (w_in, w_in * aspect)
```

## Font Matching

### Without LaTeX (mathtext — always available)

Matplotlib's built-in `mathtext` renders math without requiring a LaTeX installation. Match fonts by family:

```python
# Arial / Helvetica (Nature, many bio journals)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'mathtext.fontset': 'dejavusans',  # or 'stixsans'
})

# Times New Roman (traditional journals)
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
})

# Computer Modern (LaTeX default look, no LaTeX needed)
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['cmr10'],
    'mathtext.fontset': 'cm',
})
```

### With LaTeX (text.usetex — requires LaTeX installed)

Produces pixel-perfect LaTeX text. Slower, but matches your document exactly.

```python
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computer Modern'],
    'text.latex.preamble': r'\usepackage{amsmath}\usepackage{amssymb}',
})
```

**Common font packages:**

| Font | LaTeX package | rcParams |
|---|---|---|
| Computer Modern (default) | (none needed) | `font.serif: Computer Modern` |
| Times | `\usepackage{mathptmx}` | `font.serif: Times` |
| Palatino | `\usepackage{mathpazo}` | `font.serif: Palatino` |
| Helvetica | `\usepackage{helvet}` | `font.sans-serif: Helvetica` |
| Latin Modern | `\usepackage{lmodern}` | `font.family: lmodern` |

```python
# Example: Times in LaTeX
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Times'],
    'text.latex.preamble': r'\usepackage{mathptmx}\usepackage{amsmath}',
})
```

## PGF Backend

The PGF backend outputs `.pgf` files that LaTeX compiles natively. Text is rendered by your document's LaTeX engine, guaranteeing perfect font matching.

```python
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'pgf.preamble': '\n'.join([
        r'\usepackage[utf8x]{inputenc}',
        r'\usepackage[T1]{fontenc}',
        r'\usepackage{amsmath}',
    ]),
    'font.family': 'serif',
    'font.size': 8,
})

fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_xlabel(r'$x$ (units)')
ax.set_ylabel(r'$x^2$')
fig.savefig('figure.pgf')  # include in LaTeX with \input{figure.pgf}
```

**In LaTeX:**
```latex
\begin{figure}[htbp]
  \centering
  \input{figure.pgf}
  \caption{My figure with perfectly matched fonts.}
\end{figure}
```

**PGF gotcha:** If the PGF file references external images (e.g., from `imshow`), the paths are relative to where `pdflatex` runs, not where the `.pgf` file is. You may need to manually edit paths in the `.pgf` file.

## Subfigure Export

### Batch export panels as separate PDFs

```python
def export_panels(fig_funcs, basename, journal='nature', columns=1):
    """Export multiple panels as separate PDFs for LaTeX subfigure.

    Parameters
    ----------
    fig_funcs : list of callables
        Each function takes (fig, ax) and draws one panel.
    basename : str
        Base filename (panels saved as basename_a.pdf, basename_b.pdf, etc.)
    """
    w, h = journal_figsize(journal, columns)
    panel_w = w / len(fig_funcs)

    for i, func in enumerate(fig_funcs):
        letter = chr(ord('a') + i)
        fig, ax = plt.subplots(figsize=(panel_w, h))
        func(fig, ax)
        fig.savefig(f'{basename}_{letter}.pdf', bbox_inches='tight')
        plt.close(fig)
```

**In LaTeX:**
```latex
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{figure1_a.pdf}
    \caption{Panel A description}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{figure1_b.pdf}
    \caption{Panel B description}
  \end{subfigure}
  \caption{Overall figure caption.}
\end{figure}
```

Use `\usepackage{subcaption}` (modern) — avoid the deprecated `subfigure` package.

## mplstyle Files

### Creating a reusable style file

Save as `assets/latex.mplstyle`:

```ini
# LaTeX-compatible publication defaults
text.usetex: True
text.latex.preamble: \usepackage{amsmath}\usepackage{amssymb}
font.family: serif
font.serif: Computer Modern
font.size: 8
axes.labelsize: 9
axes.titlesize: 9
xtick.labelsize: 7
ytick.labelsize: 7
legend.fontsize: 7
axes.linewidth: 0.5
xtick.major.width: 0.5
ytick.major.width: 0.5
xtick.direction: in
ytick.direction: in
lines.linewidth: 1.0
lines.markersize: 4
savefig.dpi: 300
savefig.bbox: tight
savefig.format: pdf
figure.figsize: 3.504, 2.165
image.cmap: viridis
```

**Use:**
```python
plt.style.use('assets/latex.mplstyle')
```

**Combine styles:**
```python
plt.style.use(['assets/latex.mplstyle', 'seaborn-v0_8-whitegrid'])
```

## Common Gotchas

1. **`text.usetex: True` requires LaTeX installed.** In environments without LaTeX (including Claude's container), use `mathtext` instead. Set `mathtext.fontset` to match your target font.

2. **Special characters need raw strings:**
   ```python
   ax.set_xlabel(r'Concentration ($\mu$g/mL)')  # correct
   ax.set_xlabel('Concentration (μg/mL)')         # fails with usetex
   ```

3. **Display math `$$ $$` is not supported.** Use `\displaystyle`:
   ```python
   ax.set_title(r'$\displaystyle\sum_{i=1}^{n} x_i$')
   ```

4. **Font not found:** If LaTeX can't find a font package, you get cryptic errors. Verify with `kpsewhich mathptmx.sty` (should return a path).

5. **PGF + images:** `imshow` in PGF mode creates external PNG files. Paths in the `.pgf` file must be correct relative to where `pdflatex` compiles.

6. **Fallback strategy:** Always develop with `text.usetex: False` first, then enable for final export. This avoids waiting for LaTeX rendering during iteration.