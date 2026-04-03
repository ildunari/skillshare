#!/usr/bin/env python3
from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

from _shared import (
    headings,
    jaccard_similarity,
    load_json,
    normalize_text,
    normalized_discovery_items,
    safe_read_text,
    sequence_similarity,
    write_json,
)


def slug_tokens(item: dict) -> set[str]:
    slug = str(item.get("slug") or Path(item["path"]).parent.name).lower()
    return {part for part in slug.replace("_", "-").split("-") if part}


def likely_candidate(left: dict, right: dict, left_text: str, right_text: str) -> bool:
    left_tokens = slug_tokens(left)
    right_tokens = slug_tokens(right)
    if left_tokens & right_tokens:
        return True
    head = jaccard_similarity(headings(left_text), headings(right_text))
    return head >= 0.35


def main():
    parser = argparse.ArgumentParser(description="Find near-duplicate skills by content similarity.")
    parser.add_argument("discovery")
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--min-score", type=float, default=0.8)
    parser.add_argument("--max-files", type=int, default=80)
    parser.add_argument("--max-comparisons", type=int, default=2500)
    args = parser.parse_args()

    data = load_json(args.discovery)
    items = [
        i
        for i in normalized_discovery_items(data)
        if i.get("entity_type") == "skill" or str(i.get("path", "")).endswith("SKILL.md")
    ][:args.max_files]
    texts = {i["path"]: safe_read_text(i["path"]) for i in items}
    pairs = []
    comparisons = 0
    skipped_prefilter = 0
    for left, right in combinations(items, 2):
        if comparisons >= args.max_comparisons:
            break
        if left.get("content_hash") == right.get("content_hash"):
            continue
        raw_left = texts[left["path"]]
        raw_right = texts[right["path"]]
        if not likely_candidate(left, right, raw_left, raw_right):
            skipped_prefilter += 1
            continue
        comparisons += 1
        ltxt = normalize_text(raw_left)
        rtxt = normalize_text(raw_right)
        seq = sequence_similarity(ltxt, rtxt)
        head = jaccard_similarity(headings(raw_left), headings(raw_right))
        score = round(seq * 0.7 + head * 0.3, 4)
        if score >= args.min_score:
            pairs.append({
                "left": left["path"],
                "right": right["path"],
                "left_slug": left.get("slug") or Path(left["path"]).parent.name,
                "right_slug": right.get("slug") or Path(right["path"]).parent.name,
                "score": score,
                "suggestion": "merge-candidate" if score >= 0.9 else "review",
            })
    payload = {
        "summary": {
            "pair_count": len(pairs),
            "files_considered": len(items),
            "comparisons_run": comparisons,
            "prefilter_skipped": skipped_prefilter,
            "comparison_cap_hit": comparisons >= args.max_comparisons,
        },
        "pairs": sorted(pairs, key=lambda p: p["score"], reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
