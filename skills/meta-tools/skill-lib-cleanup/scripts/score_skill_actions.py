#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict

from _shared import load_json, load_skill_blocklist, write_json


def main():
    parser = argparse.ArgumentParser(description="Score primary actions for skills using topology and drift data.")
    parser.add_argument("drift")
    parser.add_argument("duplicates")
    parser.add_argument("routing")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    drift_payload = load_json(args.drift)
    drift = drift_payload.get("rows", [])
    drift_summary = drift_payload.get("summary", {})
    dup_payload = load_json(args.duplicates)
    dup_clusters = dup_payload.get("duplicate_clusters", dup_payload.get("clusters", []))
    routing_payload = load_json(args.routing)
    routing = routing_payload.get("collisions", [])
    mode = drift_summary.get("mode", "canonical-source")
    drift_not_applicable = bool(drift_summary.get("not_applicable"))
    blocked_skills = load_skill_blocklist()

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

    # Broad-sweep mode can still produce action recommendations from duplicates
    # and routing collisions even when canonical-vs-install drift is not applicable.
    if drift_not_applicable:
        for slug in set(dup_slugs) | set(routing_slugs):
            by_skill.setdefault(slug, [])

    actions = []
    for slug, rows in sorted(by_skill.items()):
        statuses = {r["drift_status"] for r in rows}
        action = "KEEP"
        reason = "healthy or not enough evidence for change"
        confidence = "medium"
        is_blocked = slug in blocked_skills
        if not drift_not_applicable and "out-of-sync" in statuses:
            action = "SYNC FROM SOURCE"
            reason = "canonical source and installed copies differ"
            confidence = "high"
        elif not drift_not_applicable and "install-only" in statuses:
            action = "PROMOTE TO SOURCE"
            reason = "runtime install exists without a canonical source copy"
            confidence = "medium"
        elif not drift_not_applicable and "undistributed-source" in statuses:
            action = "PUSH TO TARGETS"
            reason = "canonical source exists but expected targets are missing installs"
            confidence = "high"
        if dup_slugs[slug] > 0 and action == "KEEP":
            action = "KEEP + REWRITE" if routing_slugs[slug] > 0 else "MERGE INTO"
            reason = "duplicate family detected among scanned skills"
            confidence = "medium"
        if routing_slugs[slug] > 0 and action == "KEEP":
            action = "FIX ROUTING"
            reason = "trigger overlap detected"
            confidence = "medium"
        if is_blocked:
            action = "KEEP"
            reason = "skill is listed in references/blocklist.md and should not be changed automatically"
            confidence = "high"
        actions.append({
            "skill_slug": slug,
            "action": action,
            "reason": reason,
            "confidence": confidence,
            "blocklisted": is_blocked,
            "duplicate_family_count": dup_slugs[slug],
            "routing_collision_count": routing_slugs[slug],
            "statuses": sorted(statuses),
        })

    payload = {
        "summary": {
            "skill_count": len(actions),
            "mode": mode,
            "drift_not_applicable": drift_not_applicable,
        },
        "actions": actions,
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
