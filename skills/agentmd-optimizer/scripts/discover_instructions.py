#!/usr/bin/env python3
"""
Discover agent instruction files on the machine and emit a rich inventory for
later deterministic analysis.

The output is intentionally machine-readable first. Later scripts consume this
inventory to simulate load stacks, cluster duplicates, extract directives, and
score actions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from _shared import classify_path_kind, runtime_family, top_level_bucket


INSTRUCTION_FILES = {
    "CLAUDE.md": "claude-code",
    "AGENTS.md": "codex-cli",
    "GEMINI.md": "gemini-cli",
}
ADDITIONAL_PATTERNS = {
    ".cursor/rules": ("*.mdc", "cursor"),
    ".antigravity/rules": ("*.md", "antigravity"),
}
GLOBAL_DIRS = [
    "~/.claude",
    "~/.agents",
    "~/.gemini",
    "~/.cursor",
    "~/.antigravity",
    "~/.factory",
    "~/.codex",
    "~/.kiro",
]
DEFAULT_PROJECT_ROOTS = [
    "~/LocalDev",
    "~/Developer",
    "~/Projects",
    "~/Documents",
    "~/Desktop",
    "~/repos",
    "~/src",
    "~/code",
    "~/workspace",
    "~/Work",
]
MEMORY_PATTERNS = ["~/.claude/projects/*/memory/MEMORY.md"]
SKIP_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".build",
    "DerivedData",
    "Pods",
    ".cocoapods",
    "vendor",
    ".cargo",
    "target",
    ".next",
    ".nuxt",
    ".output",
    "_archived",
    "Trash",
    ".Trash",
    "Library",
}
PROJECT_MARKERS = {
    ".git",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "Package.swift",
    "pyproject.toml",
    "setup.py",
    "Makefile",
    "CMakeLists.txt",
    "pom.xml",
    "build.gradle",
    "Gemfile",
}
MAX_PROJECT_DEPTH = 4


def _set_max_depth(depth: int):
    global MAX_PROJECT_DEPTH
    MAX_PROJECT_DEPTH = depth


def expand_path(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


def compute_hash(filepath: Path) -> str:
    try:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()[:16]
    except Exception:
        return "unreadable"


def get_file_metadata(filepath: Path) -> dict:
    try:
        stat = filepath.stat()
        text = filepath.read_text(errors="replace")
        line_count = text.count("\n") + 1
        return {
            "size_bytes": stat.st_size,
            "line_count": line_count,
            "token_estimate": line_count * 4,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "content_hash": compute_hash(filepath),
        }
    except Exception:
        return {
            "size_bytes": 0,
            "line_count": 0,
            "token_estimate": 0,
            "modified": "unknown",
            "content_hash": "unreadable",
        }


def classify_scope(filepath: Path, home: Path) -> str:
    rel = str(filepath)
    for gdir in GLOBAL_DIRS:
        expanded = str(expand_path(gdir))
        if rel.startswith(expanded):
            return "global"
    if filepath.parent == home:
        return "global"
    return "project-local"


def find_project_root(filepath: Path) -> str | None:
    current = filepath.parent.resolve()
    home = Path.home().resolve()
    while current != home and current != current.parent:
        if any((current / marker).exists() for marker in PROJECT_MARKERS):
            return str(current)
        current = current.parent
    return None


def add_result(filepath: Path, runtime: str, results: list):
    home = Path.home().resolve()
    meta = get_file_metadata(filepath)
    scope = classify_scope(filepath, home)
    project_root = find_project_root(filepath) if scope == "project-local" else None
    real_path = str(filepath.resolve())

    results.append(
        {
            "path": str(filepath),
            "filename": filepath.name,
            "runtime": runtime_family(str(filepath), filepath.name) if runtime == "unknown" else runtime,
            "scope": scope,
            "project_root": project_root,
            "directory": str(filepath.parent),
            **meta,
            "canonical_path": real_path,
            "is_symlink": str(filepath) != real_path,
            "path_kind": classify_path_kind(str(filepath)),
            "top_level_bucket": top_level_bucket(str(filepath)),
            "file_exists": filepath.exists(),
        }
    )


def scan_directory_for_instructions(directory: Path, results: list, depth: int = 0):
    if depth > MAX_PROJECT_DEPTH or not directory.is_dir():
        return
    try:
        entries = sorted(directory.iterdir())
    except Exception:
        return

    for entry in entries:
        if entry.is_dir():
            if entry.name in SKIP_DIRS:
                continue
            for pattern_dir, (glob_pattern, runtime) in ADDITIONAL_PATTERNS.items():
                if str(entry).endswith(pattern_dir):
                    try:
                        for rule_file in entry.glob(glob_pattern):
                            if rule_file.is_file():
                                add_result(rule_file, runtime, results)
                    except Exception:
                        pass
            scan_directory_for_instructions(entry, results, depth + 1)
        elif entry.is_file() and entry.name in INSTRUCTION_FILES:
            add_result(entry, INSTRUCTION_FILES[entry.name], results)


def scan_global_dirs(results: list):
    home = Path.home().resolve()
    for filename in INSTRUCTION_FILES:
        candidate = home / filename
        if candidate.is_file():
            add_result(candidate, INSTRUCTION_FILES[filename], results)

    for gdir in GLOBAL_DIRS:
        gpath = expand_path(gdir)
        if not gpath.is_dir():
            continue
        for filename in INSTRUCTION_FILES:
            candidate = gpath / filename
            if candidate.is_file():
                add_result(candidate, INSTRUCTION_FILES[filename], results)
        try:
            for subdir in gpath.iterdir():
                if subdir.is_dir() and subdir.name not in SKIP_DIRS:
                    scan_directory_for_instructions(subdir, results, depth=1)
        except Exception:
            pass

    for pattern in MEMORY_PATTERNS:
        expanded = str(expand_path(pattern.split("*")[0]))
        base = Path(expanded)
        if base.is_dir():
            try:
                for memory_dir in base.iterdir():
                    if memory_dir.is_dir():
                        memory_file = memory_dir / "memory" / "MEMORY.md"
                        if memory_file.is_file():
                            add_result(memory_file, "claude-code", results)
            except Exception:
                pass


def scan_project_roots(roots: list[str], results: list):
    for root in roots:
        rpath = expand_path(root)
        if rpath.is_dir():
            scan_directory_for_instructions(rpath, results)


def deduplicate(results: list) -> list:
    seen = set()
    deduped = []
    for item in results:
        key = item["canonical_path"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def build_summary(results: list) -> dict:
    by_runtime: dict[str, int] = {}
    by_scope: dict[str, int] = {"global": 0, "project-local": 0}
    by_filename: dict[str, int] = {}
    by_path_kind: dict[str, int] = {}
    total_tokens = 0
    total_lines = 0

    for item in results:
        by_runtime[item["runtime"]] = by_runtime.get(item["runtime"], 0) + 1
        by_scope[item["scope"]] = by_scope.get(item["scope"], 0) + 1
        by_filename[item["filename"]] = by_filename.get(item["filename"], 0) + 1
        by_path_kind[item["path_kind"]] = by_path_kind.get(item["path_kind"], 0) + 1
        total_tokens += item["token_estimate"]
        total_lines += item["line_count"]

    largest = sorted(results, key=lambda x: x["line_count"], reverse=True)[:10]

    return {
        "total_files": len(results),
        "total_lines": total_lines,
        "total_token_estimate": total_tokens,
        "by_runtime": by_runtime,
        "by_scope": by_scope,
        "by_filename": by_filename,
        "by_path_kind": by_path_kind,
        "largest_files": [
            {
                "path": f["path"],
                "lines": f["line_count"],
                "tokens": f["token_estimate"],
                "path_kind": f["path_kind"],
            }
            for f in largest
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Discover agent instruction files on this machine.")
    parser.add_argument("--output", "-o", default="/tmp/instruction-discovery.json")
    parser.add_argument("--scan", nargs="*", default=[])
    parser.add_argument("--no-defaults", action="store_true")
    parser.add_argument("--max-depth", type=int, default=MAX_PROJECT_DEPTH)
    args = parser.parse_args()

    _set_max_depth(args.max_depth)
    results = []

    print("Scanning global directories...", file=sys.stderr)
    scan_global_dirs(results)

    project_roots = args.scan[:]
    if not args.no_defaults:
        project_roots.extend(DEFAULT_PROJECT_ROOTS)

    if project_roots:
        print(f"Scanning {len(project_roots)} project root(s)...", file=sys.stderr)
        scan_project_roots(project_roots, results)

    print(f"Found {len(results)} files before deduplication", file=sys.stderr)
    results = deduplicate(results)
    print(f"Found {len(results)} unique files after deduplication", file=sys.stderr)

    summary = build_summary(results)
    output = {
        "scan_time": datetime.now().isoformat(),
        "machine": os.uname().nodename,
        "home": str(Path.home()),
        "summary": summary,
        "files": results,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2))

    print("\nDiscovery complete:", file=sys.stderr)
    print(f"  Total files: {summary['total_files']}", file=sys.stderr)
    print(f"  Total lines: {summary['total_lines']}", file=sys.stderr)
    print(f"  Est. tokens: {summary['total_token_estimate']}", file=sys.stderr)
    print(f"  By runtime:  {json.dumps(summary['by_runtime'])}", file=sys.stderr)
    print(f"  By scope:    {json.dumps(summary['by_scope'])}", file=sys.stderr)
    print(f"  By kind:     {json.dumps(summary['by_path_kind'])}", file=sys.stderr)
    print(f"  Output:      {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
