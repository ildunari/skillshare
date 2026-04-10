# Plotly Export Reference

Saving Plotly figures as HTML, static images, JSON, and embedding in documents.

## HTML Export (interactive)

### Standalone HTML file

```python
fig.write_html('figure.html')
```

This creates a self-contained HTML file (~3MB) with the Plotly.js library embedded.

### Reduce file size

```python
# Use CDN instead of embedding Plotly.js (~6KB vs ~3MB)
fig.write_html('figure.html', include_plotlyjs='cdn')

# Minimal: no Plotly.js, requires loading separately
fig.write_html('figure.html', include_plotlyjs=False)

# Separate Plotly.js into a directory
fig.write_html('figure.html', include_plotlyjs='directory')
```

### HTML string (for embedding)

```python
html_str = fig.to_html(full_html=False, include_plotlyjs='cdn')
# Returns just the <div> — embed in your own HTML page
```

### Jupyter display control

```python
fig.show()                          # default renderer
fig.show(renderer='browser')        # open in browser
fig.show(renderer='notebook')       # inline in Jupyter
fig.show(renderer='png')            # static PNG inline
fig.show(renderer='svg')            # static SVG inline
```

## Static Image Export

Requires the **Kaleido** engine (replaces deprecated Orca).

### Installation

```bash
pip install kaleido
```

### Save static images

```python
fig.write_image('figure.png')                    # PNG (default)
fig.write_image('figure.pdf')                    # PDF (vector)
fig.write_image('figure.svg')                    # SVG (vector)
fig.write_image('figure.webp')                   # WebP
fig.write_image('figure.jpeg', quality=95)       # JPEG with quality

# Control resolution
fig.write_image('figure.png', scale=2)           # 2x resolution (retina)
fig.write_image('figure.png', width=1200, height=800, scale=3)

# For publication (300 DPI equivalent at typical sizes):
fig.write_image('figure.png', width=2100, height=1400, scale=1)  # ~7" x 4.7" at 300 DPI
fig.write_image('figure.pdf', width=700, height=467)              # vector, scale irrelevant
```

### DPI calculation

Plotly uses pixels, not inches+DPI. To get a specific DPI:

```python
def plotly_dims(width_inches, height_inches, dpi=300):
    """Convert inches + DPI to Plotly pixel dimensions."""
    return dict(width=int(width_inches * dpi), height=int(height_inches * dpi))

# Nature single-column (89mm = 3.5in) at 300 DPI:
fig.write_image('figure.png', **plotly_dims(3.5, 2.5, dpi=300))
```

### Get image as bytes (no file)

```python
img_bytes = fig.to_image(format='png', scale=2)
# Returns bytes object — write to file, embed in PDF, etc.

from PIL import Image
import io
img = Image.open(io.BytesIO(img_bytes))
```

## JSON Serialization

### Save/load figure as JSON

```python
# Save
fig.write_json('figure.json')
import json
with open('figure.json', 'w') as f:
    json.dump(fig.to_dict(), f)

# Load
import plotly.io as pio
fig = pio.read_json('figure.json')
```

### Get as dict/JSON string

```python
fig_dict = fig.to_dict()           # Python dict
fig_json = fig.to_json()           # JSON string
fig_plotlyjs = fig.to_plotly_json() # Plotly.js-compatible JSON
```

Useful for storing figures in databases, sending via API, or programmatic reuse.

## Multi-Format Export Helper

```python
def save_plotly_figure(fig, basename, formats=None, dpi=300, width_in=7, height_in=5):
    """Save Plotly figure in multiple formats.

    Parameters
    ----------
    fig : go.Figure
    basename : str
        Filename without extension.
    formats : list
        List of formats: 'html', 'png', 'pdf', 'svg', 'json'. Default: all.
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
        elif fmt in ('png', 'svg', 'pdf', 'webp', 'jpeg'):
            if fmt in ('svg', 'pdf'):
                fig.write_image(path, width=int(width_in * 72), height=int(height_in * 72))
            else:
                fig.write_image(path, width=w_px, height=h_px)
        print(f'Saved: {path}')
```

## Embedding in LaTeX

For LaTeX documents, export Plotly as PDF (vector) or high-DPI PNG:

```python
# PDF vector export (best for LaTeX)
fig.write_image('figures/fig1.pdf', width=510, height=340)  # Nature double-column in points

# Then in LaTeX:
# \includegraphics[width=\textwidth]{figures/fig1.pdf}
```

**Note:** For pixel-perfect font matching with your LaTeX document, matplotlib with `text.usetex=True` is still superior. Plotly's strength is exploration; export to matplotlib for final publication if font matching matters. See `latex-integration.md`.

## Kaleido Troubleshooting

| Issue | Solution |
|---|---|
| `ValueError: image export requires kaleido` | `pip install kaleido` |
| Blank/corrupted images | Update kaleido: `pip install --upgrade kaleido` |
| Timeout on complex figures | Add `engine='kaleido'` explicitly |
| Wrong fonts in static export | Fonts must be installed on the system; Kaleido uses system fonts |
| Large file sizes for PNG | Reduce `scale` parameter or figure dimensions |
