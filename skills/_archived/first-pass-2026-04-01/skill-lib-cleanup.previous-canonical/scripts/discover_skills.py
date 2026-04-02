#!/usr/bin/env python3
"""
Discover all skills, agents, plugins, profiles, and rules across every
AI agent runtime on this machine. Resolves symlinks, extracts metadata,
classifies entity types and scope (global vs project-local), outputs JSON.

Usage:
    python discover_skills.py [--paths PATH1 PATH2 ...] [--output FILE]
    python discover_skills.py --scan-projects ~/LocalDev ~/Documents/ProjectsCode
    python discover_skills.py --all  # scan defaults + common project roots

Supports: Claude Code, Codex CLI, Factory/Droid, Cursor, Gemini CLI,
AntiGravity, Craft Agents, Osaurus, Kiro, and project-local .agents/.
"""

import argparse
import glob as globmod
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


# ── Entity Types ─────────────────────────────────────────────────────────────
# Each discovered item is classified as one of these types.
ENTITY_TYPES = {
    "skill",       # SKILL.md — reusable instruction set
    "agent",       # .md in agents/ or droids/ — autonomous entity definition
    "plugin",      # plugin.json or .codex-plugin/ — installable extension
    "profile",     # profiles.json or profile config — configuration preset
    "rule",        # .mdc or rules.md — always-on constraint
    "command",     # .md in commands/ — slash command binding
    "context",     # CLAUDE.md / AGENTS.md / GEMINI.md — project context file
}

# ── Global Skill Directories ────────────────────────────────────────────────
# These are user-level (~/.*) directories that contain skills globally.
GLOBAL_SKILL_PATHS = [
    # Shared / cross-framework
    "~/.agents/skills",
    # Claude Code
    "~/.claude/skills",
    "~/.claude-profiles/skills",
    # Factory / Droid
    "~/.factory/skills",
    # Codex CLI
    "~/.codex/skills",
    # Kiro (AWS)
    "~/.kiro/skills",
    # Cursor
    "~/.cursor/skills-cursor",
    # Gemini CLI
    "~/.gemini/skills",
    "~/.gemini/antigravity/skills",
    # Osaurus
    "~/.osaurus/skills",
    # Craft Agents (per-workspace)
    "~/.craft-agent/workspaces/*/skills",
    "~/.craft-agent-phone/workspaces/*/skills",
]

# ── Global Agent/Droid Directories ──────────────────────────────────────────
GLOBAL_AGENT_PATHS = [
    "~/.claude/agents",
    "~/.claude-profiles/agents",
    "~/.factory/droids",
]

# ── Global Command Directories ──────────────────────────────────────────────
GLOBAL_COMMAND_PATHS = [
    "~/.claude/commands",
    "~/.factory/commands",
]

# ── Global Profile Directories ──────────────────────────────────────────────
GLOBAL_PROFILE_PATHS = [
    "~/.agents/profiles",
]

# ── Global Rule Directories ─────────────────────────────────────────────────
GLOBAL_RULE_PATHS = [
    "~/.cursor/rules",
]

# ── Project-local patterns (searched inside project roots) ──────────────────
PROJECT_LOCAL_PATTERNS = [
    ".agents/skills",
    ".claude/skills",
    ".factory/skills",
    ".cursor/skills",
    ".gemini/skills",
    ".antigravity/skills",
    ".kiro/skills",
]

PROJECT_LOCAL_AGENT_PATTERNS = [
    ".claude/agents",
    ".agents/agents",
    ".factory/droids",
]

# ── Common project root directories to scan for project-local skills ────────
DEFAULT_PROJECT_ROOTS = [
    "~/LocalDev",
    "~/Developer",
    "~/Documents/ProjectsCode",
    "~/Documents/ProjectsXcode",
    "~/Documents/ProjectsApps",
    "~/Documents/ProjectsGames",
]

# ── Agent Runtime Detection ─────────────────────────────────────────────────
# Order matters: more specific patterns first.
AGENT_RUNTIME_MAP = [
    # Craft Agents
    (".craft-agent-phone/workspaces", "craft-agent-phone"),
    (".craft-agent/workspaces", "craft-agent"),
    # Framework-specific globals
    (".factory/", "factory"),
    (".kiro/", "kiro"),
    (".claude-profiles/", "claude-code"),
    (".claude/", "claude-code"),
    (".codex/", "codex-cli"),
    (".cursor/", "cursor"),
    (".gemini/antigravity/", "antigravity"),
    (".gemini/", "gemini-cli"),
    (".osaurus/", "osaurus"),
    # Cross-framework shared pool
    (".agents/", "global-pool"),
    # Project-local patterns
    ("/.agents/", "project-local"),
    ("/.claude/", "project-local"),
    ("/.factory/", "project-local"),
    ("/.cursor/", "project-local"),
    ("/.gemini/", "project-local"),
    ("/.antigravity/", "project-local"),
    ("/.kiro/", "project-local"),
]


