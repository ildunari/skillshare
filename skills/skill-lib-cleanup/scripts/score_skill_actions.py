#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict

from _shared import load_json, write_json


def main():
    parser = argparse.ArgumentParser(description="Score primary actions for skills using topology and drift data.")
    parser.add_argument("drift")
    parser.add_argument("duplicates")
    parser.add_argument("routing")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    drift = load_json(args.drift).get("rows", [])
    dup_clusters = load_json(args.duplicates).get("clusters", [])
    routing = load_json(args.routing).get("collisions", [])

    dup_slugs = defaultdict(int)
    for c in dup_clusters:
        for slug in c.get("skill_slugs", []):
            dup_slugs[slug] += 1
    routing_slugs = defaultdict(int)
    for c in routing:
        routing_slugs[c["left"]] += 1
        routing_slugs[c["right"]] += 1

    by_skill = defaultdict(list)
    for row in drift:
        by_skill[row["skill_slug"]].append(row)

    actions = []
    for slug, rows in sorted(by_skill.items()):
        statuses = {r["drift_status"] for r in rows}
        action = "KEEP"
        reason = "healthy or not enough evidence for change"
        confidence = "medium"
        if "out-of-sync" in statuses:
            action = "SYNC FROM SOURCE"
            reason = "canonical source and installed copies differ"
            confidence = "high"
        elif "install-only" in statuses:
            action = "PROMOTE TO SOURCE"
            reason = "runtime install exists without a canonical source copy"
            confidence = "medium"
        elif "undistributed-source" in statuses:
            action = "PUSH TO TARGETS"
            reason = "canonical source exists but expected targets are missing installs"
            confidence = "high"
        if dup_slugs[slug] > 0 and action == "KEEP":
            action = "MERGE INTO REVIEW GROUP"
            reason = "exact duplicate family detected"
            confidence = "medium"
        if routing_slugs[slug] > 0 and action == "KEEP":
            action = "FIX ROUTING"
            reason = "trigger overlap detected"
            confidence = "medium"
        actions.append({
            "skill_slug": slug,
            "action": action,
            "reason": reason,
            "confidence": confidence,
            "duplicate_family_count": dup_slugs[slug],
            "routing_collision_count": routing_slugs[slug],
            "statuses": sorted(statuses),
        })

    payload = {"summary": {"skill_count": len(actions)}, "actions": actions}
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
