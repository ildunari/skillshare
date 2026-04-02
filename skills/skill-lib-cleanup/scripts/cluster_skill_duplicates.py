#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from _shared import load_json, write_json


def main():
    parser = argparse.ArgumentParser(description="Cluster exact duplicate skills by content hash.")
    parser.add_argument("discovery")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    data = load_json(args.discovery)
    items = [i for i in data.get("items", data.get("files", [])) if i.get("entity_type") == "skill" or str(i.get("path", "")).endswith("SKILL.md")]
    groups = defaultdict(list)
    for item in items:
        groups[item.get("content_hash")].append(item)
    clusters = []
    for content_hash, copies in groups.items():
        if len(copies) < 2:
            continue
        clusters.append({
            "content_hash": content_hash,
            "copy_count": len(copies),
            "skill_slugs": sorted({c.get("slug") or Path(c["path"]).parent.name for c in copies}),
            "paths": [c["path"] for c in sorted(copies, key=lambda x: x["path"])],
            "roles": sorted({c.get("role", "unknown") for c in copies}),
            "runtimes": sorted({c.get("runtime", "unknown") for c in copies}),
        })
    payload = {"summary": {"cluster_count": len(clusters)}, "clusters": sorted(clusters, key=lambda c: c["copy_count"], reverse=True)}
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
