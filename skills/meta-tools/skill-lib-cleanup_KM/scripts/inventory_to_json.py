#!/usr/bin/env python3
"""
Bulk extract frontmatter metadata from SKILL.md and agent .md files.
Reads discovery JSON and enriches each item with parsed frontmatter fields.

Usage:
    python inventory_to_json.py DISCOVERY_JSON [--output FILE]
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_frontmatter(filepath: str) -> dict:
    """Extract YAML frontmatter fields from SKILL.md or agent .md."""
    try:
        content = Path(filepath).read_text(errors="replace")
    except OSError:
        return {}

    if not content.startswith("---"):
        return {}

    end = content.find("---", 3)
    if end == -1:
        return {}

    frontmatter = content[3:end]
    result = {}

    # Extract name
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    if name_match:
        result["name"] = name_match.group(1).strip().strip("'\"")

    # Extract description (handles multi-line with > or |)
    desc_match = re.search(
        r"^description:\s*[>|]?\s*\n?((?:[ \t]+.+\n?)+|.+)$",
        frontmatter, re.MULTILINE
    )
    if desc_match:
        desc = desc_match.group(1).strip()
        desc = re.sub(r"\s+", " ", desc).strip()
        if (desc.startswith('"') and desc.endswith('"')) or \
           (desc.startswith("'") and desc.endswith("'")):
            desc = desc[1:-1]
        result["description"] = desc
    else:
        desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
        if desc_match:
            result["description"] = desc_match.group(1).strip()

    # Extract trigger phrases from description
    desc = result.get("description", "")
    triggers = []
    trigger_patterns = re.findall(
        r'(?:trigger|use when|use for|triggers? on)[:\s]+(.+?)(?:\.|$)',
        desc, re.IGNORECASE
    )
    for tp in trigger_patterns:
        phrases = [p.strip().strip('"\'') for p in re.split(r'[,;]|" or "|\bor\b', tp)]
        triggers.extend(p for p in phrases if len(p) > 3)
    result["triggers"] = triggers[:15]

    # Extract supersedes declarations
    supersedes = []
    sup_match = re.search(r"supersedes?\s+(.+?)(?:\.|$)", desc, re.IGNORECASE)
    if sup_match:
        supersedes = [s.strip() for s in re.split(r",|\band\b", sup_match.group(1))]
    result["supersedes"] = supersedes

    # Count body sections (## headers)
    body = content[end + 3:]
    sections = re.findall(r"^##\s+.+$", body, re.MULTILINE)
    result["section_count"] = len(sections)

    # Extract agent-specific frontmatter fields
    for field in ["model", "tools", "permissionMode", "maxTurns", "effort",
                  "allowed-tools", "user-invocable", "disable-model-invocation",
                  "agent", "isolation", "context"]:
        field_match = re.search(rf"^{re.escape(field)}:\s*(.+)$", frontmatter, re.MULTILINE)
        if field_match:
            val = field_match.group(1).strip().strip("'\"")
            result[field] = val

    # Detect platform targets from content
    platforms = set()
    content_lower = content.lower()
    platform_signals = {
        "claude-code": ["claude code", "claude-code", "task tool", "bash tool"],
        "codex-cli": ["codex", "codex cli", "codex_home"],
        "craft-agent": ["craft agent", "craft-agent", "craftagents://"],
        "cursor": ["cursor", ".mdc", "cursor rules"],
        "gemini-cli": ["gemini cli", "gemini.md"],
        "factory": ["factory", "droid", ".factory/"],
    }
    for platform, signals in platform_signals.items():
        if any(sig in content_lower for sig in signals):
            platforms.add(platform)
    result["platform_signals"] = sorted(platforms)

    return result


def enrich_inventory(discovery: dict) -> dict:
    """Add parsed frontmatter to each item in discovery data."""
    enriched = []

    for item in discovery.get("skills", []):
        fm = parse_frontmatter(item.get("path", ""))
        enriched_item = {
            **item,
            "parsed_name": fm.get("name", item.get("name", "")),
            "description": fm.get("description", ""),
            "triggers": fm.get("triggers", []),
            "supersedes": fm.get("supersedes", []),
            "section_count": fm.get("section_count", 0),
            "platform_signals": fm.get("platform_signals", []),
        }
        # Carry through agent-specific fields
        for field in ["model", "tools", "permissionMode", "maxTurns", "effort",
                      "allowed-tools", "user-invocable", "disable-model-invocation",
                      "agent", "isolation", "context"]:
            if field in fm:
                enriched_item[field] = fm[field]

        enriched.append(enriched_item)

    # Build per-entity-type counts
    by_type = {}
    for item in enriched:
        et = item.get("entity_type", "skill")
        by_type[et] = by_type.get(et, 0) + 1

    return {
        "inventoried_at": discovery.get("discovered_at", ""),
        "total_items": len(enriched),
        "total_skills": by_type.get("skill", 0),
        "by_entity_type": by_type,
        "skills": enriched,
    }


def main():
    parser = argparse.ArgumentParser(description="Bulk extract SKILL.md / agent metadata")
    parser.add_argument("discovery_json", help="Path to discover_skills.py output")
    parser.add_argument("--output", "-o", default=None, help="Output file")
    args = parser.parse_args()

    with open(args.discovery_json) as f:
        discovery = json.load(f)

    inventory = enrich_inventory(discovery)

    print(f"Inventoried {inventory['total_items']} items "
          f"({inventory['total_skills']} skills).", file=sys.stderr)

    json_str = json.dumps(inventory, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