def detect_agent_runtime(path: str) -> str:
    """Determine which agent runtime owns this path."""
    home = os.path.expanduser("~")
    # Normalize for matching
    norm = path.replace("\\", "/")

    for pattern, runtime in AGENT_RUNTIME_MAP:
        # For home-directory globals, check if path starts with ~/.<pattern>
        if pattern.startswith(".") and not pattern.startswith("/."):
            global_check = os.path.join(home, pattern).replace("\\", "/")
            if global_check in norm:
                if runtime == "craft-agent":
                    match = re.search(r"workspaces/([^/]+)/", norm)
                    if match:
                        return f"craft-agent:{match.group(1)}"
                elif runtime == "craft-agent-phone":
                    match = re.search(r"workspaces/([^/]+)/", norm)
                    if match:
                        return f"craft-agent-phone:{match.group(1)}"
                return runtime
        # For project-local patterns, check if path contains /<dotdir>/
        elif pattern.startswith("/"):
            if pattern in norm and not norm.startswith(os.path.join(home, pattern.lstrip("/")).replace("\\", "/")):
                return runtime

    return "unknown"


def detect_entity_type(filepath: str, parent_dir_name: str) -> str:
    """Classify what kind of entity this file represents."""
    basename = os.path.basename(filepath)
    dirpath = os.path.dirname(filepath)
    parent_of_parent = os.path.basename(os.path.dirname(dirpath))

    # SKILL.md → skill
    if basename == "SKILL.md":
        return "skill"

    # Context files
    if basename in ("CLAUDE.md", "AGENTS.md", "GEMINI.md"):
        return "context"

    # Agent/droid definitions (in agents/ or droids/ directories)
    if basename.endswith(".md") and parent_of_parent in ("agents", "droids"):
        return "agent"
    if parent_dir_name in ("agents", "droids") and basename.endswith(".md"):
        return "agent"

    # Rules (.mdc files or rules.md in rules/ directory)
    if basename.endswith(".mdc"):
        return "rule"
    if parent_dir_name == "rules" and basename.endswith(".md"):
        return "rule"

    # Commands
    if parent_dir_name == "commands" and basename.endswith(".md"):
        return "command"

    # Plugin manifests
    if basename == "plugin.json":
        return "plugin"

    # Profiles
    if "profile" in basename.lower() and basename.endswith(".json"):
        return "profile"

    return "skill"  # Default fallback


def detect_scope(path: str) -> str:
    """Classify whether this entity is global or project-local."""
    home = os.path.expanduser("~")
    norm = path.replace("\\", "/")
    home_norm = home.replace("\\", "/")

    # Home-directory dotfiles are global
    # Pattern: ~/.<framework>/...
    after_home = norm[len(home_norm):] if norm.startswith(home_norm) else ""
    if after_home and re.match(r"^/\.[^/]+", after_home):
        return "global"

    return "project-local"


def extract_project_root(path: str) -> str | None:
    """For project-local entities, extract the project root directory."""
    # Look for .agents/, .claude/, .factory/ etc. in path and return parent
    for pattern in [".agents/", ".claude/", ".factory/", ".cursor/",
                    ".gemini/", ".antigravity/", ".kiro/"]:
        idx = path.find("/" + pattern)
        if idx >= 0:
            return path[:idx]
    return None


def sha256_file(filepath: str) -> str:
    """Compute SHA256 hash of file contents."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()[:16]
    except (OSError, PermissionError):
        return "error"


def extract_frontmatter_name(filepath: str) -> str:
    """Extract skill name from YAML frontmatter."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(2000)
        if not content.startswith("---"):
            return os.path.basename(os.path.dirname(filepath))
        end = content.find("---", 3)
        if end == -1:
            return os.path.basename(os.path.dirname(filepath))
        frontmatter = content[3:end]
        for line in frontmatter.split("\n"):
            line = line.strip()
            if line.startswith("name:"):
                name = line[5:].strip().strip("'\"")
                return name
    except (OSError, UnicodeDecodeError):
        pass
    return os.path.basename(os.path.dirname(filepath))


