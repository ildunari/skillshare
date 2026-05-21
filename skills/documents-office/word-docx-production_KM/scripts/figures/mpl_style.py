#!/usr/bin/env python3
"""Matplotlib style helpers for docx-enhanced.

Loads JSON style specs from assets/style-specs and applies a doc-friendly
matplotlib rcParams profile (fonts, sizes, grid, color cycle).

This module is intentionally dependency-light: it only requires matplotlib.

Example:

    from mpl_style import mpl_style_context, figure_size_for_doc, save_figure
    import matplotlib.pyplot as plt

    with mpl_style_context("business"):
        fig, ax = plt.subplots(figsize=figure_size_for_doc("business", width="full"))
        ax.plot([0, 1, 2], [1.0, 0.6, 0.9])
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Response")
        save_figure(fig, "out/figure.png")

"""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Tuple, Union


SpecLike = Union[str, Path, Dict[str, Any]]


def _assets_root() -> Path:
    # scripts/figures/mpl_style.py -> scripts/figures -> scripts -> repo root
    return Path(__file__).resolve().parents[2] / "assets"


def resolve_spec_path(name_or_path: str) -> Path:
    p = Path(name_or_path)
    if p.exists():
        return p

    aliases = {
        "academic": "academic_manuscript_generic",
        "business": "business_report_modern",
        "technical": "technical_report_engineering",
    }
    name = aliases.get(name_or_path, name_or_path)
    return _assets_root() / "style-specs" / f"{name}.json"


def load_style_spec(name_or_path: Union[str, Path]) -> Dict[str, Any]:
    p = resolve_spec_path(str(name_or_path))
    if not p.exists():
        raise FileNotFoundError(f"Style spec not found: {p}")
    return json.loads(p.read_text(encoding="utf8"))


def _page_size_in(spec: Dict[str, Any]) -> Tuple[float, float]:
    size = str(spec.get("page", {}).get("size", "Letter")).lower().strip()
    if size == "a4":
        # A4 = 210mm x 297mm => 8.2677 x 11.6929 in
        return (8.2677, 11.6929)
    # Letter
    return (8.5, 11.0)


def text_width_in(spec_or_name: SpecLike) -> float:
    spec = load_style_spec(spec_or_name) if isinstance(spec_or_name, (str, Path)) else spec_or_name
    page_w, _ = _page_size_in(spec)
    margins = spec.get("page", {}).get("margins_in", {})
    left = float(margins.get("left", 1.0))
    right = float(margins.get("right", 1.0))
    return page_w - left - right


def figure_size_for_doc(
    spec_or_name: SpecLike,
    width: Union[str, float] = "full",
    gutter_in: float = 0.25,
    aspect: float = 0.62,
    height_in: Optional[float] = None,
) -> Tuple[float, float]:
    """Return a (width_in, height_in) tuple sized to the document text box.

    width:
      - "full"  : full text width
      - "half"  : 2-up layout (half width minus gutter)
      - "third" : 3-up layout (third width minus gutters)
      - float     : explicit width in inches
    """
    tw = text_width_in(spec_or_name)

    if isinstance(width, (int, float)):
        w = float(width)
    else:
        wkey = str(width).lower().strip()
        if wkey in ("full", "1"):
            w = tw
        elif wkey in ("half", "0.5", "2col", "two-column", "two_col"):
            w = max(1.0, (tw - gutter_in) / 2.0)
        elif wkey in ("third", "0.33"):
            w = max(1.0, (tw - 2.0 * gutter_in) / 3.0)
        else:
            raise ValueError(f"Unknown width spec: {width}")

    h = float(height_in) if height_in is not None else w * float(aspect)
    return (w, h)


def _strip_hash(hex_color: str) -> str:
    h = hex_color.strip()
    return h[1:] if h.startswith("#") else h


def _hex_or_none(v: Any) -> Optional[str]:
    if not isinstance(v, str):
        return None
    h = _strip_hash(v).upper().strip()
    if len(h) == 6 and all(c in "0123456789ABCDEF" for c in h):
        return h
    return None


