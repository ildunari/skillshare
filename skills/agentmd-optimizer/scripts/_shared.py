#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

INSTRUCTION_FILENAMES = {"CLAUDE.md", "AGENTS.md", "GEMINI.md", "MEMORY.md"}
RUNTIME_LABELS = {
    "CLAUDE.md": "claude-code",
    "AGENTS.md": "codex-cli",
    "GEMINI.md": "gemini-cli",
    "MEMORY.md": "claude-code",
}
DIRECTIVE_RE = re.compile(
    r"\b(always|never|must|should|do not|don't|avoid|prefer|use|before|after|when|if)\b",
    re.I,
)
STALE_PATTERNS = [
    (re.compile(r"Claude\s*3(?:\.5)?|Sonnet\s*3|Opus\s*3", re.I), "obsolete-claude-3-reference"),
    (re.compile(r"Claude\s*4\.0|Opus\s*4\.0|Opus\s*4\.1", re.I), "stale-claude-4-reference"),
    (re.compile(r"GPT-4(?:o| Turbo)?", re.I), "stale-gpt4-reference"),
    (re.compile(r"Gemini\s*1\.5|Gemini\s*2\.0|Gemini\s*2\.5", re.I), "possibly-stale-gemini-reference"),
    (re.compile(r"TODO|FIXME"), "todo-fixme-in-instructions"),
]
ARCHIVE_MARKERS = ["/archive/", "/archives/", "/_external/", "/backup/", "/backups/", "/Trash/", "/.Trash/"]
MIRROR_MARKERS = ["/Documents - Kosta", "/mirror/", "/mirrors/", "/synced/", "/sync/"]
CACHE_MARKERS = ["/.claude/plugins/cache/", "/cache/", "/tmp/", "/temp_"]
VENDOR_MARKERS = ["/node_modules/", "/vendor/", "/Pods/"]
SKILL_HINT_MARKERS = ["/skills/", "/.claude/skills/", "/.codex/skills/", "/.gemini/skills/", "/.cursor/skills/", "/.factory/skills/", "/.kiro/skills/"]
PROJECT_MARKERS = {".git", "package.json", "pyproject.toml", "Cargo.toml", "Package.swift", "go.mod", "Gemfile", "Makefile"}


@dataclass
class FileRecord:
    path: str
    filename: str
    runtime: str
    scope: str
    project_root: str | None
    directory: str
    size_bytes: int
    line_count: int
    token_estimate: int
    modified: str
    content_hash: str
    canonical_path: str | None = None
    is_symlink: bool | None = None
    file_exists: bool | None = None
    path_kind: str | None = None


def load_json(path: str | Path):
    return json.loads(Path(path).read_text())


def write_json(path: str | Path, payload):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=False))
    return str(p)


def load_inventory(path: str | Path):
    data = load_json(path)
    files = data.get("files", data if isinstance(data, list) else [])
    return data, files


def safe_read_text(path: str | Path) -> str:
    try:
        return Path(path).read_text(errors="ignore")
    except Exception:
        return ""


def normalize_text(text: str) -> str:
    lines = [re.sub(r"\s+", " ", line.strip()) for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def sequence_similarity(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    return SequenceMatcher(None, a, b).ratio()


def jaccard_similarity(a: Iterable[str], b: Iterable[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def headings(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.lstrip().startswith("#")]


def likely_directive_lines(text: str) -> list[str]:
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or len(line) < 12:
            continue
        if line.startswith("#"):
            continue
        if DIRECTIVE_RE.search(line):
            out.append(line)
    return out


def stale_hits(text: str) -> list[str]:
    hits = []
    for pat, label in STALE_PATTERNS:
        if pat.search(text):
            hits.append(label)
    return sorted(set(hits))


def count_emphasis_hits(text: str) -> int:
    return len(re.findall(r"\b(MUST|ALWAYS|NEVER|CRITICAL)\b", text))


def count_all_caps_lines(text: str) -> int:
    n = 0
    for line in text.splitlines():
        letters = re.findall(r"[A-Z]", line)
        if len(letters) >= 8 and line.strip() and line.strip() == line.strip().upper():
            n += 1
    return n


def classify_path_kind(path: str) -> str:
    lower = path.lower()
    if any(marker.lower() in lower for marker in VENDOR_MARKERS):
        return "vendor"
    if any(marker.lower() in lower for marker in ARCHIVE_MARKERS):
        return "archive"
    if any(marker.lower() in lower for marker in MIRROR_MARKERS):
        return "mirror"
    if any(marker.lower() in lower for marker in CACHE_MARKERS):
        return "cache"
    if any(marker.lower() in lower for marker in SKILL_HINT_MARKERS):
        return "skill-install"
    return "project"


def exists_now(path: str) -> bool:
    return Path(path).exists()


def find_project_root_for_path(filepath: str | Path) -> str | None:
    current = Path(filepath).resolve().parent
    home = Path.home().resolve()
    while current != current.parent and current != home:
        if any((current / marker).exists() for marker in PROJECT_MARKERS):
            return str(current)
        current = current.parent
    return None


def runtime_family(path: str, filename: str) -> str:
    if filename in RUNTIME_LABELS:
        return RUNTIME_LABELS[filename]
    p = path.lower()
    if "/.claude/" in p or "/claude/" in p:
        return "claude-code"
    if "/.codex/" in p or "/.agents/" in p:
        return "codex-cli"
    if "/.gemini/" in p:
        return "gemini-cli"
    if "/.cursor/" in p:
        return "cursor"
    if "/.factory/" in p:
        return "factory"
    if "/.kiro/" in p:
        return "kiro"
    return "unknown"


def file_record_from_inventory(item: dict) -> FileRecord:
    return FileRecord(**item)


def bucket_counts(files: list[dict], key: str) -> dict[str, int]:
    c = Counter(str(f.get(key, "unknown")) for f in files)
    return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


def top_level_bucket(path: str) -> str:
    parts = Path(path).parts
    if len(parts) <= 4:
        return path
    if parts[1].startswith('.'):
        return "/" + "/".join(parts[1:3])
    return "/" + "/".join(parts[1:4])


def estimate_directive_count(text: str) -> int:
    return len(likely_directive_lines(text))


def path_depth_from_root(root: str | None, path: str) -> int:
    if not root:
        return 0
    try:
        rel = Path(path).resolve().relative_to(Path(root).resolve())
        return len(rel.parts)
    except Exception:
        return 0


def lines_by_category(text: str) -> dict[str, int]:
    directive_lines = likely_directive_lines(text)
    return {
        "heading_count": len(headings(text)),
        "directive_count": len(directive_lines),
        "emphasis_hits": count_emphasis_hits(text),
        "all_caps_lines": count_all_caps_lines(text),
        "stale_hit_count": len(stale_hits(text)),
    }


def cluster_by_hash(files: list[dict]) -> dict[str, list[dict]]:
    grouped = defaultdict(list)
    for item in files:
        grouped[item.get("content_hash", "unreadable")].append(item)
    return grouped
