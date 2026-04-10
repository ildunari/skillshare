#!/usr/bin/env python3
"""
ui_slop_scan.py

A lightweight repo scanner that flags common "generic AI/template UI" signals:
- overused default fonts (Inter/Roboto/etc.)
- heavy glass/backdrop-filter usage
- centered body text patterns
- excessive gradient usage (very rough heuristic)
- autoplay video
- frequent generic Tailwind classes (rounded-xl/shadow-lg everywhere)

This is not a linter. It's a heuristic report to guide human review.

Usage:
  python scripts/ui_slop_scan.py --root . --max-files 500
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


EXTS = {".html", ".css", ".scss", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".mdx"}


@dataclass
class Hit:
    rule: str
    path: str
    line: int
    snippet: str


def iter_files(root: Path, max_files: int) -> Iterable[Path]:
    count = 0
    for p in root.rglob("*"):
        if count >= max_files:
            return
        if p.is_file() and p.suffix.lower() in EXTS:
            yield p
            count += 1


def scan_text(text: str, rules: List[Tuple[str, re.Pattern]]) -> List[Tuple[str, int, str]]:
    hits: List[Tuple[str, int, str]] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        for name, pat in rules:
            if pat.search(line):
                snippet = line.strip()
                if len(snippet) > 240:
                    snippet = snippet[:237] + "..."
                hits.append((name, i, snippet))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Repo root to scan")
    ap.add_argument("--max-files", type=int, default=800, help="Limit files scanned")
    ap.add_argument("--max-hits", type=int, default=1200, help="Limit total hits printed")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")

    rules: List[Tuple[str, re.Pattern]] = [
        ("generic-font", re.compile(r"\b(Inter|Roboto|Open Sans|Montserrat|Lato)\b")),
        ("centered-body-text", re.compile(r"\b(text-align:\s*center|text-center\b)\b")),
        ("glass/backdrop-filter", re.compile(r"\b(backdrop-filter|bg-white/10|bg-black/10|blur\()\b")),
        ("heavy-gradient", re.compile(r"\b(linear-gradient|radial-gradient)\b")),
        ("autoplay", re.compile(r"\bautoplay\b")),
        ("generic-tailwind-radius", re.compile(r"\b(rounded-xl|rounded-2xl|rounded-3xl)\b")),
        ("generic-tailwind-shadow", re.compile(r"\b(shadow-lg|shadow-xl|drop-shadow)\b")),
    ]

    all_hits: List[Hit] = []

    for fp in iter_files(root, args.max_files):
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        local_hits = scan_text(text, rules)
        for rule_name, line_no, snippet in local_hits:
            all_hits.append(Hit(rule=rule_name, path=str(fp.relative_to(root)), line=line_no, snippet=snippet))
            if len(all_hits) >= args.max_hits:
                break
        if len(all_hits) >= args.max_hits:
            break

    # Summaries
    by_rule = {}
    for h in all_hits:
        by_rule[h.rule] = by_rule.get(h.rule, 0) + 1

    print("# UI Slop Scan Report\n")
    print(f"- Root: `{root}`")
    print(f"- Files scanned (max): {args.max_files}")
    print(f"- Hits shown (max): {args.max_hits}")
    print("\n## Summary by rule\n")
    if not by_rule:
        print("No hits found. (This does not mean the UI is great — only that these heuristics didn't trigger.)")
        return 0

    for rule, count in sorted(by_rule.items(), key=lambda x: (-x[1], x[0])):
        print(f"- **{rule}**: {count}")

    print("\n## Findings\n")
    for h in all_hits:
        print(f"- **{h.rule}** — `{h.path}:{h.line}`")
        print(f"  - `{h.snippet}`")

    print("\n## How to use this report\n")
    print("- Treat this as a *triage list*, not a verdict.")
    print("- If a rule triggers many times, it may indicate a default/template aesthetic or an accessibility risk.")
    print("- Use the skill references to decide what to change:\n"
          "  - Typography: `references/typography-guide.md`\n"
          "  - Color: `references/color-systems.md`\n"
          "  - Motion: `references/animations.md`\n"
          "  - A11y: `references/accessibility.md`\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
