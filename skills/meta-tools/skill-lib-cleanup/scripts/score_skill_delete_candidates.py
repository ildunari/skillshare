#!/usr/bin/env python3
from __future__ import annotations

import argparse
from _shared import classify_role, load_json, load_skill_blocklist, normalized_discovery_items, write_json


def main():
    parser = argparse.ArgumentParser(description="Score delete/archive candidates in a skill library.")
    parser.add_argument("discovery")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    data = load_json(args.discovery)
    items = normalized_discovery_items(data)
    blocked_skills = load_skill_blocklist()
    rows = []
    for item in items:
        role = item.get("role") or classify_role(item.get("path", ""))
        slug = item.get("slug")
        score = 0
        reasons = []
        if role == "backup":
            score += 85; reasons.append("backup-copy")
        if role == "archive":
            score += 80; reasons.append("archive-copy")
        if role == "mirror":
            score += 65; reasons.append("mirror-copy")
        if role == "generated-artifact":
            score += 90; reasons.append("generated-artifact")
        if role == "canonical-source":
            score -= 60; reasons.append("canonical-source")
        if slug in blocked_skills:
            score = min(score, 0)
            reasons.append("blocklisted")
        bucket = "review-required"
        if score >= 85:
            bucket = "delete-now"
        elif score >= 60:
            bucket = "probably-delete"
        elif score >= 35:
            bucket = "archive-first"
        if slug in blocked_skills:
            bucket = "protected"
        rows.append({
            "path": item.get("path"),
            "slug": slug,
            "runtime": item.get("runtime"),
            "role": role,
            "delete_score": score,
            "bucket": bucket,
            "blocklisted": slug in blocked_skills,
            "reasons": reasons,
        })
    payload = {
        "summary": {
            "delete_now": sum(1 for r in rows if r["bucket"] == "delete-now"),
            "probably_delete": sum(1 for r in rows if r["bucket"] == "probably-delete"),
            "archive_first": sum(1 for r in rows if r["bucket"] == "archive-first"),
            "protected": sum(1 for r in rows if r["bucket"] == "protected"),
        },
        "candidates": sorted(rows, key=lambda r: r["delete_score"], reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