def extract_agent_name(filepath: str) -> str:
    """Extract agent/droid name from filename or frontmatter."""
    basename = os.path.basename(filepath)
    name = os.path.splitext(basename)[0]

    # Try frontmatter
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(2000)
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                frontmatter = content[3:end]
                for line in frontmatter.split("\n"):
                    line = line.strip()
                    if line.startswith("name:"):
                        return line[5:].strip().strip("'\"")
    except (OSError, UnicodeDecodeError):
        pass
    return name


def expand_paths(path_patterns: list[str]) -> list[Path]:
    """Expand glob patterns and ~ in path list."""
    result = []
    for pattern in path_patterns:
        expanded = os.path.expanduser(pattern)
        if "*" in expanded:
            matches = globmod.glob(expanded)
            result.extend(Path(m) for m in matches if os.path.isdir(m))
        else:
            p = Path(expanded)
            if p.is_dir():
                result.append(p)
    return result


def discover_skills(paths: list[Path]) -> list[dict]:
    """Walk skill directories, find SKILL.md files, extract metadata."""
    visited_inodes = set()
    results = []

    for base_path in paths:
        for root, dirs, files in os.walk(str(base_path), followlinks=True):
            # Avoid infinite symlink loops
            try:
                inode = os.stat(root).st_ino
                if inode in visited_inodes:
                    dirs.clear()
                    continue
                visited_inodes.add(inode)
            except OSError:
                dirs.clear()
                continue

            # Skip deep nesting
            depth = root.replace(str(base_path), "").count(os.sep)
            if depth > 2:
                dirs.clear()
                continue

            if "SKILL.md" in files:
                skill_md = os.path.join(root, "SKILL.md")
                real_path = os.path.realpath(skill_md)
                is_symlink = os.path.islink(root) or os.path.islink(skill_md)

                try:
                    stat = os.stat(skill_md)
                    mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                    with open(skill_md, "r", errors="replace") as lf:
                        line_count = sum(1 for _ in lf)
                except OSError:
                    mtime = "unknown"
                    line_count = 0

                skill_dir = root
                ref_count = 0
                script_count = 0
                has_feedback = os.path.exists(os.path.join(skill_dir, "FEEDBACK.md"))

                refs_dir = os.path.join(skill_dir, "references")
                if os.path.isdir(refs_dir):
                    ref_count = len([f for f in os.listdir(refs_dir) if f.endswith(".md")])

                scripts_dir = os.path.join(skill_dir, "scripts")
                if os.path.isdir(scripts_dir):
                    script_count = len([
                        f for f in os.listdir(scripts_dir)
                        if f.endswith((".py", ".sh", ".js", ".ts"))
                    ])

                runtime = detect_agent_runtime(skill_md)
                scope = detect_scope(skill_md)
                project_root = extract_project_root(skill_md) if scope == "project-local" else None

                entry = {
                    "name": extract_frontmatter_name(skill_md),
                    "directory": os.path.basename(skill_dir),
                    "entity_type": "skill",
                    "scope": scope,
                    "path": skill_md,
                    "canonical_path": real_path,
                    "is_symlink": is_symlink,
                    "agent_runtime": runtime,
                    "mtime": mtime,
                    "hash": sha256_file(skill_md),
                    "line_count": line_count,
                    "ref_count": ref_count,
                    "script_count": script_count,
                    "has_feedback": has_feedback,
                }
                if project_root:
                    entry["project_root"] = project_root

                results.append(entry)
                dirs.clear()

    return results


def discover_agents(paths: list[Path]) -> list[dict]:
    """Walk agent/droid directories, find .md files, extract metadata."""
    results = []
    for base_path in paths:
        if not base_path.is_dir():
            continue
        try:
            for item in os.listdir(str(base_path)):
                filepath = os.path.join(str(base_path), item)
                if item.endswith(".md") and os.path.isfile(filepath):
                    real_path = os.path.realpath(filepath)
                    is_symlink = os.path.islink(filepath)

                    try:
                        stat = os.stat(filepath)
                        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                        with open(filepath, "r", errors="replace") as lf:
                            line_count = sum(1 for _ in lf)
                    except OSError:
                        mtime = "unknown"
                        line_count = 0

                    # Determine if it's an agent or droid based on parent dir name
                    parent_name = os.path.basename(str(base_path))
                    subtype = "droid" if parent_name == "droids" else "agent"

                    results.append({
                        "name": extract_agent_name(filepath),
                        "directory": os.path.splitext(item)[0],
                        "entity_type": "agent",
                        "entity_subtype": subtype,
                        "scope": detect_scope(filepath),
                        "path": filepath,
                        "canonical_path": real_path,
                        "is_symlink": is_symlink,
                        "agent_runtime": detect_agent_runtime(filepath),
                        "mtime": mtime,
                        "hash": sha256_file(filepath),
                        "line_count": line_count,
                        "ref_count": 0,
                        "script_count": 0,
                        "has_feedback": False,
                    })
        except OSError:
            continue
    return results


