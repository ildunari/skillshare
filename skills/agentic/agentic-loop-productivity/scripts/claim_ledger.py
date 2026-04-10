#!/usr/bin/env python3
"""Claim Ledger — track quantitative claims from source files through document editing.

Modes:
  create   Scan source files for numeric values matching patterns, produce a ledger JSON.
  verify   Compare a document against an existing ledger and flag drift / missing claims.
  report   Generate a markdown summary of ledger status.

Requires Python 3.9+, stdlib only.  Optional: python-docx for .docx support.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

NOW_ISO = datetime.now().replace(microsecond=0).isoformat()


# --- Helpers ---

def _read_text(path: Path) -> str:
    """Return the full text of a file (.md, .txt, or .docx if python-docx is available)."""
    if path.suffix.lower() == ".docx":
        if not HAS_DOCX:
            print(f"  [warn] python-docx not installed — skipping {path.name}")
            return ""
        doc = DocxDocument(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    return path.read_text(encoding="utf-8", errors="replace")


def _find_matches(text: str, patterns: list[str]) -> list[dict]:
    """Return all regex matches with surrounding context (up to 60 chars each side)."""
    hits: list[dict] = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            start = max(0, m.start() - 60)
            end = min(len(text), m.end() + 60)
            snippet = text[start:end].replace("\n", " ").strip()
            hits.append({
                "matched": m.group(),
                "span": (m.start(), m.end()),
                "context": snippet,
            })
    return hits


def _location_hint(text: str, pos: int) -> str:
    """Derive a rough location string (line number + nearby heading)."""
    before = text[:pos]
    line_no = before.count("\n") + 1
    # Walk backwards for a markdown heading
    heading = ""
    for line in reversed(before.splitlines()):
        if line.startswith("#"):
            heading = line.lstrip("# ").strip()
            break
    loc = f"line {line_no}"
    if heading:
        loc += f', under "{heading}"'
    return loc


# --- CREATE ---

def cmd_create(args):
    sources: list[Path] = [Path(s) for s in args.sources]
    patterns: list[str] = args.patterns
    missing = [s for s in sources if not s.exists()]
    if missing:
        print(f"Error: source file(s) not found: {', '.join(str(m) for m in missing)}")
        sys.exit(1)

    claims: list[dict] = []
    claim_idx = 1
    for src in sources:
        text = _read_text(src)
        if not text:
            continue
        hits = _find_matches(text, patterns)
        for h in hits:
            raw = re.sub(r"[^\d.eE+-]", "", h["matched"])
            claims.append({
                "id": f"C-{claim_idx:02d}",
                "text": h["context"],
                "raw_value": raw,
                "display_value": h["matched"],
                "source_file": src.name,
                "source_location": _location_hint(text, h["span"][0]),
                "status": "unverified",
                "last_checked": NOW_ISO,
            })
            claim_idx += 1

    ledger = {
        "created": NOW_ISO,
        "phase": args.phase or "",
        "claims": claims,
    }

    out = Path(args.output)
    out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Ledger created: {out}  ({len(claims)} claim(s) from {len(sources)} source(s))")


# --- VERIFY ---

def cmd_verify(args):
    ledger_path = Path(args.ledger)
    doc_path = Path(args.document)
    for p, label in [(ledger_path, "ledger"), (doc_path, "document")]:
        if not p.exists():
            print(f"Error: {label} file not found: {p}")
            sys.exit(1)

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    doc_text = _read_text(doc_path)

    verified = 0
    drifted = 0
    missing = 0
    lines: list[str] = ["# Claim Verification Report", "", f"Document: `{doc_path.name}`",
                         f"Ledger: `{ledger_path.name}`", f"Checked: {NOW_ISO}", "",
                         "| ID | Display | Status | Detail |",
                         "|----|---------|--------|--------|"]

    for c in ledger.get("claims", []):
        display = c.get("display_value", "")
        cid = c["id"]
        if display and display in doc_text:
            c["status"] = "verified"
            c["last_checked"] = NOW_ISO
            verified += 1
            lines.append(f"| {cid} | {display} | verified | exact match found |")
        elif display and re.search(re.escape(c.get("raw_value", "impossible")), doc_text):
            c["status"] = "drifted"
            c["last_checked"] = NOW_ISO
            drifted += 1
            lines.append(f"| {cid} | {display} | drifted | raw value present but display differs |")
        else:
            c["status"] = "missing"
            c["last_checked"] = NOW_ISO
            missing += 1
            lines.append(f"| {cid} | {display} | MISSING | not found in document |")

    # Write updated ledger back
    ledger_path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write report
    report_path = Path(args.output)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    total = verified + drifted + missing
    print(f"Verification complete: {verified}/{total} verified, "
          f"{drifted} drifted, {missing} missing  ->  {report_path}")


# --- REPORT ---

def cmd_report(args):
    ledger_path = Path(args.ledger)
    if not ledger_path.exists():
        print(f"Error: ledger file not found: {ledger_path}")
        sys.exit(1)

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    claims = ledger.get("claims", [])

    counts = {"verified": 0, "drifted": 0, "missing": 0, "unverified": 0}
    for c in claims:
        counts[c.get("status", "unverified")] = counts.get(c.get("status", "unverified"), 0) + 1

    lines = [
        "# Claim Ledger Summary", "",
        f"**Created:** {ledger.get('created', 'unknown')}",
        f"**Phase:** {ledger.get('phase', '—')}",
        f"**Total claims:** {len(claims)}", "",
        "## Status Breakdown", "",
        f"- Verified: {counts['verified']}",
        f"- Drifted: {counts['drifted']}",
        f"- Missing: {counts['missing']}",
        f"- Unverified: {counts['unverified']}", "",
        "## Claims", "",
        "| ID | Display | Source | Status |",
        "|----|---------|--------|--------|",
    ]
    for c in claims:
        lines.append(
            f"| {c['id']} | {c.get('display_value','')} | {c.get('source_file','')} | {c.get('status','')} |"
        )

    out = Path(args.output)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written: {out}  ({len(claims)} claim(s))")
    print(f"  verified={counts['verified']}  drifted={counts['drifted']}  "
          f"missing={counts['missing']}  unverified={counts['unverified']}")


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Claim Ledger — track quantitative claims through document editing."
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # create
    p_create = sub.add_parser("create", help="Scan sources and build a new ledger")
    p_create.add_argument("--sources", nargs="+", required=True, help="Source files to scan")
    p_create.add_argument("--patterns", nargs="+", required=True, help="Regex patterns for numeric claims")
    p_create.add_argument("--output", required=True, help="Output ledger JSON path")
    p_create.add_argument("--phase", default="", help="Label for the current editing phase")
    p_create.set_defaults(func=cmd_create)

    # verify
    p_verify = sub.add_parser("verify", help="Verify claims in a document against the ledger")
    p_verify.add_argument("--ledger", required=True, help="Path to ledger JSON")
    p_verify.add_argument("--document", required=True, help="Document to verify against")
    p_verify.add_argument("--output", required=True, help="Output report path (.md)")
    p_verify.set_defaults(func=cmd_verify)

    # report
    p_report = sub.add_parser("report", help="Generate a markdown summary of the ledger")
    p_report.add_argument("--ledger", required=True, help="Path to ledger JSON")
    p_report.add_argument("--output", required=True, help="Output summary path (.md)")
    p_report.set_defaults(func=cmd_report)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
