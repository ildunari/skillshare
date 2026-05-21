#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from _shared import (
    load_json,
    load_skillshare_config,
    normalized_discovery_items,
    normalized_target_map,
    path_startswith,
    write_json,
)


def main():
    parser = argparse.ArgumentParser(description="Analyze canonical source and target topology from skillshare config.")
    parser.add_argument("discovery")
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument(
        "--mode",
        choices=["auto", "canonical-source", "broad-sweep"],
        default="auto",
        help="Audit mode. Auto chooses canonical-source when a skillshare source is present in the scan.",
    )
    args = parser.parse_args()

    data = load_json(args.discovery)
    items = normalized_discovery_items(data)
    items = [i for i in items if i.get("entity_type") == "skill" or str(i.get("path", "")).endswith("SKILL.md")]
    cfg = load_skillshare_config()
    source = cfg.get("source")
    targets = normalized_target_map(cfg)

    if args.mode == "auto":
        mode = "canonical-source" if source and any(path_startswith(i.get("path", ""), source) for i in items) else "broad-sweep"
    else:
        mode = args.mode

    by_slug = defaultdict(list)
    for item in items:
        slug = item.get("slug")
        if slug:
            by_slug[slug].append(item)

    skills = []
    for slug, copies in sorted(by_slug.items()):
        if mode == "canonical-source":
            source_copy = [c for c in copies if source and path_startswith(c.get("path", ""), source)]
            installed = []
            for target_name, target_path in targets.items():
                matches = [c for c in copies if path_startswith(c.get("path", ""), target_path)]
                installed.append({
                    "target": target_name,
                    "path": target_path,
                    "status": "present" if matches else "missing",
                    "copies": [m.get("path") for m in matches],
                    "hashes": sorted({m.get("content_hash") for m in matches if m.get("content_hash")}),
                    "runtimes": sorted({m.get("runtime", "unknown") for m in matches}),
                })
            skills.append({
                "skill_slug": slug,
                "source_path": source_copy[0].get("path") if source_copy else None,
                "source_hash": source_copy[0].get("content_hash") if source_copy else None,
                "source_present": bool(source_copy),
                "targets": installed,
                "placements": [
                    {
                        "path": c.get("path"),
                        "runtime": c.get("runtime"),
                        "role": c.get("role"),
                        "content_hash": c.get("content_hash"),
                    }
                    for c in sorted(copies, key=lambda item: item.get("path", ""))
                ],
                "copy_count": len(copies),
            })
        else:
            placements = [
                {
                    "path": c.get("path"),
                    "runtime": c.get("runtime"),
                    "role": c.get("role"),
                    "content_hash": c.get("content_hash"),
                }
                for c in sorted(copies, key=lambda item: item.get("path", ""))
            ]
            skills.append({
                "skill_slug": slug,
                "source_path": None,
                "source_hash": None,
                "source_present": False,
                "targets": [],
                "placements": placements,
                "runtime_count": len({p["runtime"] for p in placements}),
                "copy_count": len(copies),
            })

    payload = {
        "summary": {
            "mode": mode,
            "canonical_source": source,
            "target_count": len(targets),
            "skill_count": len(skills),
            "source_missing_skills": sum(1 for s in skills if not s["source_present"]) if mode == "canonical-source" else 0,
            "runtime_count": len({item.get("runtime", "unknown") for item in items}),
        },
        "targets": [{"name": k, "path": v} for k, v in targets.items()],
        "skills": skills,
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
