#!/usr/bin/env python3
"""contrast.py — compute WCAG-style contrast ratio between two colors.

Usage:
  python3 contrast.py --fg "#ffffff" --bg "#7c3aed"
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass


HEX_RE = re.compile(r"^#?(?P<h>[0-9a-fA-F]{6})$")


@dataclass(frozen=True)
class RGB:
    r: int
    g: int
    b: int


def parse_hex(s: str) -> RGB:
    m = HEX_RE.match(s.strip())
    if not m:
        raise ValueError(f"Expected 6-digit hex like #aabbcc, got: {s!r}")
    h = m.group("h")
    return RGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def srgb_to_lin(c: int) -> float:
    x = c / 255.0
    return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4


def rel_lum(rgb: RGB) -> float:
    r = srgb_to_lin(rgb.r)
    g = srgb_to_lin(rgb.g)
    b = srgb_to_lin(rgb.b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: RGB, bg: RGB) -> float:
    L1 = rel_lum(fg)
    L2 = rel_lum(bg)
    hi, lo = (L1, L2) if L1 >= L2 else (L2, L1)
    return (hi + 0.05) / (lo + 0.05)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fg", required=True, help="Foreground hex color, e.g. #ffffff")
    ap.add_argument("--bg", required=True, help="Background hex color, e.g. #0f172a")
    args = ap.parse_args()

    fg = parse_hex(args.fg)
    bg = parse_hex(args.bg)

    ratio = contrast_ratio(fg, bg)
    print(f"fg={args.fg} bg={args.bg} contrast={ratio:.2f}:1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
