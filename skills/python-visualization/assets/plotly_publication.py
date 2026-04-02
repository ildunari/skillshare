"""Plotly publication-quality template.

Provides a clean, minimal Plotly template that matches common publication
aesthetics. Use as a starting point for figures that may be exported as
static images for journal submission.

Usage:
    import plotly.io as pio
    from plotly_publication import publication_template, apply_publication_style

    # Register and set as default
    pio.templates['publication'] = publication_template()
    pio.templates.default = 'publication'

    # Or apply to a single figure
    fig = apply_publication_style(fig)
"""

import plotly.graph_objects as go
import plotly.io as pio


# Okabe-Ito colorblind-safe palette
OKABE_ITO = [
    '#0072B2',  # blue
    '#D55E00',  # vermilion
    '#009E73',  # green
    '#CC79A7',  # pink
    '#E69F00',  # orange
    '#56B4E9',  # sky blue
    '#F0E442',  # yellow
    '#000000',  # black
]

# Muted publication palette (alternative)
MUTED = [
    '#4878CF',  # blue
    '#D65F5F',  # red
    '#6ACC65',  # green
    '#B47CC7',  # purple
    '#C4AD66',  # olive
    '#77BEDB',  # cyan
    '#D4A6C8',  # pink
    '#8C8C8C',  # gray
]


def publication_template(font_family='Arial, Helvetica, sans-serif',
                          font_size=11, palette='okabe_ito'):
    """Create a publication-quality Plotly template.

    Parameters
    ----------
    font_family : str
        Font stack for all text.
    font_size : int
        Base font size.
    palette : str
        Color palette: 'okabe_ito' or 'muted'.

    Returns
    -------
    plotly.graph_objects.layout.Template
    """
    colors = OKABE_ITO if palette == 'okabe_ito' else MUTED

    template = go.layout.Template()
    template.layout = go.Layout(
        font=dict(family=font_family, size=font_size, color='black'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=55, r=15, t=40, b=55),
        xaxis=dict(
            showline=True, linewidth=1, linecolor='black', mirror=True,
            showgrid=False, zeroline=False, ticks='inside',
            title_font=dict(size=font_size + 1),
            tickfont=dict(size=font_size - 1),
        ),
        yaxis=dict(
            showline=True, linewidth=1, linecolor='black', mirror=True,
            showgrid=False, zeroline=False, ticks='inside',
            title_font=dict(size=font_size + 1),
            tickfont=dict(size=font_size - 1),
        ),
        legend=dict(
            bordercolor='gray', borderwidth=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            font=dict(size=font_size - 1),
        ),
        colorway=colors,
    )

    # Default trace styling
    template.data.scatter = [go.Scatter(
        line=dict(width=1.5),
        marker=dict(size=6, line=dict(width=0.5, color='white')),
    )]
    template.data.bar = [go.Bar(
        marker=dict(line=dict(width=0.5, color='white')),
    )]

    return template


def apply_publication_style(fig, font_family='Arial, Helvetica, sans-serif',
                             font_size=11):
    """Apply publication styling to an existing figure.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
    font_family : str
    font_size : int

    Returns
    -------
    plotly.graph_objects.Figure (modified in place)
    """
    fig.update_layout(
        template='simple_white',
        font=dict(family=font_family, size=font_size, color='black'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=55, r=15, t=40, b=55),
    )
    fig.update_xaxes(
        showline=True, linewidth=1, linecolor='black', mirror=True,
        showgrid=False, ticks='inside',
    )
    fig.update_yaxes(
        showline=True, linewidth=1, linecolor='black', mirror=True,
        showgrid=False, ticks='inside',
    )
    return fig


def register_template(name='publication', **kwargs):
    """Register the publication template with Plotly and set as default.

    Usage:
        register_template()
        fig = px.scatter(df, x='x', y='y')  # automatically uses pub style
    """
    pio.templates[name] = publication_template(**kwargs)
    pio.templates.default = name
    print(f"Registered Plotly template '{name}' as default.")
