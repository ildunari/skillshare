#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser(description="Render Mermaid-ready visual snippets from analysis outputs.")
    parser.add_argument("--load-stacks")
    parser.add_argument("--exact-clusters")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    sections = []
    if args.load_stacks:
        data = load(args.load_stacks)
        top = data.get("stacks", [])[:5]
        for idx, stack in enumerate(top, start=1):
            lines = ["graph TD", f"    ROOT{idx}[\"{stack['project_root']}\"]"]
            prev = f"ROOT{idx}"
            for j, path in enumerate(stack["stack_files"], start=1):
                node = f"S{idx}_{j}"
                label = path.replace('"', "'")
                lines.append(f"    {prev} --> {node}[\"{label}\"]")
                prev = node
            sections.append({"type": "load-stack", "title": f"{stack['runtime']} — {stack['project_root']}", "mermaid": "\n".join(lines)})
    if args.exact_clusters:
        data = load(args.exact_clusters)
        top = data.get("clusters", [])[:5]
        for idx, cluster in enumerate(top, start=1):
            lines = ["graph TD", f"    C{idx}[\"hash {cluster['content_hash']}\"]"]
            for j, path in enumerate(cluster["paths"], start=1):
                node = f"P{idx}_{j}"
                label = path.replace('"', "'")
                lines.append(f"    C{idx} --> {node}[\"{label}\"]")
            sections.append({"type": "duplicate-cluster", "title": f"Exact cluster {cluster['content_hash']}", "mermaid": "\n".join(lines)})
    payload = {"sections": sections}
    Path(args.output).write_text(json.dumps(payload, indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
