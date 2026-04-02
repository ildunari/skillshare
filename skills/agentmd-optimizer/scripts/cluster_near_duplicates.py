#!/usr/bin/env python3
from __future__ import annotations

import argparse
from itertools import combinations

from _shared import headings, jaccard_similarity, load_inventory, normalize_text, safe_read_text, sequence_similarity, write_json


def similarity_score(a_text: str, b_text: str) -> tuple[float, float, float]:
    a_norm = normalize_text(a_text)
    b_norm = normalize_text(b_text)
    seq = sequence_similarity(a_norm, b_norm)
    head = jaccard_similarity(headings(a_text), headings(b_text))
    lines = jaccard_similarity(a_norm.splitlines(), b_norm.splitlines())
    return seq, head, lines


def main():
    parser = argparse.ArgumentParser(description="Cluster near-duplicate instruction files.")
    parser.add_argument("inventory")
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--min-score", type=float, default=0.78)
    parser.add_argument("--max-files", type=int, default=120)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    candidates = [f for f in files if f.get("line_count", 0) > 0][: args.max_files]
    texts = {f["path"]: safe_read_text(f["path"]) for f in candidates}
    pairs = []
    for left, right in combinations(candidates, 2):
        if left.get("content_hash") == right.get("content_hash"):
            continue
        seq, head, lines = similarity_score(texts[left["path"]], texts[right["path"]])
        score = round((seq * 0.6) + (head * 0.2) + (lines * 0.2), 4)
        if score >= args.min_score:
            pairs.append({
                "left": left["path"],
                "right": right["path"],
                "score": score,
                "sequence_similarity": round(seq, 4),
                "heading_similarity": round(head, 4),
                "line_jaccard": round(lines, 4),
                "suggestion": "merge-or-wrap" if score >= 0.9 else "manual-review",
            })
    payload = {
        "summary": {
            "pair_count": len(pairs),
            "threshold": args.min_score,
        },
        "pairs": sorted(pairs, key=lambda p: p["score"], reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
