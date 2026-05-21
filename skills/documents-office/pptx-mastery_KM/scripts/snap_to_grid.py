#!/usr/bin/env python3
"""Snap element bounding boxes to the deck grid.

This is a deterministic helper for the repair loop.

What it does:
- Snaps x and w to nearest column boundaries.
- Snaps y and h to a vertical rhythm step (default 0.1in).

Usage:
  python scripts/snap_to_grid.py deck.ir.json --out deck.snapped.ir.json

Notes:
- Only adjusts elements that have `bbox`.
- Will not move elements beyond margins.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

EMU_PER_INCH = 914400


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def round_to_step(v: float, step: float) -> float:
    return round(v / step) * step


@dataclass
class Grid:
    w: float
    h: float
    m_t: float
    m_r: float
    m_b: float
    m_l: float
    columns: int
    gutter: float

    @property
    def content_w(self) -> float:
        return self.w - self.m_l - self.m_r

    @property
    def col_w(self) -> float:
        return (self.content_w - self.gutter * (self.columns - 1)) / self.columns

    def col_x(self, idx: int) -> float:
        # idx is 0-based column index
        return self.m_l + idx * (self.col_w + self.gutter)

    def nearest_col_boundary(self, x: float) -> float:
        boundaries = [self.m_l]
        for i in range(1, self.columns + 1):
            # right edge of column i
            boundaries.append(self.m_l + i * self.col_w + (i - 1) * self.gutter)
        return min(boundaries, key=lambda b: abs(b - x))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ir", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--y-step", type=float, default=0.1)
    args = ap.parse_args()

    ir = json.loads(args.ir.read_text(encoding="utf-8"))
    tokens = ir.get("deck", {}).get("tokens", {})
    grid_t = tokens.get("grid", {})
    canvas = grid_t.get("canvas", {})
    margins = grid_t.get("margins_in", {})

    grid = Grid(
        w=float(canvas.get("w_in", 13.333)),
        h=float(canvas.get("h_in", 7.5)),
        m_t=float(margins.get("t", 0.7)),
        m_r=float(margins.get("r", 0.7)),
        m_b=float(margins.get("b", 0.7)),
        m_l=float(margins.get("l", 0.7)),
        columns=int(grid_t.get("columns", 12)),
        gutter=float(grid_t.get("gutter_in", 0.25)),
    )

    for slide in ir.get("deck", {}).get("slides", []):
        for el in slide.get("elements", []):
            bbox = el.get("bbox")
            if not bbox:
                continue
            x, y, w, h = (float(bbox.get("x", 0)), float(bbox.get("y", 0)), float(bbox.get("w", 0)), float(bbox.get("h", 0)))

            # Snap x and w to nearest column boundaries.
            x2 = x + w
            nx = grid.nearest_col_boundary(x)
            nx2 = grid.nearest_col_boundary(x2)
            if nx2 <= nx:
                # fallback: keep width, just snap left
                nx2 = nx + w

            # Snap y/h to vertical rhythm.
            ny = round_to_step(y, args.y_step)
            nh = round_to_step(h, args.y_step)

            # Clamp to safe content region.
            nx = clamp(nx, grid.m_l, grid.w - grid.m_r)
            ny = clamp(ny, grid.m_t, grid.h - grid.m_b)
            nx2 = clamp(nx2, grid.m_l, grid.w - grid.m_r)
            nh = clamp(nh, args.y_step, grid.h - grid.m_t - grid.m_b)

            bbox["x"] = round(nx, 4)
            bbox["y"] = round(ny, 4)
            bbox["w"] = round(nx2 - nx, 4)
            bbox["h"] = round(nh, 4)

            # recurse into children
            for child in el.get("children", []) if isinstance(el.get("children"), list) else []:
                cb = child.get("bbox")
                if cb:
                    # Children are usually absolute in this IR. Snap lightly.
                    cb["x"] = round(clamp(grid.nearest_col_boundary(float(cb.get("x", 0))), grid.m_l, grid.w - grid.m_r), 4)
                    cb["y"] = round(round_to_step(float(cb.get("y", 0)), args.y_step), 4)

    args.out.write_text(json.dumps(ir, indent=2), encoding="utf-8")
    print(f"✅ Snapped IR written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
