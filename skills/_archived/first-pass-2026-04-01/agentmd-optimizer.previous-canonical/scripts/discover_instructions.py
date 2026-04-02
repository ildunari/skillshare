#!/usr/bin/env python3
"""
Discover all agent instruction files on the machine.

Scans global config directories, project roots, and home directory for
CLAUDE.md, AGENTS.md, GEMINI.md, and other instruction files.

Usage:
    python3 discover_instructions.py --output /tmp/instruction-discovery.json
    python3 discover_instructions.py --scan ~/Work ~/Clients --output /tmp/out.json
    python3 discover_instructions.py --help
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# Instruction file patterns to search for
INSTRUCTION_FILES = {
    "CLAUDE.md": "claude-code",
    "AGENTS.md": "codex-cli",
    "GEMINI.md": "gemini-cli",
}

# Additional patterns in specific directories
ADDITIONAL_PATTERNS = {
    ".cursor/rules": ("*.mdc", "cursor"),
    ".antigravity/rules": ("*.md", "antigravity"),
}

# Global config directories to always scan
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

# Common project root directories
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

# Memory file patterns
MEMORY_PATTERNS = [
    "~/.claude/projects/*/memory/MEMORY.md",
]

# Max directory depth for project scanning
MAX_PROJECT_DEPTH = 4


def _set_max_depth(depth: int):
    global MAX_PROJECT_DEPTH
    MAX_PROJECT_DEPTH = depth

# Directories to skip during scanning
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


def expand_path(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


def compute_hash(filepath: Path) -> str:
    try:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()[:16]
    except (OSError, PermissionError):
        return "unreadable"


def get_file_metadata(filepath: Path) -> dict:
    try:
        stat = filepath.stat()
        line_count = filepath.read_text(errors="replace").count("\n") + 1
        return {
            "size_bytes": stat.st_size,
            "line_count": line_count,
            "token_estimate": line_count * 4,  # rough tokens-per-line
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "content_hash": compute_hash(filepath),
        }
    except (OSError, PermissionError):
        return {
            "size_bytes": 0,
            "line_count": 0,
            "token_estimate": 0,
            "modified": "unknown",
            "content_hash": "unreadable",
        }


def classify_scope(filepath: Path, home: Path) -> str:
    """Classify as global or project-local."""
    rel = str(filepath)
    # Global: lives in ~/.<framework>/
    for gdir in GLOBAL_DIRS:
        expanded = str(expand_path(gdir))
        if rel.startswith(expanded):
            return "global"
    # Home-level files
    if filepath.parent == home:
        return "global"
    return "project-local"


def find_project_root(filepath: Path) -> str | None:
    """Walk up to find the nearest project root (has .git, Package.swift, etc.)."""
    project_markers = {
        ".git", "package.json", "Cargo.toml", "go.mod", "Package.swift",
        "pyproject.toml", "setup.py", "Makefile", "CMakeLists.txt",
        "pom.xml", "build.gradle", "Gemfile",
    }
    current = filepath.parent
    home = Path.home()
    while current != home and current != current.parent:
        if any((current / marker).exists() for marker in project_markers):
            return str(current)
        current = current.parent
    return None


def detect_runtime(filepath: Path, filename: str) -> str:
    """Detect which agent runtime this file targets."""
    if filename in INSTRUCTION_FILES:
        return INSTRUCTION_FILES[filename]

    path_str = str(filepath)
    if "/.claude/" in path_str or "/claude" in path_str.lower():
        return "claude-code"
    if "/.agents/" in path_str or "/.codex/" in path_str:
        return "codex-cli"
    if "/.gemini/" in path_str:
        return "gemini-cli"
    if "/.cursor/" in path_str:
        return "cursor"
    if "/.factory/" in path_str:
        return "factory"
    if "/.antigravity/" in path_str:
        return "antigravity"
    if "/.kiro/" in path_str:
        return "kiro"
    return "unknown"


def scan_directory_for_instructions(directory: Path, results: list, depth: int = 0):
    """Recursively scan a directory for instruction files."""
    if depth > MAX_PROJECT_DEPTH:
        return
    if not directory.is_dir():
        return

    try:
        entries = sorted(directory.iterdir())
    except (PermissionError, OSError):
        return

    for entry in entries:
        if entry.is_dir():
            if entry.name in SKIP_DIRS:
                continue
            # Check for additional patterns in specific subdirs
            for pattern_dir, (glob_pattern, runtime) in ADDITIONAL_PATTERNS.items():
                if str(entry).endswith(pattern_dir):
                    try:
                        for rule_file in entry.glob(glob_pattern):
                            if rule_file.is_file():
                                add_result(rule_file, runtime, results)
                    except (PermissionError, OSError):
                        pass

            scan_directory_for_instructions(entry, results, depth + 1)
        elif entry.is_file() and entry.name in INSTRUCTION_FILES:
            runtime = INSTRUCTION_FILES[entry.name]
            add_result(entry, runtime, results)


def add_result(filepath: Path, runtime: str, results: list):
    """Add a discovered file to results."""
    home = Path.home()
    meta = get_file_metadata(filepath)
    scope = classify_scope(filepath, home)
    project_root = find_project_root(filepath) if scope == "project-local" else None

    results.append({
        "path": str(filepath),
        "filename": filepath.name,
        "runtime": runtime,
        "scope": scope,
        "project_root": project_root,
        "directory": str(filepath.parent),
        **meta,
    })


def scan_global_dirs(results: list):
    """Scan global config directories for instruction files."""
    home = Path.home()

    # Check home directory itself
    for filename in INSTRUCTION_FILES:
        candidate = home / filename
        if candidate.is_file():
            add_result(candidate, INSTRUCTION_FILES[filename], results)

    # Check global config dirs
    for gdir in GLOBAL_DIRS:
        gpath = expand_path(gdir)
        if not gpath.is_dir():
            continue
        # Direct instruction files
        for filename in INSTRUCTION_FILES:
            candidate = gpath / filename
            if candidate.is_file():
                add_result(candidate, INSTRUCTION_FILES[filename], results)

        # Check subdirectories (e.g., ~/.claude/projects/*/CLAUDE.md)
        try:
            for subdir in gpath.iterdir():
                if subdir.is_dir() and subdir.name not in SKIP_DIRS:
                    scan_directory_for_instructions(subdir, results, depth=1)
        except (PermissionError, OSError):
            pass

    # Memory files
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
            except (PermissionError, OSError):
                pass


def scan_project_roots(roots: list[str], results: list):
    """Scan project root directories for instruction files."""
    for root in roots:
        rpath = expand_path(root)
        if rpath.is_dir():
            scan_directory_for_instructions(rpath, results)


def deduplicate(results: list) -> list:
    """Remove duplicates by resolved path."""
    seen = set()
    deduped = []
    for item in results:
        real_path = str(Path(item["path"]).resolve())
        if real_path not in seen:
            seen.add(real_path)
            item["canonical_path"] = real_path
            is_symlink = str(Path(item["path"])) != real_path
            item["is_symlink"] = is_symlink
            deduped.append(item)
    return deduped


def build_summary(results: list) -> dict:
    """Build a summary of discovered files."""
    by_runtime = {}
    by_scope = {"global": 0, "project-local": 0}
    by_filename = {}
    total_tokens = 0
    total_lines = 0

    for item in results:
        rt = item["runtime"]
        by_runtime[rt] = by_runtime.get(rt, 0) + 1
        by_scope[item["scope"]] = by_scope.get(item["scope"], 0) + 1
        fn = item["filename"]
        by_filename[fn] = by_filename.get(fn, 0) + 1
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
        "largest_files": [
            {"path": f["path"], "lines": f["line_count"], "tokens": f["token_estimate"]}
            for f in largest
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Discover agent instruction files on this machine."
    )
    parser.add_argument(
        "--output", "-o",
        default="/tmp/instruction-discovery.json",
        help="Output JSON file path (default: /tmp/instruction-discovery.json)",
    )
    parser.add_argument(
        "--scan",
        nargs="*",
        default=[],
        help="Additional project root directories to scan",
    )
    parser.add_argument(
        "--no-defaults",
        action="store_true",
        help="Skip scanning default project root directories",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=MAX_PROJECT_DEPTH,
        help=f"Maximum directory depth for scanning (default: {MAX_PROJECT_DEPTH})",
    )
    args = parser.parse_args()

    # Update module-level depth via function parameter instead of global
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

    print(f"\nDiscovery complete:", file=sys.stderr)
    print(f"  Total files: {summary['total_files']}", file=sys.stderr)
    print(f"  Total lines: {summary['total_lines']}", file=sys.stderr)
    print(f"  Est. tokens: {summary['total_token_estimate']}", file=sys.stderr)
    print(f"  By runtime:  {json.dumps(summary['by_runtime'])}", file=sys.stderr)
    print(f"  By scope:    {json.dumps(summary['by_scope'])}", file=sys.stderr)
    print(f"  Output:      {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
