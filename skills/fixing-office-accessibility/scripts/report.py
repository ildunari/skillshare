#!/usr/bin/env python3
"""Create human-readable and JSON accessibility remediation reports."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

RULE_TO_WCAG = {
    "ALT": ["1.1.1"],
    "DECORATIVE": ["1.1.1"],
    "TABLE": ["1.3.1"],
    "MERGED": ["1.3.1"],
    "READING_ORDER": ["1.3.2"],
    "FLOATING": ["1.3.2"],
    "HEADING": ["1.3.1", "2.4.6", "2.4.10"],
    "CONTRAST": ["1.4.3"],
    "NON_TEXT": ["1.4.11"],
    "LINK": ["2.4.6"],
    "SLIDE_TITLE": ["2.4.6", "2.4.10"],
    "LANG": ["3.1.1"],
    "FORM": ["4.1.2"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_jsonl(path: Optional[Path]) -> List[Dict[str, Any]]:
    if not path or not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def infer_wcag(rule_id: str) -> List[str]:
    hits: Set[str] = set()
    upper = rule_id.upper()
    for key, values in RULE_TO_WCAG.items():
        if key in upper:
            hits.update(values)
    return sorted(hits)


def changes_from_log(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    changes: List[Dict[str, Any]] = []
    for row in rows:
        if row.get("type") == "change":
            changes.append(row)
        elif row.get("type") == "officecli_batch":
            for cmd in row.get("commands", []):
                props = cmd.get("props") or cmd.get("properties") or {}
                changes.append({
                    "finding_id": cmd.get("finding_id", "unknown"),
                    "rule_id": cmd.get("rule_id", "unknown"),
                    "location": cmd.get("path", cmd.get("parent", "/")),
                    "operation": cmd.get("command", cmd.get("op", "set")),
                    "before": cmd.get("before"),
                    "after": props,
                    "officecli_commands": [cmd],
                    "rationale": cmd.get("rationale", "Applied OfficeCLI batch command from stage 4 remediation."),
                    "wcag_criteria": cmd.get("wcag_criteria") or infer_wcag(str(cmd.get("rule_id", ""))),
                    "decision_source": cmd.get("decision_source", "agent_high_confidence"),
                })
    return changes


def latest_validation(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    for row in reversed(rows):
        if row.get("validation_status"):
            status = dict(row["validation_status"])
            status.setdefault("restored_from_backup", bool(row.get("restored_from_backup")))
            return status
    return {"passed": False, "command": "officecli validate not run", "stdout": "", "stderr": ""}


def backup_path(rows: List[Dict[str, Any]]) -> Optional[str]:
    for row in reversed(rows):
        if row.get("backup_path"):
            return row["backup_path"]
    return None


def build_report(manifest: Dict[str, Any], rows: List[Dict[str, Any]], manifest_path: Optional[str]) -> Dict[str, Any]:
    changes = changes_from_log(rows)
    wcag = sorted({crit for c in changes for crit in c.get("wcag_criteria", [])})
    unresolved_count = max(0, len(manifest.get("findings", [])) - len({c.get("finding_id") for c in changes}))
    summary = (
        f"Stage 4 accessibility remediation processed {len(manifest.get('findings', []))} residual findings "
        f"for {manifest.get('document_path', 'the document')}. {len(changes)} changes were committed, "
        f"covering {', '.join(wcag) if wcag else 'no WCAG criteria yet'}, with {unresolved_count} item(s) not recorded as committed."
    )
    return {
        "schema_version": "1.0.0",
        "generated_at": utc_now(),
        "document_path": manifest.get("document_path", ""),
        "manifest_path": manifest_path,
        "executive_summary": summary,
        "changes_committed": changes,
        "changes_user_approved": [r for r in rows if r.get("type") == "user_approved"],
        "changes_user_declined": [r for r in rows if r.get("type") == "user_declined"],
        "items_deferred": [r for r in rows if r.get("type") == "deferred"],
        "wcag_criteria_addressed": wcag,
        "validation_status": latest_validation(rows),
        "file_backup_path": backup_path(rows),
    }


def markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# Office Accessibility Stage 4 Report",
        "",
        "## Executive summary",
        report["executive_summary"],
        "",
        "## Changes committed",
        "",
        "| Finding | Rule | Location | Operation | WCAG |",
        "|---|---|---|---|---|",
    ]
    for c in report["changes_committed"]:
        lines.append(
            f"| {c.get('finding_id','')} | {c.get('rule_id','')} | {c.get('location','')} | "
            f"{c.get('operation','')} | {', '.join(c.get('wcag_criteria', []))} |"
        )
    if not report["changes_committed"]:
        lines.append("| — | — | — | No committed changes recorded | — |")
    lines.extend([
        "",
        "## Deferred or declined",
        f"Deferred: {len(report['items_deferred'])}",
        f"Declined: {len(report['changes_user_declined'])}",
        "",
        "## Validation",
        f"Passed: {report['validation_status'].get('passed')}",
        f"Command: `{report['validation_status'].get('command')}`",
        f"Backup: {report.get('file_backup_path') or 'not recorded'}",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit stage 4 accessibility remediation reports.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--change-log", type=Path, help="JSONL log from Claude/apply_batch.py")
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    rows = load_jsonl(args.change_log)
    report = build_report(manifest, rows, str(args.manifest))
    args.out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    args.out_md.write_text(markdown(report), encoding="utf-8")
    print(markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
