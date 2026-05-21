"""LaTeX figure integration helpers.

Provides:
- Journal column width lookup and figure sizing
- LaTeX-compatible matplotlib configuration
- Multi-format export with correct dimensions
- Subfigure batch export for LaTeX subcaption
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# ---------------------------------------------------------------------------
# Journal column widths (mm)
# ---------------------------------------------------------------------------

JOURNAL_WIDTHS_MM = {
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


def journal_figsize(journal='nature', columns=1, aspect=0.618):
    """Get figure dimensions for a specific journal.

    Parameters
    ----------
    journal : str
        Journal name. One of: nature, science, cell, pnas, acs, plos,
        elsevier, rsc, wiley.
    columns : float
        1 for single column, 1.5 for 1.5-column, 2 for double column.
    aspect : float
        Height/width ratio. Default 0.618 (golden ratio).

    Returns
    -------
    tuple : (width_inches, height_inches)
    """
    key = journal.lower()
    if key not in JOURNAL_WIDTHS_MM:
        raise ValueError(f"Unknown journal: {journal}. "
                         f"Available: {list(JOURNAL_WIDTHS_MM.keys())}")
    widths = JOURNAL_WIDTHS_MM[key]
    if columns not in widths:
        available = list(widths.keys())
        raise ValueError(f"{journal} doesn't support {columns}-column. "
                         f"Available: {available}")
    w_in = widths[columns] / 25.4
    return (w_in, w_in * aspect)


def pt_to_inches(pt):
    """Convert LaTeX points to inches."""
    return pt / 72.27


# ---------------------------------------------------------------------------
# Matplotlib configuration
# ---------------------------------------------------------------------------

def configure_latex(font='cm', usetex=False, fontsize=8):
    """Configure matplotlib for LaTeX-compatible output.

    Parameters
    ----------
    font : str
        Font preset: 'cm' (Computer Modern), 'times', 'arial', 'palatino'.
    usetex : bool
        Enable LaTeX text rendering. Requires LaTeX installed.
    fontsize : int
        Base font size.
    """
    config = {
        'font.size': fontsize,
        'axes.labelsize': fontsize + 1,
        'axes.titlesize': fontsize + 1,
        'xtick.labelsize': fontsize - 1,
        'ytick.labelsize': fontsize - 1,
        'legend.fontsize': fontsize - 1,
        'axes.linewidth': 0.5,
        'xtick.major.width': 0.5,
        'ytick.major.width': 0.5,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'lines.linewidth': 1.0,
        'lines.markersize': 4,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.format': 'pdf',
    }

    font_presets = {
        'cm': {
            'font.family': 'serif',
            'font.serif': ['cmr10', 'Computer Modern', 'DejaVu Serif'],
            'mathtext.fontset': 'cm',
        },
        'times': {
            'font.family': 'serif',
            'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
            'mathtext.fontset': 'stix',
        },
        'arial': {
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
            'mathtext.fontset': 'dejavusans',
        },
        'palatino': {
            'font.family': 'serif',
            'font.serif': ['Palatino', 'Palatino Linotype', 'DejaVu Serif'],
            'mathtext.fontset': 'stix',
        },
    }

    if font.lower() not in font_presets:
        raise ValueError(f"Unknown font: {font}. "
                         f"Available: {list(font_presets.keys())}")

    config.update(font_presets[font.lower()])

    if usetex:
        preamble_map = {
            'cm': r'',
            'times': r'\usepackage{mathptmx}',
            'arial': r'\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}',
            'palatino': r'\usepackage{mathpazo}',
        }
        config.update({
            'text.usetex': True,
            'text.latex.preamble': (
                r'\usepackage{amsmath}\usepackage{amssymb}'
                + ('\n' + preamble_map.get(font.lower(), '') if preamble_map.get(font.lower()) else '')
            ),
        })

    plt.rcParams.update(config)


def configure_pgf(font='cm', fontsize=8):
    """Configure matplotlib for PGF backend output.

    Must be called before any plt.subplots() or figure creation.
    """
    import matplotlib
    matplotlib.use('pgf')

    preamble_lines = [
        r'\usepackage[utf8x]{inputenc}',
        r'\usepackage[T1]{fontenc}',
        r'\usepackage{amsmath}',
        r'\usepackage{amssymb}',
    ]
    font_packages = {
        'cm': [],
        'times': [r'\usepackage{mathptmx}'],
        'arial': [r'\usepackage{helvet}', r'\renewcommand{\familydefault}{\sfdefault}'],
        'palatino': [r'\usepackage{mathpazo}'],
    }
    preamble_lines.extend(font_packages.get(font.lower(), []))

    plt.rcParams.update({
        'pgf.texsystem': 'pdflatex',
        'pgf.preamble': '\n'.join(preamble_lines),
        'font.family': 'serif' if font.lower() != 'arial' else 'sans-serif',
        'font.size': fontsize,
    })


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------

def save_figure(fig, basename, formats=None, dpi=300):
    """Save figure in multiple publication formats.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    basename : str
        Filename without extension. Can include path.
    formats : list of str
        Formats to save. Default: ['pdf', 'png'].
    dpi : int
        DPI for raster formats.
    """
    if formats is None:
        formats = ['pdf', 'png']

    path = Path(basename)
    path.parent.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        outpath = path.with_suffix(f'.{fmt}')
        fig.savefig(outpath, dpi=dpi, bbox_inches='tight', format=fmt)
        print(f'Saved: {outpath}')


def export_subfigures(panel_funcs, basename, journal='nature', columns=1,
                      aspect=0.618, formats=None, dpi=300):
    """Export multiple panels as separate PDFs for LaTeX subfigure environment.

    Parameters
    ----------
    panel_funcs : list of callables
        Each function signature: func(fig, ax) -> None. Draws one panel.
    basename : str
        Base filename. Panels saved as basename_a.pdf, basename_b.pdf, etc.
    journal : str
    columns : float
    aspect : float
    formats : list of str

    Returns
    -------
    list of str : file paths created
    """
    if formats is None:
        formats = ['pdf']

    total_w, total_h = journal_figsize(journal, columns, aspect)
    n = len(panel_funcs)
    panel_w = total_w / n

    paths = []
    for i, func in enumerate(panel_funcs):
        letter = chr(ord('a') + i)
        fig, ax = plt.subplots(figsize=(panel_w, total_h))
        func(fig, ax)
        panel_base = f'{basename}_{letter}'
        save_figure(fig, panel_base, formats=formats, dpi=dpi)
        plt.close(fig)
        paths.append(panel_base)

    # Print LaTeX snippet
    print('\n% LaTeX snippet (requires \\usepackage{subcaption}):')
    print('\\begin{figure}[htbp]')
    print('  \\centering')
    subfig_width = f'{0.95 / n:.2f}'
    for i in range(n):
        letter = chr(ord('a') + i)
        print(f'  \\begin{{subfigure}}[b]{{{subfig_width}\\textwidth}}')
        print(f'    \\includegraphics[width=\\textwidth]{{{basename}_{letter}}}')
        print(f'    \\caption{{Panel {letter.upper()} description}}')
        print(f'  \\end{{subfigure}}')
        if i < n - 1:
            print('  \\hfill')
    print('  \\caption{Overall figure caption.}')
    print('  \\label{fig:' + Path(basename).stem + '}')
    print('\\end{figure}')

    return paths
