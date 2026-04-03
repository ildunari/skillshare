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
    parser.add_argument("--max-skills", type=int, default=8)
    args = parser.parse_args()

    topo = load(args.topology)
    summary = topo.get("summary", {})
    sections = []
    sections.append(
        {
            "type": "summary",
            "title": "Audit Mode",
            "data": {
                "mode": summary.get("mode", "unknown"),
                "canonical_source": summary.get("canonical_source"),
                "target_count": summary.get("target_count", 0),
                "skill_count": summary.get("skill_count", 0),
                "runtime_count": summary.get("runtime_count", 0),
            },
        }
    )
    mode = topo.get("summary", {}).get("mode", "canonical-source")
    for idx, skill in enumerate(topo.get('skills', [])[: args.max_skills], start=1):
        if mode == "canonical-source":
            lines = ["graph TD", f"    SRC{idx}[\"{skill['skill_slug']} source\"]"]
            for j, target in enumerate(skill.get('targets', []), start=1):
                node = f"T{idx}_{j}"
                label = f"{target['target']}\\n{target['status']}"
                lines.append(f"    SRC{idx} --> {node}[\"{label}\"]")
            mermaid = "\n".join(lines)
        else:
            lines = ["graph TD", f"    SK{idx}[\"{skill['skill_slug']}\"]"]
            for j, placement in enumerate(skill.get("placements", [])[:6], start=1):
                node = f"P{idx}_{j}"
                label = f"{placement.get('runtime', 'unknown')}\\n{placement.get('role', 'other')}"
                lines.append(f"    SK{idx} --> {node}[\"{label}\"]")
            mermaid = "\n".join(lines)
        sections.append({"type": "skill-topology", "title": skill['skill_slug'], "mermaid": mermaid})
    Path(args.output).write_text(json.dumps({"sections": sections}, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
