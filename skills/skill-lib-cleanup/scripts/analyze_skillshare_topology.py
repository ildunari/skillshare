#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from _shared import load_json, load_skillshare_config, skill_slug_from_path, write_json


def main():
    parser = argparse.ArgumentParser(description="Analyze canonical source and target topology from skillshare config.")
    parser.add_argument("discovery")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    data = load_json(args.discovery)
    items = data.get("items", data.get("files", []))
    cfg = load_skillshare_config()
    source = cfg.get("source", "/Users/kosta/.config/skillshare/skills")
    targets = {name: meta.get("path") for name, meta in (cfg.get("targets") or {}).items() if isinstance(meta, dict) and meta.get("path")}

    by_slug = defaultdict(list)
    for item in items:
        slug = item.get("slug") or skill_slug_from_path(item.get("path", ""))
        if slug:
            by_slug[slug].append(item)

    skills = []
    for slug, copies in sorted(by_slug.items()):
        source_copy = [c for c in copies if c.get("path", "").startswith(source)]
        installed = []
        for target_name, target_path in targets.items():
            matches = [c for c in copies if c.get("path", "").startswith(target_path)]
            installed.append({
                "target": target_name,
                "path": target_path,
                "status": "present" if matches else "missing",
                "copies": [m.get("path") for m in matches],
                "hashes": sorted({m.get("content_hash") for m in matches}),
            })
        skills.append({
            "skill_slug": slug,
            "source_path": source_copy[0].get("path") if source_copy else None,
            "source_hash": source_copy[0].get("content_hash") if source_copy else None,
            "source_present": bool(source_copy),
            "targets": installed,
            "copy_count": len(copies),
        })

    payload = {
        "summary": {
            "canonical_source": source,
            "target_count": len(targets),
            "skill_count": len(skills),
            "source_missing_skills": sum(1 for s in skills if not s["source_present"]),
        },
        "targets": [{"name": k, "path": v} for k, v in targets.items()],
        "skills": skills,
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
