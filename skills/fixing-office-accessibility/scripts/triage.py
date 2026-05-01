#!/usr/bin/env python3
"""Group and order stage 4 accessibility findings."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

CATEGORY_RULES = [
    ("reading_order", re.compile(r"READING_ORDER|MEANINGFUL_SEQUENCE|FLOATING_OBJECT_ORDER", re.I)),
    ("complex_table", re.compile(r"TABLE|MERGED|MERGE|LAYOUT_TABLE", re.I)),
    ("heading_structure", re.compile(r"HEADING|SECTION_TITLE", re.I)),
    ("color_contrast", re.compile(r"CONTRAST|COLOR", re.I)),
    ("decorative_or_informative_image", re.compile(r"ALT|IMAGE|DECORATIVE|PICTURE|SMARTART|CHART_ALT", re.I)),
    ("floating_object", re.compile(r"FLOATING|WRAP|ANCHOR", re.I)),
    ("link_text", re.compile(r"LINK", re.I)),
    ("slide_title", re.compile(r"SLIDE_TITLE|TITLE_MISSING|TITLE_DUPLICATE", re.I)),
    ("document_metadata", re.compile(r"DOCUMENT_TITLE|CORE_TITLE|METADATA", re.I)),
    ("language", re.compile(r"LANG", re.I)),
    ("form_control", re.compile(r"FORM|CONTROL|NAME_ROLE", re.I)),
]

SEVERITY_WEIGHT = {"error": 100, "warning": 70, "tip": 35, "info": 20}
CATEGORY_WEIGHT = {
    "reading_order": 70,
    "complex_table": 65,
    "heading_structure": 60,
    "color_contrast": 50,
    "slide_title": 45,
    "decorative_or_informative_image": 40,
    "floating_object": 40,
    "link_text": 35,
    "document_metadata": 25,
    "language": 25,
    "form_control": 55,
    "other": 20,
}
STRUCTURAL = {"reading_order", "complex_table", "heading_structure", "floating_object", "form_control"}


def categorize(finding: Dict[str, Any]) -> str:
    if finding.get("issue_type"):
        return str(finding["issue_type"])
    rule = str(finding.get("rule_id", ""))
    for category, pattern in CATEGORY_RULES:
        if pattern.search(rule):
            return category
    return "other"


def container_key(location: str, category: str) -> str:
    if category in {"reading_order", "slide_title"}:
        match = re.search(r"/slide\[\d+\]", location)
        if match:
            return match.group(0)
    if category in {"complex_table", "merged_cells"}:
        match = re.search(r"(/body/tbl\[\d+\]|/slide\[\d+\]/table\[\d+\])", location)
        if match:
            return match.group(1)
    if category == "heading_structure":
        return "document-outline"
    return location.rsplit("/", 1)[0] if "/" in location else location


def build_components(findings: List[Dict[str, Any]]) -> List[Set[str]]:
    ids = {f["id"] for f in findings}
    neighbors: Dict[str, Set[str]] = {f["id"]: set() for f in findings}
    by_id = {f["id"]: f for f in findings}
    bucket: Dict[tuple, List[str]] = defaultdict(list)

    for f in findings:
        fid = f["id"]
        for rid in f.get("related_findings_ids", []):
            if rid in ids:
                neighbors[fid].add(rid)
                neighbors[rid].add(fid)
        category = categorize(f)
        bucket[(category, container_key(str(f.get("location", "")), category))].append(fid)

    for members in bucket.values():
        if len(members) > 1:
            first = members[0]
            for member in members[1:]:
                neighbors[first].add(member)
                neighbors[member].add(first)

    seen: Set[str] = set()
    components: List[Set[str]] = []
    for fid in by_id:
        if fid in seen:
            continue
        stack = [fid]
        comp: Set[str] = set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            comp.add(cur)
            stack.extend(neighbors[cur] - seen)
        components.append(comp)
    return components


def group_score(members: Iterable[Dict[str, Any]]) -> int:
    score = 0
    cats = set()
    for f in members:
        category = categorize(f)
        cats.add(category)
        score = max(score, SEVERITY_WEIGHT.get(str(f.get("severity", "info")), 20) + CATEGORY_WEIGHT.get(category, 20))
        if f.get("confidence") is not None and float(f["confidence"]) < 0.5:
            score += 5
    if cats & STRUCTURAL:
        score += 25
    return score


def action_for(category: str, findings: List[Dict[str, Any]]) -> str:
    high_impact = category in STRUCTURAL or any(f.get("severity") == "error" for f in findings)
    low_conf = any(f.get("confidence") is not None and float(f["confidence"]) < 0.65 for f in findings)
    if high_impact or low_conf:
        return "ask_or_inspect"
    return "fix_and_log"


def triage(manifest: Dict[str, Any]) -> Dict[str, Any]:
    findings = list(manifest.get("findings", []))
    by_id = {f["id"]: f for f in findings}
    groups = []
    for idx, comp in enumerate(build_components(findings), 1):
        members = [by_id[fid] for fid in sorted(comp)]
        categories = [categorize(f) for f in members]
        category = max(set(categories), key=lambda c: CATEGORY_WEIGHT.get(c, 0))
        locations = sorted({str(f.get("location", "")) for f in members})
        score = group_score(members)
        groups.append({
            "group_id": f"g{idx:03d}",
            "category": category,
            "priority_score": score,
            "finding_ids": [f["id"] for f in members],
            "locations": locations,
            "recommended_action": action_for(category, members),
            "reason": f"Grouped by related ids and shared {category} context; structural/dependent items are prioritized before leaf fixes."
        })
    groups.sort(key=lambda g: (-g["priority_score"], g["group_id"]))
    return {
        "document_path": manifest.get("document_path"),
        "document_type": manifest.get("document_type"),
        "groups": groups,
        "ordered_finding_ids": [fid for g in groups for fid in g["finding_ids"]]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create grouped stage 4 accessibility work plan.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON. This is the default output.")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    print(json.dumps(triage(manifest), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
