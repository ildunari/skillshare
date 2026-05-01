#!/usr/bin/env python3
"""WCAG contrast calculator with lightweight Office theme color resolution."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

THEME_NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
THEME_ALIASES = {
    "background1": "lt1",
    "text1": "dk1",
    "background2": "lt2",
    "text2": "dk2",
    "hyperlink": "hlink",
    "followedhyperlink": "folHlink",
}


def normalize_hex(value: str) -> str:
    value = value.strip()
    if value.startswith("theme:"):
        raise ValueError(f"Theme color {value!r} requires --theme and --fg-theme/--bg-theme")
    if value.startswith("#"):
        value = value[1:]
    if re.fullmatch(r"[0-9a-fA-F]{3}", value):
        value = "".join(ch * 2 for ch in value)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        raise ValueError(f"Invalid RGB color: {value!r}")
    return value.upper()


def parse_theme(theme_path: Optional[str]) -> Dict[str, str]:
    if not theme_path:
        return {}
    root = ET.parse(theme_path).getroot()
    scheme = root.find(".//a:clrScheme", THEME_NS)
    colors: Dict[str, str] = {}
    if scheme is None:
        return colors
    for child in list(scheme):
        name = child.tag.split("}", 1)[-1]
        srgb = child.find(".//a:srgbClr", THEME_NS)
        sysclr = child.find(".//a:sysClr", THEME_NS)
        if srgb is not None and srgb.get("val"):
            colors[name] = normalize_hex(srgb.get("val", ""))
        elif sysclr is not None and sysclr.get("lastClr"):
            colors[name] = normalize_hex(sysclr.get("lastClr", ""))
    return colors


def resolve_color(value: Optional[str], theme_key: Optional[str], theme: Dict[str, str], role: str) -> Tuple[str, str]:
    if theme_key:
        key = THEME_ALIASES.get(theme_key.lower(), theme_key)
        if key not in theme:
            raise ValueError(f"Theme color {theme_key!r} for {role} not found in theme file")
        return theme[key], f"theme:{key}"
    if not value:
        raise ValueError(f"Missing {role} color")
    if value.startswith("theme:"):
        key = THEME_ALIASES.get(value.split(":", 1)[1].lower(), value.split(":", 1)[1])
        if key not in theme:
            raise ValueError(f"Theme color {key!r} for {role} not found in theme file")
        return theme[key], f"theme:{key}"
    return normalize_hex(value), "literal"


def rgb_tuple(hex_color: str) -> Tuple[float, float, float]:
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def linearize(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    r, g, b = (linearize(c) for c in rgb_tuple(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = luminance(fg), luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def threshold(args: argparse.Namespace) -> float:
    if args.non_text:
        return 3.0
    if args.font_size_pt is not None:
        if args.font_size_pt >= 18 or (args.bold and args.font_size_pt >= 14):
            return 3.0
    return 4.5


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate WCAG contrast ratio.")
    parser.add_argument("--fg", help="Foreground RGB color, e.g. #777777 or 777777")
    parser.add_argument("--bg", help="Background RGB color, e.g. #FFFFFF or FFFFFF")
    parser.add_argument("--fg-theme", help="Foreground Office theme slot, e.g. accent2")
    parser.add_argument("--bg-theme", help="Background Office theme slot, e.g. lt1")
    parser.add_argument("--theme", help="Path to Office theme XML, e.g. ppt/theme/theme1.xml")
    parser.add_argument("--font-size-pt", type=float, help="Text size in points")
    parser.add_argument("--bold", action="store_true", help="Text is bold")
    parser.add_argument("--non-text", action="store_true", help="Use WCAG 1.4.11 non-text threshold")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    try:
        theme = parse_theme(args.theme)
        fg, fg_source = resolve_color(args.fg, args.fg_theme, theme, "foreground")
        bg, bg_source = resolve_color(args.bg, args.bg_theme, theme, "background")
        ratio = contrast_ratio(fg, bg)
        target = threshold(args)
        result = {
            "foreground": f"#{fg}",
            "background": f"#{bg}",
            "foreground_source": fg_source,
            "background_source": bg_source,
            "ratio": round(ratio, 4),
            "threshold": target,
            "passes": ratio >= target,
            "criterion": "WCAG 2.2 1.4.11" if args.non_text else "WCAG 2.2 1.4.3",
            "note": "Ratios are not rounded up for pass/fail decisions."
        }
        print(json.dumps(result, indent=2 if args.pretty else None))
        return 0 if result["passes"] else 2
    except Exception as exc:  # noqa: BLE001 - CLI should surface friendly errors
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
