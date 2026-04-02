#!/usr/bin/env python3
from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

from _shared import headings, jaccard_similarity, load_json, normalize_text, safe_read_text, sequence_similarity, write_json


def main():
    parser = argparse.ArgumentParser(description="Find near-duplicate skills by content similarity.")
    parser.add_argument("discovery")
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--min-score", type=float, default=0.8)
    parser.add_argument("--max-files", type=int, default=80)
    args = parser.parse_args()

    data = load_json(args.discovery)
    items = [i for i in data.get("items", data.get("files", [])) if i.get("entity_type") == "skill" or str(i.get("path", "")).endswith("SKILL.md")][:args.max_files]
    texts = {i["path"]: safe_read_text(i["path"]) for i in items}
    pairs = []
    for left, right in combinations(items, 2):
        if left.get("content_hash") == right.get("content_hash"):
            continue
        ltxt = normalize_text(texts[left["path"]])
        rtxt = normalize_text(texts[right["path"]])
        seq = sequence_similarity(ltxt, rtxt)
        head = jaccard_similarity(headings(texts[left["path"]]), headings(texts[right["path"]]))
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
    payload = {"summary": {"pair_count": len(pairs)}, "pairs": sorted(pairs, key=lambda p: p["score"], reverse=True)}
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
