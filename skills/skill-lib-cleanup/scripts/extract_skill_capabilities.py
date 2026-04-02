#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _shared import estimate_capability_count, headings, load_json, likely_capability_lines, safe_read_text, stale_hits, trigger_phrases, write_json


def main():
    parser = argparse.ArgumentParser(description="Extract capabilities and trigger signals from skills.")
    parser.add_argument("discovery")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    data = load_json(args.discovery)
    items = data.get("items", data.get("files", []))
    rows = []
    for item in items:
        if item.get("entity_type") != "skill" and not str(item.get("path", "")).endswith("SKILL.md"):
            continue
        text = safe_read_text(item["path"])
        rows.append({
            "slug": item.get("slug") or Path(item["path"]).parent.name,
            "path": item["path"],
            "runtime": item.get("runtime"),
            "role": item.get("role"),
            "heading_count": len(headings(text)),
            "capability_count": estimate_capability_count(text),
            "trigger_lines": trigger_phrases(text),
            "capability_lines": likely_capability_lines(text)[:25],
            "stale_hits": stale_hits(text),
            "script_count": item.get("script_count", 0),
            "reference_count": item.get("reference_count", 0),
        })
    payload = {
        "summary": {"skill_count": len(rows)},
        "skills": rows,
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
