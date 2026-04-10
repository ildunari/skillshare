#!/usr/bin/env python3
"""
Compare skills and agents across locations. Detects drift, orphans,
symlink chains, and renamed duplicates. Now handles entity types
and separates global from project-local analysis.

Usage:
    python cross_location_diff.py DISCOVERY_JSON [--output FILE]

Input: JSON from discover_skills.py
Output: Cross-location comparison report as JSON.
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone


def classify_group(entries: list[dict]) -> dict:
    """Classify a group of same-named items across locations."""
    if len(entries) == 1:
        return {
            "status": "singleton",
            "detail": f"Only in {entries[0]['agent_runtime']}",
            "locations": [e["agent_runtime"] for e in entries],
            "entries": entries,
        }

    # Check if all are symlinks to the same canonical path
    canonical_paths = set(e["canonical_path"] for e in entries)
    if len(canonical_paths) == 1:
        return {
            "status": "symlinked",
            "detail": f"All {len(entries)} copies point to same file",
            "canonical_path": entries[0]["canonical_path"],
            "locations": [e["agent_runtime"] for e in entries],
            "entries": entries,
        }

    # Check content hashes
    hashes = set(e["hash"] for e in entries if e.get("hash") != "error")
    if len(hashes) <= 1:
        return {
            "status": "identical",
            "detail": f"{len(entries)} independent copies, same content",
            "locations": [e["agent_runtime"] for e in entries],
            "entries": entries,
        }

    # Content differs — find newest
    dated = sorted(
        entries,
        key=lambda e: e.get("mtime", "") if e.get("mtime", "") != "unknown" else "",
        reverse=True,
    )
    newest = dated[0]
    stale = dated[1:]

    hash_groups = defaultdict(list)
    for e in entries:
        hash_groups[e["hash"]].append(e["agent_runtime"])

    return {
        "status": "drifted",
        "detail": f"{len(hashes)} different versions across {len(entries)} locations",
        "newest": {
            "location": newest["agent_runtime"],
            "mtime": newest["mtime"],
            "hash": newest["hash"],
        },
        "stale_copies": [
            {
                "location": e["agent_runtime"],
                "mtime": e["mtime"],
                "hash": e["hash"],
            }
            for e in stale if e["hash"] != newest["hash"]
        ],
        "hash_groups": dict(hash_groups),
        "locations": [e["agent_runtime"] for e in entries],
        "entries": entries,
    }


def analyze(discovery: dict) -> dict:
    """Group items by name and entity type, compare across locations."""
    all_items = discovery.get("skills", [])

    # Separate global from project-local
    global_items = [i for i in all_items if i.get("scope", "global") == "global"]
    local_items = [i for i in all_items if i.get("scope", "global") == "project-local"]

    # ── Global analysis: group by (directory, entity_type) ──
    by_key = defaultdict(list)
    for item in global_items:
        key = item["directory"]
        by_key[key].append(item)

    results = {
        "analyzed_at": datetime.now(tz=timezone.utc).isoformat(),
        "total_items": len(all_items),
        "total_global": len(global_items),
        "total_project_local": len(local_items),
        "total_unique_skills": len(by_key),
        "summary": {
            "symlinked": 0, "identical": 0, "drifted": 0, "singleton": 0,
            "renamed_duplicate_groups": 0,
        },
        "drifted": [],
        "skills": {},
    }

    for name, entries in sorted(by_key.items()):
        group = classify_group(entries)
        status = group["status"]
        results["summary"][status] = results["summary"].get(status, 0) + 1
        results["skills"][name] = {
            "status": status,
            "detail": group["detail"],
            "location_count": len(entries),
            "locations": group["locations"],
            "entity_type": entries[0].get("entity_type", "skill"),
        }
        if status == "drifted":
            results["drifted"].append({
                "name": name,
                "entity_type": entries[0].get("entity_type", "skill"),
                **{k: v for k, v in group.items() if k != "entries"},
            })

    # ── Content-based dedup: find different names with identical hashes ──
    hash_to_items = defaultdict(list)
    for item in global_items:
        h = item.get("hash", "")
        if h and h != "error":
            hash_to_items[h].append(item)

    renamed_dupes = []
    for h, entries in hash_to_items.items():
        names = set(e["directory"] for e in entries)
        if len(names) > 1:
            name_locations = defaultdict(list)
            for e in entries:
                name_locations[e["directory"]].append(e["agent_runtime"])
            renamed_dupes.append({
                "hash": h,
                "names": sorted(names),
                "name_locations": {k: sorted(v) for k, v in name_locations.items()},
                "entity_type": entries[0].get("entity_type", "skill"),
                "detail": (f"{len(names)} different names share identical "
                           f"content (hash {h})"),
            })

    results["renamed_duplicates"] = renamed_dupes
    results["summary"]["renamed_duplicate_groups"] = len(renamed_dupes)

    # ── Project-local summary ──
    if local_items:
        by_project = defaultdict(list)
        for item in local_items:
            pr = item.get("project_root", "unknown")
            by_project[pr].append(item)

        results["project_local"] = {
            "total": len(local_items),
            "projects": {
                pr: {
                    "count": len(items),
                    "items": [
                        {
                            "name": i["name"],
                            "entity_type": i.get("entity_type", "skill"),
                            "agent_runtime": i.get("agent_runtime", "unknown"),
                        }
                        for i in items
                    ],
                }
                for pr, items in sorted(by_project.items())
            },
        }

    # ── Per-entity-type breakdown ──
    type_summary = defaultdict(lambda: {"total": 0, "drifted": 0, "singleton": 0})
    for item in global_items:
        et = item.get("entity_type", "skill")
        type_summary[et]["total"] += 1
    for d in results["drifted"]:
        et = d.get("entity_type", "skill")
        type_summary[et]["drifted"] += 1
    for name, info in results["skills"].items():
        if info["status"] == "singleton":
            et = info.get("entity_type", "skill")
            type_summary[et]["singleton"] += 1

    results["by_entity_type"] = dict(type_summary)

    return results


def main():
    parser = argparse.ArgumentParser(description="Cross-location skill comparison")
    parser.add_argument("discovery_json", help="Path to discover_skills.py output")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.discovery_json) as f:
        discovery = json.load(f)

    results = analyze(discovery)

    s = results["summary"]
    print(f"Global items: {results['total_global']} | "
          f"Project-local: {results['total_project_local']}", file=sys.stderr)
    print(f"Unique (global): {results['total_unique_skills']}", file=sys.stderr)
    print(f"  Symlinked: {s['symlinked']}, Identical: {s['identical']}, "
          f"Drifted: {s['drifted']}, Singleton: {s['singleton']}", file=sys.stderr)
    if s.get("renamed_duplicate_groups", 0) > 0:
        print(f"  Renamed duplicates: {s['renamed_duplicate_groups']} groups", file=sys.stderr)

    json_str = json.dumps(results, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
