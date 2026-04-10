# Plotly API Reference

Quick reference for Plotly's Python graphing library. Covers Plotly Express (high-level) and Graph Objects (low-level).

## When to Use Which

| Need | Use | Why |
|---|---|---|
| Quick exploration, standard chart types | Plotly Express (`px`) | One-liner charts, automatic legends/colors |
| Full customization, multi-trace, complex layouts | Graph Objects (`go`) | Direct control over every element |
| Start fast, customize later | `px` then modify | `px` returns a `go.Figure` — fully customizable |

**Key insight:** Plotly Express always returns a `go.Figure`. You can start with `px` and drop down to `go` methods for fine-tuning. Never rewrite from scratch.

## Installation

```python
pip install plotly kaleido  # kaleido for static image export
```

Current stable: plotly 6.x (as of 2025). Breaking changes from 5.x are minor.

## Plotly Express (px)

### Common chart functions

**Relational:**
- `px.scatter(df, x, y, color, size, symbol, facet_row, facet_col, hover_name, hover_data, trendline)`
- `px.line(df, x, y, color, line_dash, markers, facet_row, facet_col)`
- `px.area(df, x, y, color, line_group)`

**Distributions:**
- `px.histogram(df, x, y, color, nbins, marginal, histnorm, barmode)`
- `px.box(df, x, y, color, notched, points)`
- `px.violin(df, x, y, color, box, points)`
- `px.strip(df, x, y, color)`
- `px.ecdf(df, x, color, marginal)`

**Categorical:**
- `px.bar(df, x, y, color, barmode, text_auto, orientation)`
- `px.funnel(df, x, y, color)`

**Matrix:**
- `px.imshow(data, color_continuous_scale, aspect, text_auto)` — heatmaps, image data
- `px.density_heatmap(df, x, y, marginal_x, marginal_y, nbinsx, nbinsy)`

**3D:**
- `px.scatter_3d(df, x, y, z, color, size, symbol)`
- `px.line_3d(df, x, y, z, color)`
- `px.surface(z=array)` — not in px, use `go.Surface`

**Statistical:**
- `px.scatter_matrix(df, dimensions, color)` — pair plot
- `px.parallel_coordinates(df, dimensions, color)`
- `px.parallel_categories(df, dimensions, color)`
- `px.density_contour(df, x, y, color, marginal_x, marginal_y)`

**Specialized:**
- `px.treemap(df, path, values, color)`
- `px.sunburst(df, path, values, color)`
- `px.pie(df, values, names, hole)` — hole > 0 for donut
- `px.polar(df, r, theta)` — not common, use `go.Scatterpolar`

### Key shared parameters

| Parameter | Purpose | Example |
|---|---|---|
| `color` | Map column to color | `color='species'` |
| `size` | Map column to marker size | `size='population'` |
| `symbol` | Map column to marker shape | `symbol='continent'` |
| `facet_row` / `facet_col` | Small multiples by column | `facet_col='year'` |
| `facet_col_wrap` | Max columns before wrapping | `facet_col_wrap=3` |
| `hover_name` | Bold label on hover | `hover_name='country'` |
| `hover_data` | Extra columns in hover | `hover_data=['gdp', 'pop']` |
| `animation_frame` | Animate over column | `animation_frame='year'` |
| `animation_group` | Track identity across frames | `animation_group='country'` |
| `trendline` | Add regression line | `trendline='ols'` or `'lowess'` |
| `marginal` / `marginal_x` / `marginal_y` | Distribution on margins | `marginal='box'`, `'violin'`, `'histogram'`, `'rug'` |
| `log_x` / `log_y` | Log scale axes | `log_x=True` |
| `color_continuous_scale` | Continuous colormap | `color_continuous_scale='Viridis'` |
| `color_discrete_sequence` | Discrete color list | `color_discrete_sequence=px.colors.qualitative.Set2` |
| `template` | Visual theme | `template='plotly_white'`, `'simple_white'`, `'presentation'` |
| `title` | Chart title | `title='My Chart'` |
| `labels` | Rename axes/legend entries | `labels={'x_col': 'X Label'}` |
| `category_orders` | Force category order | `category_orders={'day': ['Mon','Tue']}` |

### Built-in templates

```python
import plotly.io as pio
# Available: plotly, plotly_white, plotly_dark, ggplot2, seaborn,
#            simple_white, presentation, xgridoff, ygridoff, gridon, none
pio.templates.default = 'plotly_white'  # set globally
```

`simple_white` is closest to publication style. `presentation` has larger fonts.

## Graph Objects (go)

