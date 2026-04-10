#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from _shared import classify_path_kind, load_inventory, write_json


def skill_slug_from_path(path: str) -> str | None:
    p = Path(path)
    parts = p.parts
    if "skills" in parts:
        idx = parts.index("skills")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def classify_role(path: str) -> str:
    lower = path.lower()
    if "/localdev/" in lower and "/skills/" in lower:
        return "source-candidate"
    if any(marker in lower for marker in ["/.claude/skills/", "/.codex/skills/", "/.gemini/skills/", "/.cursor/skills/", "/.factory/skills/", "/.kiro/skills/"]):
        return "runtime-install"
    if classify_path_kind(path) == "mirror":
        return "mirror"
    return "other"


def main():
    parser = argparse.ArgumentParser(description="Analyze skill topology across source and installed copies.")
    parser.add_argument("inventory")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    skill_files = [f for f in files if "/skills/" in f["path"]]
    groups = defaultdict(list)
    for item in skill_files:
        slug = skill_slug_from_path(item["path"])
        if slug:
            groups[slug].append(item)

    topologies = []
    for slug, items in sorted(groups.items()):
        copies = []
        hashes = {i.get("content_hash") for i in items}
        for item in sorted(items, key=lambda x: x["path"]):
            copies.append({
                "path": item["path"],
                "runtime": item.get("runtime"),
                "path_kind": item.get("path_kind"),
                "role": classify_role(item["path"]),
                "content_hash": item.get("content_hash"),
            })
        topologies.append({
            "skill_slug": slug,
            "copy_count": len(items),
            "distinct_hashes": len(hashes),
            "drift_status": "exact" if len(hashes) == 1 else "diverged",
            "copies": copies,
        })

    payload = {
        "summary": {
            "skill_count": len(topologies),
            "diverged_skills": sum(1 for t in topologies if t["drift_status"] == "diverged"),
        },
        "skills": sorted(topologies, key=lambda t: (t["copy_count"], t["distinct_hashes"]), reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
