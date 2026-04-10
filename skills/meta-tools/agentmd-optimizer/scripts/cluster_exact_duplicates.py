#!/usr/bin/env python3
from __future__ import annotations

import argparse
from _shared import cluster_by_hash, load_inventory, write_json


def main():
    parser = argparse.ArgumentParser(description="Cluster exact duplicate instruction files by content hash.")
    parser.add_argument("inventory")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    grouped = cluster_by_hash(files)
    clusters = []
    for content_hash, items in grouped.items():
        if len(items) < 2:
            continue
        items = sorted(items, key=lambda x: x["path"])
        clusters.append({
            "content_hash": content_hash,
            "copy_count": len(items),
            "line_count": items[0].get("line_count", 0),
            "token_estimate_each": items[0].get("token_estimate", 0),
            "total_cluster_tokens": sum(i.get("token_estimate", 0) for i in items),
            "paths": [i["path"] for i in items],
            "path_kinds": sorted({i.get("path_kind", "unknown") for i in items}),
            "runtimes": sorted({i.get("runtime", "unknown") for i in items}),
        })
    payload = {
        "summary": {
            "cluster_count": len(clusters),
            "duplicate_token_waste": sum(max(0, c["total_cluster_tokens"] - c["token_estimate_each"]) for c in clusters),
        },
        "clusters": sorted(clusters, key=lambda c: (c["total_cluster_tokens"], c["copy_count"]), reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
