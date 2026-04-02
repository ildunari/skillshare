#!/usr/bin/env python3
"""
Generate a freshness report from discovery data.
Flags stale skills, missing FEEDBACK.md, and obsolete model references.
Now handles all entity types (skills, agents, commands, rules).

Usage:
    python freshness_report.py DISCOVERY_JSON [--days 90] [--output FILE]
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


# NOTE: These patterns may flag historical references (e.g., "upgraded from
# Claude 3"). False positives are acceptable — the freshness report is a
# signal for human review, not an auto-removal trigger.
STALE_MODEL_PATTERNS = [
    r"claude[\s-]*3\.?5",
    r"claude[\s-]*3\b",
    r"opus[\s-]*4\.1",
    r"sonnet[\s-]*3",
    r"gpt[\s-]*4[\s-]*turbo",
    r"gpt[\s-]*4\b(?!\.)",  # gpt-4 but not gpt-4o or gpt-4.1
    r"gpt[\s-]*4o\b",       # gpt-4o (superseded by gpt-5.x)
    r"gemini[\s-]*1\.5",
    r"gemini[\s-]*2\.0",
]


def check_stale_models(filepath: str) -> tuple[list[str], bool]:
    """Scan file for references to obsolete model names.
    Returns (found_models, was_readable)."""
    try:
        content = Path(filepath).read_text(errors="replace").lower()
    except OSError:
        return [], False

    found = []
    for pattern in STALE_MODEL_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found.append(matches[0].strip())
    return found, True


def generate_report(discovery: dict, stale_days: int = 90) -> dict:
    """Produce freshness report from discovery data."""
    now = datetime.now(tz=timezone.utc)
    cutoff = now - timedelta(days=stale_days)

    items = discovery.get("skills", [])

    report = {
        "generated_at": now.isoformat(),
        "stale_threshold_days": stale_days,
        "total_items": len(items),
        "stale_count": 0,
        "no_feedback_count": 0,
        "stale_models_count": 0,
        "unreadable_count": 0,
        "by_entity_type": {},
        "skills": [],
    }

    # Per-entity-type counters
    type_stats = {}

    for item in sorted(items, key=lambda s: s.get("mtime", ""), reverse=True):
        mtime_str = item.get("mtime", "unknown")
        is_stale = False
        days_old = None
        entity_type = item.get("entity_type", "skill")

        if entity_type not in type_stats:
            type_stats[entity_type] = {"total": 0, "stale": 0, "no_feedback": 0, "stale_models": 0}
        type_stats[entity_type]["total"] += 1

        if mtime_str != "unknown":
            try:
                mtime = datetime.fromisoformat(mtime_str)
                days_old = (now - mtime).days
                is_stale = mtime < cutoff
            except (ValueError, TypeError):
                pass

        stale_models, was_readable = check_stale_models(item.get("path", ""))
        if not was_readable:
            report["unreadable_count"] += 1

        flags = []
        if is_stale:
            flags.append(f"stale ({days_old}d old)")
            report["stale_count"] += 1
            type_stats[entity_type]["stale"] += 1
        if not item.get("has_feedback", False) and entity_type == "skill":
            flags.append("no FEEDBACK.md")
            report["no_feedback_count"] += 1
            type_stats[entity_type]["no_feedback"] += 1
        if stale_models:
            flags.append(f"stale models: {', '.join(stale_models)}")
            report["stale_models_count"] += 1
            type_stats[entity_type]["stale_models"] += 1

        report["skills"].append({
            "name": item.get("name", ""),
            "directory": item.get("directory", ""),
            "entity_type": entity_type,
            "scope": item.get("scope", "global"),
            "agent_runtime": item.get("agent_runtime", "unknown"),
            "days_old": days_old,
            "has_feedback": item.get("has_feedback", False),
            "stale_models": stale_models,
            "flags": flags,
            "line_count": item.get("line_count", 0),
        })

    report["by_entity_type"] = type_stats

    return report


def main():
    parser = argparse.ArgumentParser(description="Skill freshness report")
    parser.add_argument("discovery_json", help="Path to discover_skills.py output")
    parser.add_argument("--days", type=int, default=90, help="Days threshold for staleness")
    parser.add_argument("--output", "-o", default=None, help="Output file")
    parser.add_argument("--flagged-only", action="store_true", help="Only show items with flags")
    args = parser.parse_args()

    with open(args.discovery_json) as f:
        discovery = json.load(f)

    report = generate_report(discovery, args.days)

    if args.flagged_only:
        report["skills"] = [s for s in report["skills"] if s["flags"]]

    print(f"Total: {report['total_items']} | Stale: {report['stale_count']} | "
          f"No FEEDBACK.md: {report['no_feedback_count']} | "
          f"Stale models: {report['stale_models_count']}", file=sys.stderr)

    for et, stats in sorted(report["by_entity_type"].items()):
        print(f"  {et}: {stats['total']} total, {stats['stale']} stale, "
              f"{stats['stale_models']} stale models", file=sys.stderr)

    json_str = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