### Figure construction

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Series A'))
fig.add_trace(go.Bar(x=categories, y=values, name='Series B'))
fig.update_layout(title='My Figure', xaxis_title='X', yaxis_title='Y')
fig.show()
```

### Common trace types

| Trace | Usage |
|---|---|
| `go.Scatter` | Lines, markers, or both. Set `mode='lines'`, `'markers'`, `'lines+markers'`, `'text'` |
| `go.Bar` | Vertical/horizontal bars |
| `go.Heatmap` | z matrix, colorscale, optional text |
| `go.Contour` | Contour from z matrix |
| `go.Histogram` | Distribution histogram |
| `go.Box` | Box plot |
| `go.Violin` | Violin plot |
| `go.Surface` | 3D surface from z matrix |
| `go.Scatter3d` | 3D scatter/line |
| `go.Mesh3d` | 3D mesh from vertices |
| `go.Scatterpolar` | Polar/radar charts |
| `go.Indicator` | KPI gauges and numbers |
| `go.Sankey` | Sankey/flow diagrams |
| `go.Table` | Data tables in figure |

### Scatter trace key parameters

```python
go.Scatter(
    x=x, y=y,
    mode='lines+markers',       # 'lines', 'markers', 'text', combinations
    name='Series A',            # legend label
    text=labels,                # text labels or hover text
    hovertemplate='%{x:.2f}, %{y:.2f}<extra></extra>',
    marker=dict(
        size=10, color=values, colorscale='Viridis',
        colorbar=dict(title='Value'), symbol='circle',
        line=dict(width=1, color='black')
    ),
    line=dict(width=2, dash='dash'),  # 'solid', 'dot', 'dash', 'dashdot'
    fill='tozeroy',             # area fill: 'tozeroy', 'tonexty', 'toself'
    opacity=0.8,
    error_y=dict(type='data', array=errors, visible=True),
)
```

### Layout configuration

```python
fig.update_layout(
    title=dict(text='Title', x=0.5, font=dict(size=18)),
    xaxis=dict(title='X Axis', type='log', range=[0, 10], dtick=1,
               showgrid=True, gridcolor='lightgray', zeroline=False),
    yaxis=dict(title='Y Axis', tickformat='.2f'),
    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)',
                bordercolor='gray', borderwidth=1),
    font=dict(family='Arial', size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=20, t=60, b=60),
    width=800, height=500,
    hovermode='x unified',     # 'x', 'y', 'closest', 'x unified', False
    template='simple_white',
)
```

### Subplots

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=['Plot A', 'Plot B', 'Plot C', 'Plot D'],
    shared_xaxes=True,
    vertical_spacing=0.1,
    horizontal_spacing=0.08,
    specs=[[{"secondary_y": True}, {}],   # secondary y-axis on top-left
           [{}, {"type": "polar"}]],       # polar chart in bottom-right
)
fig.add_trace(go.Scatter(x=x, y=y), row=1, col=1)
fig.add_trace(go.Bar(x=x, y=y2), row=1, col=1, secondary_y=True)
fig.update_layout(height=600)
```

### Annotations and shapes

```python
fig.add_annotation(x=3, y=5, text="Important point",
                   showarrow=True, arrowhead=2, ax=40, ay=-30)
fig.add_hline(y=threshold, line_dash='dash', line_color='red',
              annotation_text='Threshold')
fig.add_vrect(x0=2, x1=4, fillcolor='lightblue', opacity=0.3,
              line_width=0, annotation_text='Region of interest')
fig.add_shape(type='circle', x0=1, y0=1, x1=3, y1=3,
              line=dict(color='red', dash='dot'))
```

## Color Scales

**Continuous:** `Viridis`, `Plasma`, `Inferno`, `Magma`, `Cividis` (colorblind-safe), `Blues`, `Reds`, `RdBu` (diverging), `Turbo`

**Discrete (qualitative):**
```python
px.colors.qualitative.Set2      # 8 colors, good default
px.colors.qualitative.Plotly     # 10 colors, Plotly default
px.colors.qualitative.D3         # 10 colors, D3 default
px.colors.qualitative.Safe       # 11 colors, colorblind-safe
```

**Custom:**
```python
fig.update_traces(marker_colorscale=[[0, 'blue'], [0.5, 'white'], [1, 'red']])
```

## Common Gotchas

1. **px returns go.Figure** — never rewrite a px chart as go from scratch. Just call `fig.update_layout()` or `fig.update_traces()`.
2. **Categorical ordering** — Plotly infers order from data. Force it with `category_orders` parameter or `fig.update_xaxes(categoryorder='total ascending')`.
3. **Date axes** — Plotly auto-detects datetime columns. Force with `fig.update_xaxes(type='date')`.
4. **Large datasets** — Plotly renders in browser JS. For >100K points, use `px.scatter` with `render_mode='webgl'` or aggregate first.
5. **Notebook display** — Plotly auto-renders in Jupyter. In scripts, `fig.show()` opens browser. Use `fig.write_html()` for file output.
6. **Template stacking** — Templates are additive: `template='plotly_white+presentation'` combines both.
