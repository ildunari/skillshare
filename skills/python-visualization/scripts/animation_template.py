"""Matplotlib animation boilerplate and save helpers.

Usage:
    from animation_template import animate_line, animate_scatter, save_animation
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from functools import partial


def animate_line(x, y_func, frames=100, interval=50, xlim=None, ylim=None,
                 xlabel='x', ylabel='y', title='', figsize=(8, 5)):
    """Create a line animation using FuncAnimation.

    Parameters
    ----------
    x : array-like
        X data (static).
    y_func : callable
        Function(x, frame_index) -> y_data for each frame.
    frames : int
        Number of animation frames.
    interval : int
        Milliseconds between frames (display only).
    xlim, ylim : tuple of (min, max), optional
        Axis limits. Auto-calculated from first/last frame if None.
    xlabel, ylabel, title : str

    Returns
    -------
    fig, ani : (Figure, FuncAnimation)
        IMPORTANT: Keep `ani` alive to prevent garbage collection.
    """
    fig, ax = plt.subplots(figsize=figsize)
    line, = ax.plot([], [], 'b-', linewidth=2)
    frame_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=9)

    if xlim is None:
        xlim = (np.min(x), np.max(x))
    if ylim is None:
        y0 = y_func(x, 0)
        y_last = y_func(x, frames - 1)
        all_y = np.concatenate([y0, y_last])
        margin = (np.max(all_y) - np.min(all_y)) * 0.1
        ylim = (np.min(all_y) - margin, np.max(all_y) + margin)

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    def init():
        line.set_data([], [])
        frame_text.set_text('')
        return line, frame_text

    def update(frame):
        y = y_func(x, frame)
        line.set_data(x, y)
        frame_text.set_text(f'Frame {frame}/{frames}')
        return line, frame_text

    ani = animation.FuncAnimation(fig, update, frames=frames,
                                   init_func=init, blit=True,
                                   interval=interval, repeat=True)
    return fig, ani


def animate_scatter(positions_func, n_frames=200, n_points=50,
                    xlim=(-50, 50), ylim=(-50, 50), interval=30,
                    title='', figsize=(6, 6), markersize=20, alpha=0.6):
    """Create a scatter/particle animation.

    Parameters
    ----------
    positions_func : callable
        Function(frame_index) -> (x_array, y_array) for each frame.
    n_frames : int
    n_points : int
        Number of particles.
    xlim, ylim : tuple
    interval : int
        Milliseconds between frames.

    Returns
    -------
    fig, ani : (Figure, FuncAnimation)
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    if title:
        ax.set_title(title)

    x0, y0 = positions_func(0)
    scat = ax.scatter(x0, y0, s=markersize, alpha=alpha)

    def update(frame):
        x, y = positions_func(frame)
        scat.set_offsets(np.column_stack([x, y]))
        return scat,

    ani = animation.FuncAnimation(fig, update, frames=n_frames,
                                   interval=interval, blit=True)
    return fig, ani


def animate_fill(x, y_func, frames=100, interval=50, xlim=None, ylim=None,
                 xlabel='x', ylabel='y', title='', figsize=(8, 5),
                 color='steelblue', fill_alpha=0.2):
    """Create a line + fill_between animation (e.g., drug release).

    Parameters
    ----------
    x : array-like
    y_func : callable
        Function(x, frame_index) -> y_data.
    color : str
        Line and fill color.
    fill_alpha : float

    Returns
    -------
    fig, ani : (Figure, FuncAnimation)
    """
    fig, ax = plt.subplots(figsize=figsize)
    line, = ax.plot([], [], '-', color=color, linewidth=2)
    value_text = ax.text(0.7, 0.3, '', transform=ax.transAxes, fontsize=12)

    y_all = y_func(x, frames - 1)
    if xlim is None:
        xlim = (np.min(x), np.max(x))
    if ylim is None:
        ylim = (0, np.max(y_all) * 1.1)

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fill_collection = [None]

    def update(frame):
        idx = max(1, int(frame * len(x) / frames))
        x_slice = x[:idx]
        y_slice = y_func(x, frame)[:idx]

        line.set_data(x_slice, y_slice)
        if fill_collection[0] is not None:
            fill_collection[0].remove()
        fill_collection[0] = ax.fill_between(x_slice, y_slice,
                                              alpha=fill_alpha, color=color)
        if len(y_slice) > 0:
            value_text.set_text(f'{y_slice[-1]:.1f}')
        return line, value_text

    ani = animation.FuncAnimation(fig, update, frames=frames,
                                   interval=interval, repeat=True)
    return fig, ani


def save_animation(ani, filename, fps=20, dpi=100, writer=None):
    """Save animation with automatic writer selection.

    Parameters
    ----------
    ani : FuncAnimation or ArtistAnimation
    filename : str
        Output path. Extension determines format (.gif, .mp4, .html).
    fps : int
        Frames per second in saved file.
    dpi : int
        Resolution for raster output.
    writer : str, optional
        Override writer. If None, auto-selects based on extension.
    """
    ext = filename.rsplit('.', 1)[-1].lower()

    if writer is None:
        if ext == 'gif':
            writer = 'pillow'
        elif ext in ('mp4', 'mkv', 'avi'):
            available = animation.writers.list()
            if 'ffmpeg' in available:
                writer = 'ffmpeg'
            else:
                print("Warning: ffmpeg not available. Falling back to pillow (GIF).")
                filename = filename.rsplit('.', 1)[0] + '.gif'
                writer = 'pillow'
        elif ext == 'html':
            writer = 'html'
        else:
            writer = 'pillow'

    print(f'Saving {filename} with {writer} writer at {fps} fps, {dpi} dpi...')
    ani.save(filename, writer=writer, fps=fps, dpi=dpi)
    print(f'Saved: {filename}')


def check_writers():
    """Print available animation writers."""
    available = animation.writers.list()
    print(f"Available writers: {available}")
    for w in ['pillow', 'ffmpeg', 'imagemagick', 'html']:
        status = 'available' if w in available else 'NOT available'
        print(f"  {w}: {status}")
    return available