def discover_commands(paths: list[Path]) -> list[dict]:
    """Walk command directories, find .md files."""
    results = []
    for base_path in paths:
        if not base_path.is_dir():
            continue
        try:
            for item in os.listdir(str(base_path)):
                filepath = os.path.join(str(base_path), item)
                if item.endswith(".md") and os.path.isfile(filepath):
                    real_path = os.path.realpath(filepath)
                    try:
                        stat = os.stat(filepath)
                        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                        with open(filepath, "r", errors="replace") as lf:
                            line_count = sum(1 for _ in lf)
                    except OSError:
                        mtime = "unknown"
                        line_count = 0

                    results.append({
                        "name": os.path.splitext(item)[0],
                        "directory": os.path.splitext(item)[0],
                        "entity_type": "command",
                        "scope": detect_scope(filepath),
                        "path": filepath,
                        "canonical_path": real_path,
                        "is_symlink": os.path.islink(filepath),
                        "agent_runtime": detect_agent_runtime(filepath),
                        "mtime": mtime,
                        "hash": sha256_file(filepath),
                        "line_count": line_count,
                        "ref_count": 0,
                        "script_count": 0,
                        "has_feedback": False,
                    })
        except OSError:
            continue
    return results


def discover_rules(paths: list[Path]) -> list[dict]:
    """Walk rule directories, find .mdc and .md files."""
    results = []
    for base_path in paths:
        if not base_path.is_dir():
            continue
        try:
            for item in os.listdir(str(base_path)):
                filepath = os.path.join(str(base_path), item)
                if (item.endswith(".mdc") or item.endswith(".md")) and os.path.isfile(filepath):
                    real_path = os.path.realpath(filepath)
                    try:
                        stat = os.stat(filepath)
                        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                        with open(filepath, "r", errors="replace") as lf:
                            line_count = sum(1 for _ in lf)
                    except OSError:
                        mtime = "unknown"
                        line_count = 0

                    results.append({
                        "name": os.path.splitext(item)[0],
                        "directory": os.path.splitext(item)[0],
                        "entity_type": "rule",
                        "scope": detect_scope(filepath),
                        "path": filepath,
                        "canonical_path": real_path,
                        "is_symlink": os.path.islink(filepath),
                        "agent_runtime": detect_agent_runtime(filepath),
                        "mtime": mtime,
                        "hash": sha256_file(filepath),
                        "line_count": line_count,
                        "ref_count": 0,
                        "script_count": 0,
                        "has_feedback": False,
                    })
        except OSError:
            continue
    return results


