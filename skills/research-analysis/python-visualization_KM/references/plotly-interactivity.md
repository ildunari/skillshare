# Plotly Interactivity Reference

Interactive features that make Plotly charts dynamic: hover, buttons, dropdowns, sliders, and animations.

## Hover Customization

### hovertemplate (recommended)

Full control over hover tooltip content using format strings.

```python
fig.update_traces(
    hovertemplate=(
        '<b>%{hovertext}</b><br>'
        'X: %{x:.2f}<br>'
        'Y: %{y:.3f}<br>'
        'Size: %{marker.size}<br>'
        '<extra>%{fullData.name}</extra>'  # secondary box (trace name)
    )
)
```

**Format codes:** `%{x}` (raw), `%{x:.2f}` (2 decimals), `%{x:,}` (thousands separator), `%{x|%B %d, %Y}` (date format).

**Special variables:** `%{hovertext}`, `%{text}`, `%{customdata[0]}`, `%{marker.size}`, `%{marker.color}`, `%{fullData.name}`.

### customdata for extra columns

```python
import plotly.express as px
fig = px.scatter(df, x='x', y='y',
    hover_data={'hidden_col': True, 'x': ':.2f'},  # include hidden_col, format x
    custom_data=['extra1', 'extra2'])

# Access in hovertemplate:
fig.update_traces(
    hovertemplate='Extra1: %{customdata[0]}<br>Extra2: %{customdata[1]}'
)
```

### Hover modes

```python
fig.update_layout(
    hovermode='x unified',  # single tooltip for all traces at x position
    # Options: 'x', 'y', 'closest', 'x unified', 'y unified', False
)
```

## Buttons and Dropdowns

Use `updatemenus` in layout to add interactive controls.

### Dropdown to switch data

```python
import plotly.graph_objects as go
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=np.sin(x), name='sin', visible=True))
fig.add_trace(go.Scatter(x=x, y=np.cos(x), name='cos', visible=False))
fig.add_trace(go.Scatter(x=x, y=np.tan(x), name='tan', visible=False))

fig.update_layout(
    updatemenus=[dict(
        type='dropdown',        # 'dropdown' or 'buttons'
        direction='down',
        x=0.1, y=1.15,
        showactive=True,
        buttons=[
            dict(label='sin(x)', method='update',
                 args=[{'visible': [True, False, False]},
                       {'title': 'Sine'}]),
            dict(label='cos(x)', method='update',
                 args=[{'visible': [False, True, False]},
                       {'title': 'Cosine'}]),
            dict(label='tan(x)', method='update',
                 args=[{'visible': [False, False, True]},
                       {'title': 'Tangent', 'yaxis.range': [-5, 5]}]),
        ]
    )]
)
```

### Button methods

| Method | Updates | Use case |
|---|---|---|
| `restyle` | Trace properties only | Change colors, markers, visibility |
| `relayout` | Layout properties only | Change title, axes, annotations |
| `update` | Both trace and layout | Most common — combined updates |
| `animate` | Trigger animation frames | Play/pause animations |

### Toggle buttons (radio-style)

```python
fig.update_layout(
    updatemenus=[dict(
        type='buttons',
        direction='right',
        x=0.5, y=1.12, xanchor='center',
        buttons=[
            dict(label='Linear', method='relayout',
                 args=[{'yaxis.type': 'linear'}]),
            dict(label='Log', method='relayout',
                 args=[{'yaxis.type': 'log'}]),
        ]
    )]
)
```

## Sliders

### Range slider on x-axis

```python
fig.update_xaxes(
    rangeslider_visible=True,
    rangeslider_thickness=0.05,  # fraction of plot height
)
```

### Custom slider for parameter control