def _resolve_color(spec: Dict[str, Any], key_or_hex: Any, default: str) -> str:
    if key_or_hex is None:
        return default
    v = key_or_hex
    if isinstance(v, str) and "colors" in spec and isinstance(spec["colors"], dict) and v in spec["colors"]:
        v = spec["colors"][v]
    hx = _hex_or_none(v)
    return ("#" + hx) if hx else default


def _resolve_font(spec: Dict[str, Any], which: str = "body") -> str:
    fonts = spec.get("fonts", {})
    record = fonts.get(which, {}) if isinstance(fonts, dict) else {}
    family = record.get("family") if isinstance(record, dict) else None
    fallback = record.get("fallback") if isinstance(record, dict) else None

    if isinstance(family, str) and family.strip():
        fam = family.strip()
        # Match stylekit behavior: Aptos isn't always present; prefer declared fallbacks.
        if fam.lower().startswith("aptos") and isinstance(fallback, list) and fallback:
            return str(fallback[0])
        return fam

    return "Calibri"


def _body_font_size_pt(spec: Dict[str, Any]) -> float:
    body = spec.get("fonts", {}).get("body", {})
    if isinstance(body, dict) and isinstance(body.get("size_pt"), (int, float)):
        return float(body["size_pt"])
    return 11.0


def mpl_rc(spec_or_name: SpecLike, mode: str = "color") -> Dict[str, Any]:
    """Return matplotlib rcParams matching the doc style."""
    import matplotlib as mpl

    spec = load_style_spec(spec_or_name) if isinstance(spec_or_name, (str, Path)) else spec_or_name
    body_pt = _body_font_size_pt(spec)

    # In-doc figures typically look best slightly smaller than body text.
    base_pt = max(8.0, body_pt - 2.0)

    font_family = _resolve_font(spec, "body")

    accent = _resolve_color(spec, "accent", default="#1f77b4")
    text = _resolve_color(spec, "mutedText", default="#222222")

    grid = "#D9D9D9"
    spine = "#4D4D4D"

    # Build a cycle where the first series uses the document accent color.
    tab10 = list(mpl.rcParams.get("axes.prop_cycle").by_key().get("color", []))
    cycle = [accent] + [c for c in tab10 if c.lower() != accent.lower()]
    if not cycle:
        cycle = [accent]

    mode_key = str(mode).lower().strip()
    if mode_key in ("mono", "monochrome", "bw", "blackwhite"):
        cycle = ["#000000", "#555555", "#888888", "#AAAAAA"]

    return {
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "sans-serif",
        "font.sans-serif": [font_family, "Calibri", "Arial", "DejaVu Sans"],
        "font.size": base_pt,
        "text.color": text,
        "axes.labelcolor": text,
        "xtick.color": text,
        "ytick.color": text,
        "axes.edgecolor": spine,
        "axes.linewidth": 0.8,
        "axes.titlesize": base_pt + 1.0,
        "axes.labelsize": base_pt,
        "xtick.labelsize": max(6.0, base_pt - 1.0),
        "ytick.labelsize": max(6.0, base_pt - 1.0),
        "legend.fontsize": max(6.0, base_pt - 1.0),
        "legend.frameon": False,
        "lines.linewidth": 1.6,
        "lines.markersize": 4.0,
        "axes.grid": True,
        "grid.color": grid,
        "grid.linewidth": 0.5,
        "grid.alpha": 1.0,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler("color", cycle),
    }


@contextmanager
def mpl_style_context(spec_or_name: SpecLike, mode: str = "color") -> Iterator[None]:
    """Context manager that applies rcParams."""
    import matplotlib as mpl

    with mpl.rc_context(rc=mpl_rc(spec_or_name, mode=mode)):
        yield


def save_figure(fig: Any, path: Union[str, Path], dpi: int = 300) -> Path:
    """Save a figure with doc-friendly defaults."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi, bbox_inches="tight", pad_inches=0.02)
    return out
