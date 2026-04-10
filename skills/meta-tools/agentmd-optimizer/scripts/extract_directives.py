#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _shared import count_all_caps_lines, count_emphasis_hits, estimate_directive_count, headings, load_inventory, likely_directive_lines, safe_read_text, stale_hits, write_json

CATEGORY_PATTERNS = [
    (re.compile(r"test|lint|typecheck|verify|validate", re.I), "validation"),
    (re.compile(r"git|commit|branch|pr|pull request", re.I), "git"),
    (re.compile(r"tool|bash|read|write|edit|browser|web", re.I), "tools"),
    (re.compile(r"format|response|markdown|style|voice|tone", re.I), "response-style"),
    (re.compile(r"security|secret|credential|token|password", re.I), "security"),
    (re.compile(r"plan|report|summary|steps|workflow", re.I), "workflow"),
]


def categorize(line: str) -> str:
    for pattern, label in CATEGORY_PATTERNS:
        if pattern.search(line):
            return label
    return "general"


def strength(line: str) -> str:
    u = line.upper()
    if any(word in u for word in ["MUST", "NEVER", "ALWAYS", "CRITICAL"]):
        return "hard"
    if re.search(r"\b(should|prefer|when|if|before|after|avoid)\b", line, re.I):
        return "conditional"
    return "normal"


def main():
    parser = argparse.ArgumentParser(description="Extract directive-like instructions from inventory files.")
    parser.add_argument("inventory")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    directives = []
    file_stats = []

    for idx, item in enumerate(files):
        path = item["path"]
        text = safe_read_text(path)
        lines = likely_directive_lines(text)
        for line_idx, line in enumerate(lines, start=1):
            directives.append({
                "directive_id": f"d-{idx:03d}-{line_idx:03d}",
                "file": path,
                "runtime": item.get("runtime"),
                "scope": item.get("scope"),
                "category": categorize(line),
                "strength": strength(line),
                "text": line,
            })
        file_stats.append({
            "path": path,
            "runtime": item.get("runtime"),
            "scope": item.get("scope"),
            "directive_count": len(lines),
            "heading_count": len(headings(text)),
            "emphasis_hits": count_emphasis_hits(text),
            "all_caps_lines": count_all_caps_lines(text),
            "stale_hits": stale_hits(text),
        })

    payload = {
        "summary": {
            "file_count": len(files),
            "directive_count": len(directives),
        },
        "file_stats": sorted(file_stats, key=lambda f: f["directive_count"], reverse=True),
        "directives": directives,
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