```python
import numpy as np
import plotly.graph_objects as go

x = np.linspace(0, 10, 200)
fig = go.Figure()

# Create frames for each frequency
frames = []
slider_steps = []
for freq in np.arange(0.5, 5.0, 0.5):
    frames.append(go.Frame(
        data=[go.Scatter(x=x, y=np.sin(freq * x))],
        name=str(freq)
    ))
    slider_steps.append(dict(
        args=[[str(freq)], dict(frame=dict(duration=0), mode='immediate')],
        label=f'{freq:.1f}',
        method='animate'
    ))

fig.add_trace(go.Scatter(x=x, y=np.sin(0.5 * x)))
fig.frames = frames

fig.update_layout(
    sliders=[dict(
        active=0,
        steps=slider_steps,
        currentvalue=dict(prefix='Frequency: ', suffix=' Hz'),
        x=0.1, len=0.8,
    )]
)
```

## Plotly Animations

### Quick animation with px

```python
import plotly.express as px

df = px.data.gapminder()
fig = px.scatter(df, x='gdpPercap', y='lifeExp',
    size='pop', color='continent', hover_name='country',
    animation_frame='year', animation_group='country',
    log_x=True, size_max=55,
    range_x=[100, 100000], range_y=[25, 90])
fig.show()
```

**Critical:** Set `range_x` and `range_y` explicitly. Without fixed ranges, axes rescale per frame and the animation is disorienting.

### Custom animation with go.Frame

```python
import plotly.graph_objects as go
import numpy as np

t = np.linspace(0, 2*np.pi, 100)
fig = go.Figure(
    data=[go.Scatter(x=t, y=np.sin(t), mode='lines')],
    layout=go.Layout(
        xaxis=dict(range=[0, 2*np.pi]),
        yaxis=dict(range=[-2, 2]),
        updatemenus=[dict(type='buttons', showactive=False,
            buttons=[
                dict(label='Play', method='animate',
                     args=[None, dict(frame=dict(duration=50),
                                      fromcurrent=True)]),
                dict(label='Pause', method='animate',
                     args=[[None], dict(frame=dict(duration=0),
                                        mode='immediate')])
            ]
        )]
    ),
    frames=[go.Frame(data=[go.Scatter(x=t, y=np.sin(t + phase))])
            for phase in np.linspace(0, 2*np.pi, 60)]
)
```

### Animation transition settings

```python
fig.layout.updatemenus[0].buttons[0].args[1] = dict(
    frame=dict(duration=100, redraw=True),
    transition=dict(duration=50, easing='cubic-in-out'),
    fromcurrent=True,
    mode='immediate',
)
```

**Easing options:** `linear`, `quad`, `cubic`, `sin`, `exp`, `circle`, `elastic`, `back`, `bounce` — each with `-in`, `-out`, `-in-out` variants.

## Selection and Click Events

### Box/lasso select

Enabled by default in Plotly. Selected points fire `selectedData` event.

```python
fig.update_layout(
    dragmode='select',        # 'select' (box), 'lasso', 'zoom', 'pan'
    selectdirection='h',      # 'h', 'v', 'd' (diagonal), 'any'
)

fig.update_traces(
    selected=dict(marker=dict(color='red', size=12)),
    unselected=dict(marker=dict(color='gray', opacity=0.3)),
)
```

### Click events (Jupyter only)

```python
from plotly.callbacks import Points

fig = go.FigureWidget(data=[go.Scatter(x=x, y=y, mode='markers')])

def on_click(trace, points, state):
    print(f"Clicked point index: {points.point_inds}")
    print(f"X: {points.xs}, Y: {points.ys}")

fig.data[0].on_click(on_click)
```

**Note:** Full interactive callbacks (updating other charts on click) require Dash. In Jupyter, `FigureWidget` supports basic click/select/hover callbacks.

## Performance Tips

1. **WebGL for large datasets:** `px.scatter(..., render_mode='webgl')` or `go.Scattergl` instead of `go.Scatter`. Handles 100K+ points smoothly.
2. **Reduce hover data:** Large `customdata` arrays slow hover. Only include what's displayed.
3. **Limit animation frames:** 30-60 frames is usually enough. More frames = slower load.
4. **Use `fig.update` over repeated `fig.add`:** Batch updates are faster than iterative trace additions.
