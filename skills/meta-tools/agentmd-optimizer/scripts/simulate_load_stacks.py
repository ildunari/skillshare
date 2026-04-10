#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from _shared import estimate_directive_count, load_inventory, safe_read_text, write_json

RUNTIME_FILENAMES = {
    "claude-code": {"CLAUDE.md", "MEMORY.md"},
    "codex-cli": {"AGENTS.md"},
    "gemini-cli": {"GEMINI.md"},
    "cursor": {".mdc", "CLAUDE.md", "AGENTS.md"},
}
GLOBAL_PREFIXES = [
    str(Path.home() / ".claude"),
    str(Path.home() / ".codex"),
    str(Path.home() / ".gemini"),
    str(Path.home() / ".cursor"),
    str(Path.home() / ".factory"),
    str(Path.home() / ".kiro"),
    str(Path.home() / ".agents"),
    str(Path.home()),
]


def applies_to_runtime(item: dict, runtime: str) -> bool:
    if item.get("runtime") == runtime:
        return True
    if runtime == "cursor" and item.get("filename", "").endswith(".mdc"):
        return True
    return False


def stack_for_project(files: list[dict], runtime: str, project_root: str):
    project_root_path = Path(project_root).resolve()
    chosen = []
    for item in files:
        if not applies_to_runtime(item, runtime):
            continue
        p = Path(item["path"]).resolve()
        if item.get("scope") == "global":
            chosen.append(item)
            continue
        try:
            p.relative_to(project_root_path)
        except Exception:
            continue
        if item.get("filename") not in RUNTIME_FILENAMES.get(runtime, set()) and not item.get("filename", "").endswith(".mdc"):
            continue
        chosen.append(item)
    chosen.sort(key=lambda x: (0 if x.get("scope") == "global" else 1, len(Path(x["path"]).parts), x["path"]))
    total_tokens = sum(x.get("token_estimate", 0) for x in chosen)
    total_directives = sum(estimate_directive_count(safe_read_text(x["path"])) for x in chosen if Path(x["path"]).exists())
    risk = "low"
    if total_tokens > 2000 or total_directives > 150:
        risk = "high"
    elif total_tokens > 1000 or total_directives > 90:
        risk = "medium"
    return {
        "runtime": runtime,
        "project_root": project_root,
        "stack_files": [x["path"] for x in chosen],
        "stack_file_count": len(chosen),
        "total_tokens": total_tokens,
        "estimated_directives": total_directives,
        "risk": risk,
    }


def main():
    parser = argparse.ArgumentParser(description="Simulate plausible runtime instruction stacks.")
    parser.add_argument("inventory")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    _, files = load_inventory(args.inventory)
    runtimes = ["claude-code", "codex-cli", "gemini-cli", "cursor"]
    project_roots = sorted({f.get("project_root") for f in files if f.get("project_root")})
    stacks = []
    for runtime in runtimes:
        for root in project_roots:
            stack = stack_for_project(files, runtime, root)
            if stack["stack_files"]:
                stacks.append(stack)

    global_baseline = defaultdict(lambda: {"runtime": "", "global_files": [], "global_tokens": 0})
    for runtime in runtimes:
        items = [f for f in files if f.get("scope") == "global" and applies_to_runtime(f, runtime)]
        global_baseline[runtime] = {
            "runtime": runtime,
            "global_files": [f["path"] for f in sorted(items, key=lambda x: x["path"])],
            "global_tokens": sum(f.get("token_estimate", 0) for f in items),
        }

    payload = {
        "summary": {
            "stack_count": len(stacks),
            "high_risk_stacks": sum(1 for s in stacks if s["risk"] == "high"),
            "medium_risk_stacks": sum(1 for s in stacks if s["risk"] == "medium"),
        },
        "global_baseline": list(global_baseline.values()),
        "stacks": sorted(stacks, key=lambda s: (s["risk"], s["total_tokens"]), reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
