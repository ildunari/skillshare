#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from _shared import load_json, write_json


def main():
    parser = argparse.ArgumentParser(description="Build a skill distribution matrix from canonical-vs-install drift data.")
    parser.add_argument("drift")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    rows = load_json(args.drift).get("rows", [])
    matrix = defaultdict(dict)
    targets = []
    for row in rows:
        matrix[row["skill_slug"]][row["target"]] = row["drift_status"]
        if row["target"] not in targets:
            targets.append(row["target"])
    payload = {
        "summary": {"skill_count": len(matrix), "target_count": len(targets)},
        "targets": targets,
        "rows": [dict(skill_slug=slug, **matrix[slug]) for slug in sorted(matrix)],
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
