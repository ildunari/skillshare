#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _shared import classify_path_kind, load_inventory, write_json


def delete_score(item: dict) -> tuple[int, str, list[str]]:
    score = 0
    reasons = []
    kind = item.get("path_kind") or classify_path_kind(item["path"])
    if kind == "vendor":
        score += 90; reasons.append("vendor-path")
    if kind == "cache":
        score += 85; reasons.append("cache-path")
    if kind == "archive":
        score += 80; reasons.append("archive-path")
    if kind == "mirror":
        score += 65; reasons.append("mirror-path")
    if item.get("file_exists") is False:
        score += 95; reasons.append("already-missing")
    if item.get("scope") == "global" and kind == "project":
        score -= 20; reasons.append("global-file")
    if item.get("project_root"):
        score -= 10; reasons.append("in-project-root")
    bucket = "review-required"
    if score >= 85:
        bucket = "delete-now"
    elif score >= 60:
        bucket = "probably-delete"
    elif score >= 35:
        bucket = "archive-first"
    return score, bucket, reasons


def main():
    parser = argparse.ArgumentParser(description="Score delete candidates.")
    parser.add_argument("inventory")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    rows = []
    for item in files:
        score, bucket, reasons = delete_score(item)
        rows.append({
            "path": item["path"],
            "runtime": item.get("runtime"),
            "scope": item.get("scope"),
            "path_kind": item.get("path_kind"),
            "delete_score": score,
            "bucket": bucket,
            "reasons": reasons,
        })
    payload = {
        "summary": {
            "delete_now": sum(1 for r in rows if r["bucket"] == "delete-now"),
            "probably_delete": sum(1 for r in rows if r["bucket"] == "probably-delete"),
            "archive_first": sum(1 for r in rows if r["bucket"] == "archive-first"),
        },
        "candidates": sorted(rows, key=lambda r: r["delete_score"], reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
