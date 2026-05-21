# Matplotlib Animation Guide

Creating animated figures with matplotlib and saving as GIF, MP4, or HTML5 video.

## Two Animation Classes

| Class | How it works | Best for |
|---|---|---|
| `FuncAnimation` | Calls a function repeatedly to update artists | Most cases — efficient, low memory |
| `ArtistAnimation` | Pre-computes list of artist frames | Pre-rendered frames, simpler but uses more memory |

**Default choice:** `FuncAnimation`. Only use `ArtistAnimation` when frames are already pre-computed (e.g., from simulation output).

## FuncAnimation: The 7-Step Recipe

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 1. Create figure and axes
fig, ax = plt.subplots(figsize=(8, 5))

# 2. Create initial (empty) artists — STORE references
line, = ax.plot([], [], 'b-', linewidth=2)
point, = ax.plot([], [], 'ro', markersize=8)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# 3. Set axis limits (important — won't auto-scale during animation)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')

# 4. Define init function (clears artists for blitting)
def init():
    line.set_data([], [])
    point.set_data([], [])
    time_text.set_text('')
    return line, point, time_text

# 5. Define update function (modifies artists per frame)
x = np.linspace(0, 2*np.pi, 200)

def update(frame):
    y = np.sin(x + frame * 0.1)
    line.set_data(x, y)
    point.set_data([x[frame % len(x)]], [y[frame % len(x)]])
    time_text.set_text(f'Frame: {frame}')
    return line, point, time_text

# 6. Create FuncAnimation
ani = animation.FuncAnimation(
    fig,
    update,
    frames=100,          # number of frames (or iterable, or generator)
    init_func=init,
    blit=True,           # only redraw changed artists (faster)
    interval=50,         # milliseconds between frames (display only)
    repeat=True,         # loop animation
)

# 7. Save or show
ani.save('animation.gif', writer='pillow', fps=20)
plt.show()
```

### Critical details

- **Store artist references:** `line, = ax.plot(...)` (note the comma — unpacks single-element tuple).
- **Return artists from update and init:** Required when `blit=True`. Return as tuple.
- **Set axis limits explicitly:** Auto-scaling doesn't work during animation.
- **Keep `ani` alive:** The animation object MUST be stored in a variable. If garbage-collected, animation stops silently.

### Using functools.partial for cleaner code

```python
from functools import partial

def update(frame, line, data_x, data_y):
    line.set_data(data_x[:frame], data_y[:frame])
    return line,

ani = animation.FuncAnimation(
    fig,
    partial(update, line=line, data_x=x, data_y=y),
    frames=len(x),
    blit=True,
)
```

### Frames parameter options

```python
# Integer: equivalent to range(100)
frames=100

# Iterable: explicit frame values
frames=np.linspace(0, 2*np.pi, 60)

# Generator function: lazy evaluation, memory efficient
def gen_data():
    t = 0
    while t < 10:
        yield t
        t += 0.1
frames=gen_data  # NOTE: pass function, not gen_data()
# When using generators, set save_count to limit cached frames:
# animation.FuncAnimation(..., frames=gen_data, save_count=100)
```

## ArtistAnimation

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.2, 1.2)

x = np.linspace(0, 2*np.pi, 200)
artist_frames = []

for phase in np.linspace(0, 2*np.pi, 60):
    line, = ax.plot(x, np.sin(x + phase), 'b-')
    title = ax.text(0.5, 1.05, f'Phase: {phase:.2f}',
                    transform=ax.transAxes, ha='center')
    artist_frames.append([line, title])

ani = animation.ArtistAnimation(fig, artist_frames, interval=50, blit=True)
ani.save('artist_anim.gif', writer='pillow', fps=20)
```

## Saving Animations

### Writer comparison

| Writer | Format | Dependencies | Best for |
|---|---|---|---|
| `PillowWriter` | GIF, APNG | `pillow` (usually installed) | GIFs — no extra deps needed |
| `FFMpegWriter` | MP4, MKV, AVI | `ffmpeg` binary | Video — best quality/compression |
| `ImageMagickWriter` | GIF | `imagemagick` binary | GIFs (alternative to Pillow) |
| `HTMLWriter` | HTML | None | Jupyter/web embedding |

### GIF (recommended: PillowWriter)

