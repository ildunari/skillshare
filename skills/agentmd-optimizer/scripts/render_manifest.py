#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser(description="Render a markdown manifest from analysis outputs.")
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--load-stacks", required=True)
    parser.add_argument("--exact-clusters", required=True)
    parser.add_argument("--delete-candidates", required=True)
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    inv = load(args.inventory)
    stacks = load(args.load_stacks)
    exact = load(args.exact_clusters)
    deletes = load(args.delete_candidates)

    lines = []
    lines.append("# Token-Saving Manifest")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(f"- Files discovered: **{inv['summary']['total_files']}**")
    lines.append(f"- Estimated tokens on disk: **{inv['summary']['total_token_estimate']:,}**")
    lines.append(f"- Exact duplicate clusters: **{exact['summary']['cluster_count']}**")
    lines.append(f"- Simulated high-risk session stacks: **{stacks['summary']['high_risk_stacks']}**")
    lines.append(f"- High-confidence delete-now candidates: **{deletes['summary']['delete_now']}**")
    lines.append("")
    lines.append("## Highest-Risk Session Stacks")
    for stack in stacks.get('stacks', [])[:10]:
        lines.append(f"- **{stack['runtime']}** · `{stack['project_root']}` · {stack['total_tokens']} tokens · {stack['estimated_directives']} directives · risk={stack['risk']}")
    lines.append("")
    lines.append("## Largest Exact Duplicate Clusters")
    for cluster in exact.get('clusters', [])[:10]:
        lines.append(f"- hash `{cluster['content_hash']}` · {cluster['copy_count']} copies · {cluster['total_cluster_tokens']} total tokens")
    lines.append("")
    lines.append("## Top Delete Candidates")
    for row in deletes.get('candidates', [])[:15]:
        lines.append(f"- **{row['bucket']}** · {row['delete_score']} · `{row['path']}`")
    Path(args.output).write_text("\n".join(lines) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
