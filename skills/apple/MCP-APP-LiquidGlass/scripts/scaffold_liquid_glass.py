#!/usr/bin/env python3
"""Emit starter liquid-glass components into an output directory.

Usage:
  python scaffold_liquid_glass.py /path/to/output
  python scaffold_liquid_glass.py /path/to/output --components button panel dock css svg-filter library-card html-demo
"""

from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATES = {
    "button": "LiquidGlassButton.tsx",
    "panel": "LiquidGlassPanel.tsx",
    "dock": "LiquidGlassDock.tsx",
    "css": "liquid-glass.css",
    "svg-filter": "LiquidGlassFilter.tsx",
    "library-card": "LiquidGlassCard.tsx",
    "html-demo": "liquid-glass-template.html",
    "index": "index.ts",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--components",
        nargs="+",
        default=["button", "panel", "dock", "css", "svg-filter", "index"],
        choices=sorted(TEMPLATES.keys()),
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "templates"
    out_dir = args.output.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for key in args.components:
        src = template_root / TEMPLATES[key]
        dst = out_dir / src.name
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"wrote {dst}")

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
