"""Plotly starter templates and export helpers.

Usage:
    from plotly_template import quick_scatter, quick_bar, quick_line, save_plotly
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def quick_scatter(df, x, y, color=None, size=None, hover_name=None,
                  title=None, log_x=False, log_y=False, trendline=None,
                  template='simple_white', **kwargs):
    """Quick scatter plot with sensible defaults.

    Parameters
    ----------
    df : pd.DataFrame
    x, y : str
        Column names for axes.
    color : str, optional
        Column for color encoding.
    size : str, optional
        Column for size encoding.
    hover_name : str, optional
        Column for bold hover label.
    title : str, optional
    log_x, log_y : bool
    trendline : str, optional
        'ols', 'lowess', or None.
    template : str
        Plotly template name.

    Returns
    -------
    go.Figure
    """
    fig = px.scatter(df, x=x, y=y, color=color, size=size,
                     hover_name=hover_name, title=title,
                     log_x=log_x, log_y=log_y, trendline=trendline,
                     template=template, **kwargs)
    fig.update_layout(margin=dict(l=50, r=20, t=50, b=50))
    return fig


def quick_line(df, x, y, color=None, markers=True, title=None,
               template='simple_white', **kwargs):
    """Quick line plot with sensible defaults."""
    fig = px.line(df, x=x, y=y, color=color, markers=markers,
                  title=title, template=template, **kwargs)
    fig.update_layout(margin=dict(l=50, r=20, t=50, b=50))
    return fig


def quick_bar(df, x, y, color=None, barmode='group', text_auto=True,
              title=None, template='simple_white', **kwargs):
    """Quick bar chart with sensible defaults."""
    fig = px.bar(df, x=x, y=y, color=color, barmode=barmode,
                 text_auto=text_auto, title=title, template=template,
                 **kwargs)
    fig.update_layout(margin=dict(l=50, r=20, t=50, b=50))
    return fig


def quick_heatmap(df, title=None, color_continuous_scale='Viridis',
                  text_auto='.2f', template='simple_white'):
    """Quick heatmap from DataFrame (e.g., correlation matrix)."""
    fig = px.imshow(df, text_auto=text_auto, title=title,
                    color_continuous_scale=color_continuous_scale,
                    template=template, aspect='auto')
    fig.update_layout(margin=dict(l=50, r=20, t=50, b=50))
    return fig


def publication_layout(fig, font_family='Arial', font_size=11,
                       width=600, height=400):
    """Apply clean publication-style layout to any Plotly figure.

    Parameters
    ----------
    fig : go.Figure
    font_family : str
    font_size : int
    width, height : int
        Figure dimensions in pixels.

    Returns
    -------
    go.Figure (modified in place and returned)
    """
    fig.update_layout(
        template='simple_white',
        font=dict(family=font_family, size=font_size, color='black'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=width,
        height=height,
        margin=dict(l=60, r=20, t=40, b=60),
        legend=dict(bordercolor='gray', borderwidth=0.5,
                    bgcolor='rgba(255,255,255,0.9)'),
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig


def save_plotly(fig, basename, formats=None, dpi=300, width_in=7, height_in=5):
    """Save Plotly figure in multiple formats.

    Parameters
    ----------
    fig : go.Figure
    basename : str
        Filename without extension.
    formats : list of str
        Formats to save: 'html', 'png', 'pdf', 'svg', 'json'.
        Default: ['html', 'png', 'pdf'].
    dpi : int
        Resolution for raster formats.
    width_in, height_in : float
        Figure dimensions in inches.
    """
    if formats is None:
        formats = ['html', 'png', 'pdf']

    w_px = int(width_in * dpi)
    h_px = int(height_in * dpi)

    for fmt in formats:
        path = f'{basename}.{fmt}'
        if fmt == 'html':
            fig.write_html(path, include_plotlyjs='cdn')
        elif fmt == 'json':
            fig.write_json(path)
        elif fmt in ('png', 'webp', 'jpeg'):
            fig.write_image(path, width=w_px, height=h_px)
        elif fmt in ('svg', 'pdf'):
            fig.write_image(path, width=int(width_in * 72),
                            height=int(height_in * 72))
        print(f'Saved: {path}')


def dashboard_2x2(traces, titles, shared_xaxes=False, shared_yaxes=False,
                   height=600, width=800):
    """Create a 2x2 subplot dashboard.

    Parameters
    ----------
    traces : list of go.BaseTraceType
        Four traces, one per subplot.
    titles : list of str
        Four subplot titles.

    Returns
    -------
    go.Figure
    """
    fig = make_subplots(rows=2, cols=2, subplot_titles=titles,
                        shared_xaxes=shared_xaxes, shared_yaxes=shared_yaxes,
                        vertical_spacing=0.12, horizontal_spacing=0.1)
    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for trace, (r, c) in zip(traces, positions):
        fig.add_trace(trace, row=r, col=c)
    fig.update_layout(height=height, width=width, template='simple_white')
    return fig
