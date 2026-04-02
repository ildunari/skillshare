#!/usr/bin/env python3
from __future__ import annotations

import argparse
from itertools import combinations

from _shared import jaccard_similarity, load_json, write_json


def main():
    parser = argparse.ArgumentParser(description="Detect routing collisions using extracted trigger lines.")
    parser.add_argument("capabilities")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    data = load_json(args.capabilities)
    skills = data.get("skills", [])
    collisions = []
    for left, right in combinations(skills, 2):
        score = jaccard_similarity(left.get("trigger_lines", []), right.get("trigger_lines", []))
        if score >= 0.25 and (left.get("runtime") == right.get("runtime") or left.get("role") == right.get("role")):
            collisions.append({
                "left": left["slug"],
                "right": right["slug"],
                "runtime_pair": [left.get("runtime"), right.get("runtime")],
                "score": round(score, 4),
                "left_path": left["path"],
                "right_path": right["path"],
            })
    payload = {"summary": {"collision_count": len(collisions)}, "collisions": sorted(collisions, key=lambda c: c["score"], reverse=True)}
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
