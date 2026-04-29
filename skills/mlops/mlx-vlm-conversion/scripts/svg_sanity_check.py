#!/usr/bin/env python3
"""Extract and validate SVG text from model output.

This checks XML syntax and that the root element is SVG. It does not judge
visual quality; rendering or human/automated visual comparison is still needed.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_RE = re.compile(r"<svg\b[\s\S]*?</svg>", re.IGNORECASE)


def extract_svg(text: str) -> str:
    match = SVG_RE.search(text)
    if not match:
        raise ValueError("No complete <svg>...</svg> block found")
    return match.group(0)


def root_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1].lower()
    return tag.lower()


def validate_svg(svg_text: str) -> ET.Element:
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        raise ValueError(f"SVG XML parse error: {exc}") from exc
    if root_name(root.tag) != "svg":
        raise ValueError(f"Root element is {root.tag!r}, not svg")
    return root


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract and syntax-check SVG from model output text.")
    parser.add_argument("input", help="Text file containing model output, or '-' for stdin")
    parser.add_argument("--write-svg", help="Optional path to write extracted SVG")
    args = parser.parse_args()

    text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
    try:
        svg = extract_svg(text)
        root = validate_svg(svg)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    if args.write_svg:
        Path(args.write_svg).parent.mkdir(parents=True, exist_ok=True)
        Path(args.write_svg).write_text(svg + "\n", encoding="utf-8")

    width = root.attrib.get("width", "")
    height = root.attrib.get("height", "")
    viewbox = root.attrib.get("viewBox", root.attrib.get("viewbox", ""))
    print("PASS: valid SVG XML")
    print(f"root_attributes: width={width!r} height={height!r} viewBox={viewbox!r}")
    print(f"elements: {sum(1 for _ in root.iter())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
