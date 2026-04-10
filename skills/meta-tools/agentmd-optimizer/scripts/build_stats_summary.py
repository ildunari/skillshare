#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from statistics import mean

from _shared import bucket_counts, load_inventory, top_level_bucket, write_json


def main():
    parser = argparse.ArgumentParser(description="Build summary stats for an instruction inventory.")
    parser.add_argument("inventory")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    by_runtime = defaultdict(lambda: {"file_count": 0, "token_total": 0, "max_tokens": 0})
    by_bucket = defaultdict(lambda: {"file_count": 0, "token_total": 0, "max_tokens": 0})
    per_file = []
    for item in files:
        tok = item.get("token_estimate", 0)
        rt = item.get("runtime", "unknown")
        b = top_level_bucket(item["path"])
        by_runtime[rt]["file_count"] += 1
        by_runtime[rt]["token_total"] += tok
        by_runtime[rt]["max_tokens"] = max(by_runtime[rt]["max_tokens"], tok)
        by_bucket[b]["file_count"] += 1
        by_bucket[b]["token_total"] += tok
        by_bucket[b]["max_tokens"] = max(by_bucket[b]["max_tokens"], tok)
        per_file.append({
            "path": item["path"],
            "runtime": rt,
            "scope": item.get("scope"),
            "path_kind": item.get("path_kind"),
            "tokens": tok,
            "lines": item.get("line_count", 0),
        })
    payload = {
        "summary": {
            "total_files": len(files),
            "total_tokens": sum(f["tokens"] for f in per_file),
            "avg_tokens_per_file": round(mean([f["tokens"] for f in per_file]), 2) if per_file else 0,
        },
        "by_runtime": {k: v for k, v in sorted(by_runtime.items(), key=lambda kv: kv[1]["token_total"], reverse=True)},
        "by_top_level_bucket": {k: v for k, v in sorted(by_bucket.items(), key=lambda kv: kv[1]["token_total"], reverse=True)},
        "largest_files": sorted(per_file, key=lambda f: f["tokens"], reverse=True)[:25],
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
