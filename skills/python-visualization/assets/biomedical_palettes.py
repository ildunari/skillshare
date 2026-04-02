"""Biomedical color palettes for common visualization needs.

Provides named palettes for treatment groups, organ biodistribution,
assay readouts, and general biomedical use. All palettes are
colorblind-safe or have colorblind-safe alternatives noted.

Usage:
    from biomedical_palettes import TREATMENT, ORGANS, get_palette
    plt.plot(x, y, color=TREATMENT['drug_a'])
    colors = get_palette('treatment', n=4)
"""

# ---------------------------------------------------------------------------
# Okabe-Ito (universal colorblind-safe, 8 colors)
# ---------------------------------------------------------------------------

OKABE_ITO = [
    '#E69F00',  # orange
    '#56B4E9',  # sky blue
    '#009E73',  # green
    '#F0E442',  # yellow
    '#0072B2',  # blue
    '#D55E00',  # vermilion
    '#CC79A7',  # pink
    '#000000',  # black
]


# ---------------------------------------------------------------------------
# Treatment group palettes
# ---------------------------------------------------------------------------

# For 2-4 group comparisons (control vs treatment)
TREATMENT = {
    'control':    '#868686',  # gray
    'vehicle':    '#868686',  # gray (alias)
    'drug_a':     '#0072B2',  # blue
    'drug_b':     '#D55E00',  # vermilion
    'drug_c':     '#009E73',  # green
    'combination':'#CC79A7',  # pink
    'low_dose':   '#56B4E9',  # sky blue
    'mid_dose':   '#0072B2',  # blue
    'high_dose':  '#003F5C',  # dark blue
}

# Sequential dose palettes (light to dark)
DOSE_BLUES = ['#C6DBEF', '#6BAED6', '#2171B5', '#08306B']
DOSE_REDS = ['#FCBBA1', '#FB6A4A', '#CB181D', '#67000D']
DOSE_GREENS = ['#C7E9C0', '#74C476', '#238B45', '#00441B']


# ---------------------------------------------------------------------------
# Organ / tissue palettes
# ---------------------------------------------------------------------------

ORGANS = {
    'liver':    '#8B4513',  # brown
    'spleen':   '#800020',  # burgundy
    'kidney':   '#CD853F',  # tan
    'lung':     '#FFB6C1',  # light pink
    'heart':    '#DC143C',  # crimson
    'brain':    '#DDA0DD',  # plum
    'tumor':    '#2F4F4F',  # dark slate
    'blood':    '#B22222',  # fire brick
    'muscle':   '#D2691E',  # chocolate
    'bone':     '#F5F5DC',  # beige
    'skin':     '#FFDAB9',  # peach
    'intestine':'#DAA520',  # goldenrod
    'stomach':  '#BDB76B',  # dark khaki
    'pancreas': '#EEE8AA',  # pale goldenrod
    'bladder':  '#87CEEB',  # sky blue
}

# Ordered list for bar charts
ORGAN_ORDER = ['liver', 'spleen', 'kidney', 'lung', 'heart', 'brain', 'tumor']
ORGAN_COLORS_ORDERED = [ORGANS[o] for o in ORGAN_ORDER]


# ---------------------------------------------------------------------------
# Assay / readout palettes
# ---------------------------------------------------------------------------

VIABILITY = {
    'viable':   '#2ECC71',  # green
    'apoptotic':'#F39C12',  # amber
    'necrotic': '#E74C3C',  # red
}

CELL_CYCLE = {
    'G0/G1': '#3498DB',  # blue
    'S':     '#2ECC71',  # green
    'G2/M':  '#E74C3C',  # red
    'subG1': '#95A5A6',  # gray
}

STABILITY_ZONES = {
    'highly_stable':    '#C6EFCE',  # light green
    'moderately_stable':'#FFEB9C',  # light yellow
    'unstable':         '#FFC7CE',  # light red
}


# ---------------------------------------------------------------------------
# Significance / p-value markers
# ---------------------------------------------------------------------------

SIGNIFICANCE = {
    'ns':    '#868686',  # gray
    'p05':   '#F0E442',  # yellow (*)
    'p01':   '#E69F00',  # orange (**)
    'p001':  '#D55E00',  # vermilion (***)
}


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def get_palette(name, n=None):
    """Get a color palette by name.

    Parameters
    ----------
    name : str
        Palette name: 'okabe_ito', 'treatment', 'dose_blues', 'dose_reds',
        'dose_greens', 'organs', 'viability', 'cell_cycle'.
    n : int, optional
        Number of colors to return. If None, returns all.

    Returns
    -------
    list of str : hex color codes
    """
    palettes = {
        'okabe_ito': OKABE_ITO,
        'treatment': [TREATMENT['control'], TREATMENT['drug_a'],
                      TREATMENT['drug_b'], TREATMENT['drug_c'],
                      TREATMENT['combination']],
        'dose_blues': DOSE_BLUES,
        'dose_reds': DOSE_REDS,
        'dose_greens': DOSE_GREENS,
        'organs': ORGAN_COLORS_ORDERED,
        'viability': list(VIABILITY.values()),
        'cell_cycle': list(CELL_CYCLE.values()),
    }
    if name not in palettes:
        raise ValueError(f"Unknown palette: {name}. "
                         f"Available: {list(palettes.keys())}")
    colors = palettes[name]
    if n is not None:
        colors = colors[:n]
    return colors


def preview_palette(name='okabe_ito'):
    """Display a palette as a horizontal color bar (matplotlib)."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    colors = get_palette(name)
    fig, ax = plt.subplots(figsize=(len(colors) * 1.2, 1))
    for i, c in enumerate(colors):
        ax.add_patch(mpatches.Rectangle((i, 0), 1, 1, color=c))
        ax.text(i + 0.5, -0.15, c, ha='center', va='top', fontsize=7)
    ax.set_xlim(0, len(colors))
    ax.set_ylim(-0.3, 1)
    ax.set_title(name, fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    return fig
