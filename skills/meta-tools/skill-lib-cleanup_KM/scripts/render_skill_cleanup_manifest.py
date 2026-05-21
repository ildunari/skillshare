#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser(description="Render a markdown skill-library cleanup manifest.")
    parser.add_argument("--topology", required=True)
    parser.add_argument("--drift", required=True)
    parser.add_argument("--actions", required=True)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    topo = load(args.topology)
    drift = load(args.drift)
    actions = load(args.actions)

    lines = []
    lines.append("# Skill Library Cleanup Manifest")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(f"- Canonical source: **{topo['summary']['canonical_source']}**")
    lines.append(f"- Skills seen: **{topo['summary']['skill_count']}**")
    lines.append(f"- Targets: **{topo['summary']['target_count']}**")
    lines.append(f"- In sync: **{drift['summary']['in_sync']}**")
    lines.append(f"- Out of sync: **{drift['summary']['out_of_sync']}**")
    lines.append(f"- Install only: **{drift['summary']['install_only']}**")
    lines.append(f"- Undistributed source: **{drift['summary']['undistributed_source']}**")
    lines.append("")
    lines.append("## Primary Actions")
    for row in actions.get('actions', [])[:20]:
        lines.append(f"- **{row['skill_slug']}** → {row['action']} ({row['confidence']}) — {row['reason']}")
    Path(args.output).write_text("\n".join(lines) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