def discover_project_local(project_roots: list[str]) -> list[dict]:
    """Scan project root directories for .agents/skills/, .claude/skills/, etc."""
    results = []
    visited = set()

    for root_pattern in project_roots:
        root_expanded = os.path.expanduser(root_pattern)
        if not os.path.isdir(root_expanded):
            continue

        # Walk one level deep to find project directories
        try:
            entries = os.listdir(root_expanded)
        except OSError:
            continue

        for entry in entries:
            project_dir = os.path.join(root_expanded, entry)
            if not os.path.isdir(project_dir):
                continue

            for pattern in PROJECT_LOCAL_PATTERNS:
                skill_dir = os.path.join(project_dir, pattern)
                if os.path.isdir(skill_dir) and skill_dir not in visited:
                    visited.add(skill_dir)
                    # Find SKILL.md files
                    skills = discover_skills([Path(skill_dir)])
                    # Override scope and add project root
                    for s in skills:
                        s["scope"] = "project-local"
                        s["project_root"] = project_dir
                        if s["agent_runtime"] == "unknown":
                            # Infer runtime from pattern
                            if ".agents/" in pattern:
                                s["agent_runtime"] = "project-local:agents"
                            elif ".claude/" in pattern:
                                s["agent_runtime"] = "project-local:claude"
                            elif ".factory/" in pattern:
                                s["agent_runtime"] = "project-local:factory"
                            elif ".cursor/" in pattern:
                                s["agent_runtime"] = "project-local:cursor"
                            elif ".gemini/" in pattern:
                                s["agent_runtime"] = "project-local:gemini"
                            elif ".antigravity/" in pattern:
                                s["agent_runtime"] = "project-local:antigravity"
                            elif ".kiro/" in pattern:
                                s["agent_runtime"] = "project-local:kiro"
                    results.extend(skills)

            # Also check for agent/droid definitions
            for pattern in PROJECT_LOCAL_AGENT_PATTERNS:
                agent_dir = os.path.join(project_dir, pattern)
                if os.path.isdir(agent_dir) and agent_dir not in visited:
                    visited.add(agent_dir)
                    agents = discover_agents([Path(agent_dir)])
                    for a in agents:
                        a["scope"] = "project-local"
                        a["project_root"] = project_dir
                    results.extend(agents)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Discover skills, agents, plugins, and rules across all AI agent runtimes"
    )
    parser.add_argument("--paths", nargs="*", default=None,
                        help="Additional skill directories to scan")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file (default: stdout)")
    parser.add_argument("--compact", action="store_true",
                        help="Compact JSON output")
    parser.add_argument("--scan-projects", nargs="*", default=None,
                        help="Project root dirs to scan for local skills")
    parser.add_argument("--all", action="store_true",
                        help="Scan all defaults + common project roots")
    parser.add_argument("--skills-only", action="store_true",
                        help="Only discover SKILL.md files (skip agents, commands, rules)")
    args = parser.parse_args()

    # Build list of paths to scan
    skill_patterns = list(GLOBAL_SKILL_PATHS)
    if args.paths:
        skill_patterns.extend(args.paths)

    skill_paths = expand_paths(skill_patterns)
    agent_paths = expand_paths(GLOBAL_AGENT_PATHS)
    command_paths = expand_paths(GLOBAL_COMMAND_PATHS)
    rule_paths = expand_paths(GLOBAL_RULE_PATHS)
    profile_paths = expand_paths(GLOBAL_PROFILE_PATHS)

    if not skill_paths and not agent_paths:
        print("No valid directories found.", file=sys.stderr)
        sys.exit(1)

    all_results = []

    # Phase 1: Global skills
    print(f"Scanning {len(skill_paths)} skill directories...", file=sys.stderr)
    skills = discover_skills(skill_paths)
    all_results.extend(skills)
    print(f"  Found {len(skills)} skills", file=sys.stderr)

    if not args.skills_only:
        # Phase 2: Global agents/droids
        if agent_paths:
            print(f"Scanning {len(agent_paths)} agent/droid directories...", file=sys.stderr)
            agents = discover_agents(agent_paths)
            all_results.extend(agents)
            print(f"  Found {len(agents)} agents/droids", file=sys.stderr)

        # Phase 3: Global commands
        if command_paths:
            commands = discover_commands(command_paths)
            all_results.extend(commands)
            if commands:
                print(f"  Found {len(commands)} commands", file=sys.stderr)

        # Phase 4: Global rules
        if rule_paths:
            rules = discover_rules(rule_paths)
            all_results.extend(rules)
            if rules:
                print(f"  Found {len(rules)} rules", file=sys.stderr)

    # Phase 5: Project-local skills
    project_roots = []
    if args.scan_projects:
        project_roots = args.scan_projects
    elif args.all:
        project_roots = DEFAULT_PROJECT_ROOTS

    if project_roots:
        print(f"Scanning {len(project_roots)} project roots for local skills...", file=sys.stderr)
        local = discover_project_local(project_roots)
        all_results.extend(local)
        if local:
            print(f"  Found {len(local)} project-local items", file=sys.stderr)

    print(f"Total: {len(all_results)} items discovered.", file=sys.stderr)

    # Build summary by entity type and scope
    by_type = defaultdict(int)
    by_scope = defaultdict(int)
    by_runtime = defaultdict(int)
    for item in all_results:
        by_type[item.get("entity_type", "skill")] += 1
        by_scope[item.get("scope", "global")] += 1
        by_runtime[item.get("agent_runtime", "unknown")] += 1

    output = {
        "discovered_at": datetime.now(tz=timezone.utc).isoformat(),
        "directories_scanned": [str(p) for p in skill_paths + agent_paths + command_paths + rule_paths],
        "project_roots_scanned": project_roots,
        "total_items": len(all_results),
        "total_skills": by_type.get("skill", 0),
        "summary": {
            "by_entity_type": dict(by_type),
            "by_scope": dict(by_scope),
            "by_runtime": dict(sorted(by_runtime.items())),
        },
        "skills": all_results,  # Keep "skills" key for backward compat
    }

    indent = None if args.compact else 2
    json_str = json.dumps(output, indent=indent, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