```python
ani.save('output.gif', writer='pillow', fps=20, dpi=100)

# Or with explicit writer for more control:
writer = animation.PillowWriter(fps=20, metadata=dict(artist='Author'))
ani.save('output.gif', writer=writer, dpi=100)
```

**GIF tips:**
- Keep DPI low (72-100) to control file size
- Fewer frames + higher interval = smaller GIF
- GIFs are limited to 256 colors — fine for plots, bad for photographic content

### MP4 (recommended: FFMpegWriter)

```python
ani.save('output.mp4', writer='ffmpeg', fps=30, dpi=150)

# With explicit writer:
writer = animation.FFMpegWriter(
    fps=30,
    bitrate=1800,           # higher = better quality, larger file
    metadata=dict(title='My Animation', artist='Author'),
    extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'],
)
ani.save('output.mp4', writer=writer, dpi=150)
```

**Important:** `fps` in the writer controls the **saved** frame rate. `interval` in FuncAnimation controls the **display** frame rate. They are independent.

### HTML5 video (for Jupyter)

```python
# Inline display in Jupyter:
from IPython.display import HTML
HTML(ani.to_html5_video())

# Or save as HTML file:
ani.save('output.html', writer='html')
```

### Checking available writers

```python
print(animation.writers.list())
# Typical output: ['pillow', 'ffmpeg', 'ffmpeg_file', 'html']
```

## Common Gotchas

1. **Animation stops immediately:**
   ```python
   # WRONG — ani is garbage-collected
   animation.FuncAnimation(fig, update, frames=100)
   plt.show()

   # RIGHT — store reference
   ani = animation.FuncAnimation(fig, update, frames=100)
   plt.show()
   ```

2. **Blit + changed axes = artifacts:**
   Blitting only redraws returned artists. If you change axis labels or titles in `update()`, they won't refresh. Either:
   - Return them in the artist tuple
   - Set `blit=False` (slower but redraws everything)

3. **Generator frames + save = save_count needed:**
   ```python
   ani = animation.FuncAnimation(fig, update, frames=my_generator,
                                  save_count=200)  # how many frames to cache
   ```

4. **ffmpeg not found:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   # macOS
   brew install ffmpeg
   # Conda
   conda install -c conda-forge ffmpeg
   ```
   Or fall back to PillowWriter for GIF output.

5. **Large GIF files:**
   Reduce DPI, frame count, or figure size. A 100-frame 150DPI animation can be >10MB as GIF. Consider MP4 instead.

## Biomedical Animation Examples

### Drug release over time

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 72)
ax.set_ylim(0, 100)
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Cumulative Release (%)')
ax.set_title('Drug Release Kinetics')

t = np.linspace(0, 72, 200)
release = 100 * (1 - np.exp(-0.05 * t))  # first-order model

line, = ax.plot([], [], 'b-', linewidth=2)
fill = ax.fill_between([], [], alpha=0.2, color='blue')
text = ax.text(0.7, 0.3, '', transform=ax.transAxes, fontsize=14)

def update(frame):
    global fill
    fill.remove()
    line.set_data(t[:frame], release[:frame])
    fill = ax.fill_between(t[:frame], release[:frame], alpha=0.2, color='blue')
    if frame > 0:
        text.set_text(f'Release: {release[frame-1]:.1f}%')
    return line, text

ani = animation.FuncAnimation(fig, update, frames=len(t), interval=30)
ani.save('drug_release.gif', writer='pillow', fps=30, dpi=100)
```

### Nanoparticle diffusion

```python
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.set_aspect('equal')
ax.set_title('Nanoparticle Diffusion')

n_particles = 50
positions = np.zeros((n_particles, 2))
scat = ax.scatter(positions[:, 0], positions[:, 1], s=20, alpha=0.6)

def update(frame):
    global positions
    positions += np.random.randn(n_particles, 2) * 0.5
    scat.set_offsets(positions)
    return scat,

ani = animation.FuncAnimation(fig, update, frames=300, interval=30, blit=True)
ani.save('diffusion.gif', writer='pillow', fps=30, dpi=80)
```

## Claude Environment Notes

- **Pillow** is available in the Claude container — GIF export always works.
- **ffmpeg** may or may not be installed. Always try PillowWriter first for GIF. Check with `animation.writers.list()`.
- For MP4, install with `subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'])` if needed and network is available.
- Display: `plt.show()` won't render in Claude. Save to file and present.
