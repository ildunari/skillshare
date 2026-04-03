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
DEFAULT_SKILLSHARE_CONFIG = Path("/Users/kosta/.config/skillshare/config.yaml")
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


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else default


SKILLSHARE_CONFIG = _env_path("SKILLSHARE_CONFIG_PATH", DEFAULT_SKILLSHARE_CONFIG)


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


def normalize_path(path: str | Path) -> str:
    return str(path).replace("\\", "/").rstrip("/")


def path_startswith(path: str | Path, root: str | Path) -> bool:
    norm_path = normalize_path(path).lower()
    norm_root = normalize_path(root).lower()
    return norm_path == norm_root or norm_path.startswith(norm_root + "/")


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


def normalized_target_map(cfg: dict) -> dict[str, str]:
    targets = {}
    for name, meta in (cfg.get("targets") or {}).items():
        if not isinstance(meta, dict):
            continue
        path = None
        if isinstance(meta.get("skills"), dict):
            path = meta["skills"].get("path")
        path = path or meta.get("path")
        if path:
            targets[name] = path
    return targets


def normalized_discovery_items(data: dict) -> list[dict]:
    raw_items = data.get("skills") or data.get("items") or data.get("files") or []
    items = []
    for raw in raw_items:
        path = raw.get("path")
        if not path:
            continue
        item = dict(raw)
        item["path"] = path
        item["slug"] = raw.get("slug") or raw.get("name") or raw.get("directory") or skill_slug_from_path(path)
        item["content_hash"] = raw.get("content_hash") or raw.get("hash")
        item["runtime"] = raw.get("runtime") or raw.get("agent_runtime") or infer_runtime(path)
        item["role"] = raw.get("role") or classify_role(path)
        item["reference_count"] = raw.get("reference_count", raw.get("ref_count", 0))
        item["entity_type"] = raw.get("entity_type") or ("skill" if str(path).endswith("SKILL.md") else "unknown")
        items.append(item)
    return items


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
        in_targets = False
        in_skills_block = False
        for raw in SKILLSHARE_CONFIG.read_text().splitlines():
            line = raw.rstrip()
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if line.startswith("source:"):
                cfg["source"] = line.split(":", 1)[1].strip()
            elif line.startswith("mode:"):
                cfg["mode"] = line.split(":", 1)[1].strip()
            elif line.startswith("targets:"):
                in_targets = True
                cfg.setdefault("targets", {})
            elif in_targets and re.match(r"^  [A-Za-z0-9_.-]+:\s*$", line):
                current_target = line.strip().rstrip(":")
                cfg.setdefault("targets", {})[current_target] = {}
                in_skills_block = False
            elif current_target and re.match(r"^    skills:\s*$", line):
                cfg["targets"][current_target].setdefault("skills", {})
                in_skills_block = True
            elif current_target and in_skills_block and re.match(r"^      path:\s*", line):
                cfg["targets"][current_target]["skills"]["path"] = line.split(":", 1)[1].strip()
            elif current_target and re.match(r"^    path:\s*", line):
                cfg["targets"][current_target]["path"] = line.split(":", 1)[1].strip()
            elif not line.startswith(" "):
                in_targets = False
                current_target = None
                in_skills_block = False
        return cfg


def estimate_capability_count(text: str) -> int:
    return len(likely_capability_lines(text))
