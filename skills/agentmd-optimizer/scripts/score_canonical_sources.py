#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from _shared import classify_path_kind, load_inventory, write_json


def score(item: dict) -> tuple[int, list[str]]:
    s = 0
    reasons = []
    path = item["path"]
    kind = item.get("path_kind") or classify_path_kind(path)
    if kind == "project":
        s += 30; reasons.append("project-path")
    if kind == "skill-install":
        s += 12; reasons.append("skill-install-path")
    if kind == "mirror":
        s -= 20; reasons.append("mirror-path")
    if kind == "archive":
        s -= 25; reasons.append("archive-path")
    if kind == "cache":
        s -= 30; reasons.append("cache-path")
    if kind == "vendor":
        s -= 35; reasons.append("vendor-path")
    if item.get("scope") == "project-local":
        s += 10; reasons.append("project-local-scope")
    if item.get("project_root"):
        s += 8; reasons.append("inside-detected-project")
    if item.get("file_exists"):
        s += 5; reasons.append("exists-now")
    if "/.git/" in path:
        s -= 50; reasons.append("git-internal")
    return s, reasons


def main():
    parser = argparse.ArgumentParser(description="Score likely canonical sources.")
    parser.add_argument("inventory")
    parser.add_argument("exact_clusters")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    file_map = {f["path"]: f for f in files}
    clusters = __import__('json').loads(Path(args.exact_clusters).read_text())["clusters"]
    scored_clusters = []
    for cluster in clusters:
        scored = []
        for path in cluster["paths"]:
            item = file_map[path]
            s, reasons = score(item)
            scored.append({"path": path, "score": s, "reasons": reasons, "path_kind": item.get("path_kind")})
        scored.sort(key=lambda x: x["score"], reverse=True)
        best = scored[0] if scored else None
        scored_clusters.append({
            "content_hash": cluster["content_hash"],
            "copy_count": cluster["copy_count"],
            "canonical_candidate": best,
            "copies": scored,
            "confidence": "high" if best and (len(scored) == 1 or best["score"] - scored[min(1, len(scored)-1)]["score"] >= 15) else "medium",
        })
    payload = {"summary": {"cluster_count": len(scored_clusters)}, "clusters": scored_clusters}
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
