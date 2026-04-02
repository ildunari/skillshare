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

SKILL_FILES = {"SKILL.md", "CLAUDE.md", "AGENTS.md", "GEMINI.md"}
SKILLSHARE_CONFIG = Path("/Users/kosta/.config/skillshare/config.yaml")
STALE_MODEL_PATTERNS = [
    (re.compile(r"Claude\s*3(?:\.5)?|Sonnet\s*3|Opus\s*4\.1", re.I), "stale-claude-model"),
    (re.compile(r"GPT-4(?:o| Turbo)?", re.I), "stale-gpt4-model"),
    (re.compile(r"Gemini\s*1\.5|Gemini\s*2\.0", re.I), "stale-gemini-model"),
]
ROLE_MARKERS = {
    "canonical-source": ["/Users/kosta/.config/skillshare/skills/"],
    "runtime-install": ["/.claude/skills/", "/.codex/skills/", "/.factory/skills/", "/.gemini/skills/", "/.cursor/skills/", "/.kiro/skills/", "/.craft-agent/workspaces/"],
    "backup": ["/backup/", "/backups/"],
    "archive": ["/archive/", "/archives/", "/_archived/"],
    "mirror": ["/Documents - Kosta", "/mirror/", "/mirrors/", "/sync/"],
}


def load_json(path: str | Path):
    return json.loads(Path(path).read_text())


def write_json(path: str | Path, payload):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2))
    return str(p)


def safe_read_text(path: str | Path) -> str:
    try:
        return Path(path).read_text(errors="ignore")
    except Exception:
        return ""


def normalize_text(text: str) -> str:
    lines = [re.sub(r"\s+", " ", line.strip()) for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


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


def classify_role(path: str) -> str:
    lower = path.lower()
    for role, markers in ROLE_MARKERS.items():
        if any(marker.lower() in lower for marker in markers):
            return role
    if "/node_modules/" in lower or "/vendor/" in lower:
        return "vendor"
    if "/tmp/" in lower or "/cache/" in lower:
        return "generated-artifact"
    return "other"


def infer_runtime(path: str) -> str:
    lower = path.lower()
    if "/.claude/" in lower:
        return "claude-code"
    if "/.codex/" in lower or "/.agents/" in lower:
        return "codex-cli"
    if "/.factory/" in lower:
        return "factory"
    if "/.cursor/" in lower:
        return "cursor"
    if "/.gemini/" in lower and "/antigravity/" in lower:
        return "antigravity"
    if "/.gemini/" in lower:
        return "gemini-cli"
    if "/.kiro/" in lower:
        return "kiro"
    if "/.craft-agent/" in lower:
        return "craft-agent"
    if "/.config/skillshare/skills/" in lower:
        return "canonical-source"
    return "unknown"


def skill_slug_from_path(path: str) -> str | None:
    p = Path(path)
    parts = p.parts
    if "skills" in parts:
        idx = parts.index("skills")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return p.parent.name if p.name == "SKILL.md" else None


def headings(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.lstrip().startswith("#")]


def trigger_phrases(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        line = line.strip()
        if "Use when" in line or "Triggers on" in line or "Also use when" in line:
            out.append(line)
    return out


def likely_capability_lines(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or len(s) < 12 or s.startswith("#"):
            continue
        if re.search(r"\b(use when|triggers on|also use when|run|audit|merge|review|create|optimize|sync|analyze|clean up)\b", s, re.I):
            out.append(s)
    return out


def stale_hits(text: str) -> list[str]:
    hits = []
    for pat, label in STALE_MODEL_PATTERNS:
        if pat.search(text):
            hits.append(label)
    if "TODO" in text or "FIXME" in text:
        hits.append("todo-fixme")
    return sorted(set(hits))


def top_level_bucket(path: str) -> str:
    parts = Path(path).parts
    if len(parts) <= 4:
        return path
    return "/" + "/".join(parts[1:4])


def load_skillshare_config() -> dict:
    if not SKILLSHARE_CONFIG.exists():
        return {}
    try:
        import yaml  # type: ignore
        return yaml.safe_load(SKILLSHARE_CONFIG.read_text()) or {}
    except Exception:
        cfg = {}
        current_target = None
        for raw in SKILLSHARE_CONFIG.read_text().splitlines():
            line = raw.rstrip()
            if line.startswith("source:"):
                cfg["source"] = line.split(":", 1)[1].strip()
            elif line.startswith("mode:"):
                cfg["mode"] = line.split(":", 1)[1].strip()
            elif re.match(r"^  [A-Za-z0-9_.-]+:", line):
                current_target = line.strip().rstrip(":")
                cfg.setdefault("targets", {})[current_target] = {}
            elif current_target and "path:" in line:
                cfg["targets"][current_target]["path"] = line.split(":", 1)[1].strip()
        return cfg


def estimate_capability_count(text: str) -> int:
    return len(likely_capability_lines(text))
