#!/usr/bin/env python3
from __future__ import annotations

import argparse
from itertools import combinations

from _shared import jaccard_similarity, load_json, write_json


def normalized_trigger_lines(skill: dict) -> set[str]:
    lines = []
    for line in skill.get("trigger_lines", []):
        normalized = " ".join(str(line).lower().split())
        if normalized:
            lines.append(normalized)
    return set(lines)


def main():
    parser = argparse.ArgumentParser(description="Detect routing collisions using extracted trigger lines.")
    parser.add_argument("capabilities")
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--min-score", type=float, default=0.25)
    parser.add_argument("--max-collisions", type=int, default=500)
    args = parser.parse_args()

    data = load_json(args.capabilities)
    skills = data.get("skills", [])
    collisions = []
    considered = 0
    for left, right in combinations(skills, 2):
        considered += 1
        left_lines = normalized_trigger_lines(left)
        right_lines = normalized_trigger_lines(right)
        score = jaccard_similarity(left_lines, right_lines)
        if score >= args.min_score and (left.get("runtime") == right.get("runtime") or left.get("role") == right.get("role")):
            collisions.append({
                "left": left["slug"],
                "right": right["slug"],
                "runtime_pair": [left.get("runtime"), right.get("runtime")],
                "role_pair": [left.get("role"), right.get("role")],
                "score": round(score, 4),
                "shared_trigger_count": len(left_lines & right_lines),
                "shared_triggers": sorted(left_lines & right_lines)[:5],
                "left_path": left["path"],
                "right_path": right["path"],
            })
    collisions = sorted(
        collisions,
        key=lambda c: (c["score"], c["shared_trigger_count"], c["left"], c["right"]),
        reverse=True,
    )
    payload = {
        "summary": {
            "collision_count": len(collisions),
            "considered_pairs": considered,
            "returned_collisions": min(len(collisions), args.max_collisions),
            "truncated": len(collisions) > args.max_collisions,
        },
        "collisions": collisions[: args.max_collisions],
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
