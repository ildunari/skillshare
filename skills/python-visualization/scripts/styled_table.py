"""Pandas Styler presets for common table patterns.

Usage:
    from styled_table import style_summary, style_correlation, style_comparison,
                             style_lab_results, save_styled_table
"""

import pandas as pd
import numpy as np


def style_summary(df, precision=2, caption=None):
    """Style a descriptive statistics table (from df.describe()).

    Highlights max in green, min in red. Adds gradient to mean column.

    Parameters
    ----------
    df : pd.DataFrame
        Output of df.describe() or df.describe().T
    precision : int
    caption : str, optional

    Returns
    -------
    pd.io.formats.style.Styler
    """
    styled = (df.style
        .format(precision=precision)
        .highlight_max(color='#c6efce', axis=0)
        .highlight_min(color='#ffc7ce', axis=0))

    if 'mean' in df.columns:
        styled = styled.background_gradient(subset=['mean'], cmap='Blues')
    if 'std' in df.columns:
        styled = styled.background_gradient(subset=['std'], cmap='Oranges')
    if 'count' in df.columns:
        styled = styled.bar(subset=['count'], color='lightblue', width=70)

    if caption:
        styled = styled.set_caption(caption)

    return styled


def style_correlation(df, precision=3, caption=None, cmap='coolwarm',
                      mask_diagonal=True):
    """Style a correlation matrix with diverging colormap.

    Parameters
    ----------
    df : pd.DataFrame
        Correlation matrix (e.g., from df.corr()).
    precision : int
    caption : str, optional
    cmap : str
        Diverging colormap.
    mask_diagonal : bool
        If True, make diagonal cells bold.

    Returns
    -------
    pd.io.formats.style.Styler
    """
    styled = (df.style
        .format(precision=precision)
        .background_gradient(cmap=cmap, vmin=-1, vmax=1))

    if mask_diagonal:
        def bold_diagonal(val, col_name, index_name):
            if col_name == index_name:
                return 'font-weight: bold; background-color: #f0f0f0'
            return ''
        for col in df.columns:
            styled = styled.map(
                lambda v, c=col: 'font-weight: bold; background-color: #f0f0f0'
                if v == 1.0 else '',
                subset=[col])

    if caption:
        styled = styled.set_caption(caption)

    return styled


def style_comparison(df, before_col, after_col, precision=2, caption=None):
    """Style a before/after comparison table.

    Green = improvement (after > before), Red = decline.

    Parameters
    ----------
    df : pd.DataFrame
    before_col, after_col : str
        Column names for before and after values.
    precision : int
    caption : str, optional

    Returns
    -------
    pd.io.formats.style.Styler
    """
    def highlight_change(row):
        styles = [''] * len(row)
        before_idx = row.index.get_loc(before_col)
        after_idx = row.index.get_loc(after_col)
        if row[after_col] > row[before_col]:
            styles[after_idx] = 'background-color: #c6efce; color: #006100'
        elif row[after_col] < row[before_col]:
            styles[after_idx] = 'background-color: #ffc7ce; color: #9c0006'
        return styles

    styled = (df.style
        .format(precision=precision)
        .apply(highlight_change, axis=1))

    if caption:
        styled = styled.set_caption(caption)

    return styled


def style_lab_results(df, thresholds, precision=2, caption=None):
    """Style lab results with out-of-range highlighting.

    Parameters
    ----------
    df : pd.DataFrame
    thresholds : dict
        Column name -> (low, high) tuple. Values outside range are flagged.
        Example: {'pH': (6.8, 7.4), 'temp': (20, 25)}
    precision : int
    caption : str, optional

    Returns
    -------
    pd.io.formats.style.Styler
    """
    def flag_out_of_range(val, low, high):
        if pd.isna(val):
            return ''
        try:
            if val < low or val > high:
                return 'background-color: #ffc7ce; font-weight: bold; color: #9c0006'
            return 'background-color: #c6efce'
        except TypeError:
            return ''

    styled = df.style.format(precision=precision)

    for col, (low, high) in thresholds.items():
        if col in df.columns:
            styled = styled.map(
                lambda v, lo=low, hi=high: flag_out_of_range(v, lo, hi),
                subset=[col])

    if caption:
        styled = styled.set_caption(caption)

    return styled


def style_ranking(df, value_col, precision=2, caption=None, ascending=False,
                  top_n=3, bottom_n=3):
    """Style a ranking table with top/bottom highlighting.

    Parameters
    ----------
    df : pd.DataFrame
    value_col : str
        Column to rank by.
    ascending : bool
        If True, lower is better.
    top_n : int
        Number of top entries to highlight green.
    bottom_n : int
        Number of bottom entries to highlight red.

    Returns
    -------
    pd.io.formats.style.Styler
    """
    sorted_df = df.sort_values(value_col, ascending=ascending).copy()
    sorted_df['_rank'] = range(1, len(sorted_df) + 1)

    def color_rank(row):
        styles = [''] * len(row)
        rank = row['_rank']
        val_idx = row.index.get_loc(value_col)
        if rank <= top_n:
            styles[val_idx] = 'background-color: #c6efce; font-weight: bold'
        elif rank > len(sorted_df) - bottom_n:
            styles[val_idx] = 'background-color: #ffc7ce'
        return styles

    styled = (sorted_df.style
        .format(precision=precision)
        .apply(color_rank, axis=1)
        .bar(subset=[value_col], color='steelblue', width=60)
        .hide(subset=['_rank'], axis=1))

    if caption:
        styled = styled.set_caption(caption)

    return styled


def save_styled_table(styled, filename, title=None):
    """Save a styled DataFrame to HTML file.

    Parameters
    ----------
    styled : pd.io.formats.style.Styler
    filename : str
        Output path (.html).
    title : str, optional
        Page title for HTML.
    """
    html = styled.to_html()

    if title:
        full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 1000px; margin: auto; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ padding: 6px 10px; border: 1px solid #ddd; text-align: right; }}
  th {{ background-color: #f5f5f5; font-weight: bold; text-align: center; }}
  caption {{ font-style: italic; margin-bottom: 8px; text-align: left; }}
</style>
</head>
<body>
{html}
</body>
</html>"""
    else:
        full_html = html

    with open(filename, 'w') as f:
        f.write(full_html)
    print(f'Saved: {filename}')


def styled_to_latex(styled, filename, caption=None, label=None):
    """Export styled DataFrame to LaTeX.

    Parameters
    ----------
    styled : pd.io.formats.style.Styler
    filename : str
        Output path (.tex).
    caption : str, optional
    label : str, optional
        LaTeX label (e.g., 'tab:results').
    """
    latex = styled.to_latex(
        caption=caption,
        label=label,
        position='htbp',
        position_float='centering',
        hrules=True,
    )
    with open(filename, 'w') as f:
        f.write(latex)
    print(f'Saved: {filename}')
