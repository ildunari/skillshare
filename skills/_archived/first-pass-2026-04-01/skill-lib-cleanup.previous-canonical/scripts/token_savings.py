#!/usr/bin/env python3
"""
Estimate token savings from using scripts vs. having an LLM read everything.

Usage:
    python token_savings.py DISCOVERY_JSON [--output FILE]
"""

import argparse
import json
import sys
from datetime import datetime, timezone


# Rough token-per-line estimates (conservative)
TOKENS_PER_LINE = 4.2          # Average tokens per line of markdown/code
TOKENS_PER_JSON_ENTRY = 80     # Frontmatter parse output per skill
TOKENS_PER_HASH_COMPARE = 15   # Hash comparison reasoning per pair
TOKENS_PER_FRESHNESS_CHECK = 25 # Freshness reasoning per skill
LLM_OVERHEAD_MULTIPLIER = 1.4  # LLM reasoning overhead (chain-of-thought, formatting)

# Cost estimates (approximate, conservative)
INPUT_COST_PER_1K = 0.015      # $/1K input tokens (Opus-class)
OUTPUT_COST_PER_1K = 0.075     # $/1K output tokens


def estimate(discovery: dict) -> dict:
    items = discovery.get("skills", [])
    total_items = len(items)
    total_lines = sum(i.get("line_count", 0) for i in items)
    total_refs = sum(i.get("ref_count", 0) for i in items)
    total_scripts = sum(i.get("script_count", 0) for i in items)

    # Group by entity type
    skills = [i for i in items if i.get("entity_type", "skill") == "skill"]
    agents = [i for i in items if i.get("entity_type") == "agent"]
    others = [i for i in items if i.get("entity_type") not in ("skill", "agent", None)]

    # ── WITHOUT SCRIPTS (LLM reads everything) ──────────────────────────
    # Phase 0: LLM would need to run find/ls commands, read each dir
    without_discovery = total_items * 30  # ~30 tokens per discovery attempt (path, check, classify)

    # Phase 1: LLM reads every SKILL.md file
    without_inventory = int(total_lines * TOKENS_PER_LINE * LLM_OVERHEAD_MULTIPLIER)

    # Phase 2: LLM compares pairs for drift (n*(n-1)/2 but grouped by name)
    unique_names = len(set(i.get("directory", "") for i in items))
    avg_copies = total_items / max(unique_names, 1)
    pair_comparisons = int(unique_names * (avg_copies * (avg_copies - 1)) / 2)
    without_xdiff = pair_comparisons * TOKENS_PER_HASH_COMPARE * 8  # LLM has to read both files

    # Phase 5: LLM checks freshness by reading content and reasoning
    without_freshness = int(total_items * TOKENS_PER_FRESHNESS_CHECK * LLM_OVERHEAD_MULTIPLIER)

    without_total = without_discovery + without_inventory + without_xdiff + without_freshness

    # ── WITH SCRIPTS (deterministic) ─────────────────────────────────────
    # Phase 0: Script output JSON
    with_discovery = total_items * 12  # ~12 tokens per JSON entry in output

    # Phase 1: Script parses frontmatter, LLM reads JSON summary
    with_inventory = total_items * TOKENS_PER_JSON_ENTRY

    # Phase 2: Script does hash comparison, LLM reads drifted list
    drifted_count = len([i for i in items
                        if i.get("hash", "") != "error"])  # items with valid hashes
    with_xdiff = unique_names * 8  # ~8 tokens per group classification in JSON

    # Phase 5: Script flags issues, LLM reads flagged list
    with_freshness = total_items * 3  # ~3 tokens per entry in flagged-only output

    with_total = with_discovery + with_inventory + with_xdiff + with_freshness

    # ── SAVINGS ──────────────────────────────────────────────────────────
    savings_tokens = without_total - with_total
    savings_pct = (savings_tokens / without_total * 100) if without_total > 0 else 0

    savings_input_cost = (savings_tokens / 1000) * INPUT_COST_PER_1K
    total_without_cost = (without_total / 1000) * INPUT_COST_PER_1K

    return {
        "estimated_at": datetime.now(tz=timezone.utc).isoformat(),
        "total_items": total_items,
        "total_lines": total_lines,
        "total_skills": len(skills),
        "total_agents": len(agents),
        "unique_names": unique_names,
        "without_scripts": {
            "discovery_tokens": without_discovery,
            "inventory_tokens": without_inventory,
            "cross_location_tokens": without_xdiff,
            "freshness_tokens": without_freshness,
            "total_tokens": without_total,
            "estimated_cost_usd": round(total_without_cost, 2),
        },
        "with_scripts": {
            "discovery_tokens": with_discovery,
            "inventory_tokens": with_inventory,
            "cross_location_tokens": with_xdiff,
            "freshness_tokens": with_freshness,
            "total_tokens": with_total,
            "estimated_cost_usd": round((with_total / 1000) * INPUT_COST_PER_1K, 2),
        },
        "savings": {
            "tokens_saved": savings_tokens,
            "percentage": round(savings_pct, 1),
            "cost_saved_usd": round(savings_input_cost, 2),
        },
        "per_phase": [
            {
                "phase": "Discovery",
                "without": without_discovery,
                "with": with_discovery,
                "saved": without_discovery - with_discovery,
            },
            {
                "phase": "Inventory",
                "without": without_inventory,
                "with": with_inventory,
                "saved": without_inventory - with_inventory,
            },
            {
                "phase": "Cross-Location Diff",
                "without": without_xdiff,
                "with": with_xdiff,
                "saved": without_xdiff - with_xdiff,
            },
            {
                "phase": "Freshness Check",
                "without": without_freshness,
                "with": with_freshness,
                "saved": without_freshness - with_freshness,
            },
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Estimate token savings from scripts")
    parser.add_argument("discovery_json", help="Path to discover_skills.py output")
    parser.add_argument("--output", "-o", default=None, help="Output file")
    args = parser.parse_args()

    with open(args.discovery_json) as f:
        discovery = json.load(f)

    result = estimate(discovery)

    s = result["savings"]
    w = result["without_scripts"]
    print(f"Without scripts: {w['total_tokens']:,} tokens (~${w['estimated_cost_usd']})", file=sys.stderr)
    print(f"With scripts:    {result['with_scripts']['total_tokens']:,} tokens (~${result['with_scripts']['estimated_cost_usd']})", file=sys.stderr)
    print(f"Savings:         {s['tokens_saved']:,} tokens ({s['percentage']}%) ~${s['cost_saved_usd']}", file=sys.stderr)

    json_str = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
