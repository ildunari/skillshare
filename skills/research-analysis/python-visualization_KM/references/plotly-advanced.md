# Plotly Advanced Charts

3D plots, statistical visualizations, faceted layouts, multiple axes, and annotations.

## 3D Plots

### 3D scatter

```python
import plotly.express as px

df = px.data.iris()
fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                    color='species', size='petal_length', opacity=0.8)
fig.update_layout(scene=dict(
    xaxis_title='Sepal Length',
    yaxis_title='Sepal Width',
    zaxis_title='Petal Width',
    camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
))
```

### 3D surface

```python
import plotly.graph_objects as go
import numpy as np

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = go.Figure(data=[go.Surface(
    x=X, y=Y, z=Z,
    colorscale='Viridis',
    contours=dict(z=dict(show=True, usecolormap=True, project_z=True)),
)])
fig.update_layout(
    scene=dict(aspectratio=dict(x=1, y=1, z=0.5)),
    margin=dict(l=0, r=0, t=30, b=0),
)
```

### 3D mesh

```python
fig = go.Figure(data=[go.Mesh3d(
    x=vertices_x, y=vertices_y, z=vertices_z,
    i=faces_i, j=faces_j, k=faces_k,
    intensity=values,
    colorscale='Plasma',
    opacity=0.7,
)])
```

### Scene configuration (applies to all 3D)

```python
fig.update_layout(scene=dict(
    xaxis=dict(title='X', backgroundcolor='white', gridcolor='lightgray'),
    yaxis=dict(title='Y', backgroundcolor='white'),
    zaxis=dict(title='Z', backgroundcolor='white'),
    camera=dict(
        eye=dict(x=1.25, y=1.25, z=1.25),    # camera position
        up=dict(x=0, y=0, z=1),                # which direction is up
        center=dict(x=0, y=0, z=0),            # look-at point
    ),
    aspectmode='cube',  # 'cube', 'auto', 'manual', 'data'
))
```

## Statistical Charts

### Parallel coordinates (multivariate exploration)

```python
fig = px.parallel_coordinates(df,
    dimensions=['dim1', 'dim2', 'dim3', 'dim4'],
    color='target',
    color_continuous_scale='Bluered',
    labels={col: col.replace('_', ' ').title() for col in df.columns},
)
```

### Parallel categories (categorical dimensions)

```python
fig = px.parallel_categories(df,
    dimensions=['category1', 'category2', 'category3'],
    color='score', color_continuous_scale='Blues',
)
```

### Density contour with marginals

```python
fig = px.density_contour(df, x='x', y='y',
    marginal_x='histogram', marginal_y='box',
    color='group',
)
fig.update_traces(contours_coloring='fill')
```

### ECDF (empirical cumulative distribution)

```python
fig = px.ecdf(df, x='value', color='group',
    markers=True, lines=True,
    ecdfnorm='percent',  # 'probability', 'percent', None (count)
)
```

### Ternary plot

```python
fig = px.scatter_ternary(df,
    a='component_a', b='component_b', c='component_c',
    color='category', size='value',
)
```

## Faceted (Small Multiples)

### Row and column facets

```python
fig = px.scatter(df, x='x', y='y',
    facet_col='category',       # columns
    facet_row='group',          # rows
    facet_col_wrap=3,           # max 3 columns, then wrap
    facet_col_spacing=0.05,     # gap between columns
    facet_row_spacing=0.08,     # gap between rows
)

# Update all facet axes:
fig.update_xaxes(matches=None)  # independent x-axes per facet
fig.update_yaxes(matches=None)  # independent y-axes per facet

# Update specific subplot:
fig.update_xaxes(title_text='Custom X', row=1, col=2)
```

### Free-form subplots (mixed types)

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=['A', 'B', 'C', 'D', 'E', 'F'],
    specs=[[{}, {}, {"type": "polar"}],
           [{"colspan": 2}, None, {"type": "scene"}]],
    vertical_spacing=0.12,
)

fig.add_trace(go.Scatter(x=x, y=y), row=1, col=1)
fig.add_trace(go.Bar(x=cats, y=vals), row=1, col=2)
fig.add_trace(go.Scatterpolar(r=r, theta=theta), row=1, col=3)
fig.add_trace(go.Heatmap(z=matrix), row=2, col=1)
fig.add_trace(go.Scatter3d(x=x3, y=y3, z=z3), row=2, col=3)
```

## Multiple Y-Axes

### Secondary y-axis

```python
from plotly.subplots import make_subplots

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=dates, y=temperature, name='Temperature'),
              secondary_y=False)
fig.add_trace(go.Bar(x=dates, y=rainfall, name='Rainfall', opacity=0.5),
              secondary_y=True)

fig.update_yaxes(title_text='Temperature (C)', secondary_y=False)
fig.update_yaxes(title_text='Rainfall (mm)', secondary_y=True)
```

## Annotations and Shapes

### Text annotations

```python
fig.add_annotation(
    x=peak_x, y=peak_y,
    text=f'Peak: {peak_y:.2f}',
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=1.5,
    ax=40, ay=-40,           # arrow offset in pixels
    font=dict(size=12, color='red'),
    bgcolor='white',
    bordercolor='red',
    borderwidth=1,
    borderpad=4,
)
```

### Reference lines

```python
fig.add_hline(y=mean_val, line_dash='dash', line_color='gray',
              annotation_text=f'Mean: {mean_val:.1f}',
              annotation_position='top right')
fig.add_vline(x=cutoff, line_dash='dot', line_color='red')
```

### Shaded regions

```python
fig.add_vrect(x0=start, x1=end,
    fillcolor='lightblue', opacity=0.2,
    line_width=0,
    annotation_text='Treatment period',
    annotation_position='top left',
)
fig.add_hrect(y0=lower, y1=upper,
    fillcolor='lightgreen', opacity=0.15,
    line_width=0,
    annotation_text='Normal range',
)
```

### Shapes (geometric)

```python
fig.add_shape(type='rect', x0=1, y0=2, x1=3, y1=5,
    line=dict(color='red', width=2, dash='dash'),
    fillcolor='rgba(255,0,0,0.1)')

fig.add_shape(type='circle', x0=2, y0=2, x1=4, y1=4,
    line=dict(color='blue'))

fig.add_shape(type='line', x0=0, y0=0, x1=10, y1=10,
    line=dict(color='green', width=1, dash='dot'))
```

## Publication-Quality Plotly

### Clean minimal template

```python
fig.update_layout(
    template='simple_white',
    font=dict(family='Arial', size=11, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=600, height=400,
    margin=dict(l=50, r=20, t=40, b=50),
    legend=dict(
        bordercolor='gray', borderwidth=0.5,
        bgcolor='rgba(255,255,255,0.9)',
    ),
)
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
```

### Export workflow: explore in Plotly, finalize in matplotlib

For journal submission requiring specific formatting:
1. Use Plotly for interactive exploration and data understanding
2. Once you know the final visualization, recreate in matplotlib with publication style
3. Or use `fig.write_image('fig.pdf')` with Kaleido for Plotly direct export (see `plotly-export.md`)
