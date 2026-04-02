#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser(description="Render Mermaid-ready visuals for skill library cleanup outputs.")
    parser.add_argument("--topology", required=True)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    topo = load(args.topology)
    sections = []
    for idx, skill in enumerate(topo.get('skills', [])[:8], start=1):
        lines = ["graph TD", f"    SRC{idx}[\"{skill['skill_slug']} source\"]"]
        for j, target in enumerate(skill.get('targets', []), start=1):
            node = f"T{idx}_{j}"
            label = f"{target['target']}\\n{target['status']}"
            lines.append(f"    SRC{idx} --> {node}[\"{label}\"]")
        sections.append({"type": "skill-topology", "title": skill['skill_slug'], "mermaid": "\n".join(lines)})
    Path(args.output).write_text(json.dumps({"sections": sections}, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
