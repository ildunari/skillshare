#!/usr/bin/env python3
"""Scan files for deprecated values that should have been replaced.

Usage:
  python stale_value_finder.py --files f1.md f2.docx --deprecated '{"old": "new"}' --output report.md
  python stale_value_finder.py --files f1.md --deprecated-file stale_values.json --output report.md
"""
import argparse, json, os, re, sys
from pathlib import Path

QUANT_PATTERNS = re.compile(
    r"(%|\bparticle|\bconcentrat|\bviab|\byield|\bdose|\bcount|\bmean\b"
    r"|\bmedian\b|\bSD\b|\bSEM\b|\bp\s*[<=]|\bCI\b|\bfold\b|\bmL\b|\bμ[gLm])",
    re.IGNORECASE,
)
COMMENT_PATTERNS = re.compile(
    r"(<!-|^>\s|^\s*#\s*TODO|^\s*//|^\s*%|NOTE:|FIXME:|COMMENT:)", re.IGNORECASE
)

def read_text_file(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.readlines()

def read_docx_file(path: str) -> list[str]:
    try:
        from docx import Document
        doc = Document(path)
        return [p.text + "\n" for p in doc.paragraphs]
    except ImportError:
        pass
    try:
        from markitdown import MarkItDown
        md = MarkItDown()
        result = md.convert(path)
        return result.text_content.splitlines(keepends=True)
    except ImportError:
        print(f"WARNING: cannot read .docx '{path}' — install python-docx or markitdown", file=sys.stderr)
        return []


def read_file(path: str) -> list[str]:
    ext = Path(path).suffix.lower()
    if ext == ".docx":
        return read_docx_file(path)
    return read_text_file(path)

def classify_severity(context: str) -> str:
    if COMMENT_PATTERNS.search(context):
        return "INFO"
    if QUANT_PATTERNS.search(context):
        return "CRITICAL"
    return "WARNING"


def context_snippet(line: str, start: int, length: int, radius: int = 50) -> str:
    lo = max(0, start - radius)
    hi = min(len(line), start + length + radius)
    snippet = line[lo:hi].replace("\n", " ").strip()
    prefix = "..." if lo > 0 else ""
    suffix = "..." if hi < len(line) else ""
    return f"{prefix}{snippet}{suffix}"


def search_file(filepath: str, deprecated: dict, case_insensitive: bool) -> list[dict]:
    if not os.path.isfile(filepath):
        print(f"ERROR: file not found — {filepath}", file=sys.stderr)
        return []
    lines = read_file(filepath)
    findings: list[dict] = []
    flags = re.IGNORECASE if case_insensitive else 0
    for old_val, new_val in deprecated.items():
        pattern = re.compile(re.escape(old_val), flags)
        for lineno, line in enumerate(lines, start=1):
            for m in pattern.finditer(line):
                ctx = context_snippet(line, m.start(), len(old_val))
                findings.append({
                    "file": filepath,
                    "line": lineno,
                    "old": old_val,
                    "new": new_val,
                    "context": ctx,
                    "severity": classify_severity(ctx),
                })
    return findings

def build_report(findings: list[dict]) -> str:
    if not findings:
        return "# Stale Value Report\n\nNo stale values found.\n"
    lines = ["# Stale Value Report\n"]
    lines.append(f"**{len(findings)} finding(s)** across "
                 f"{len({f['file'] for f in findings})} file(s).\n")
    crit = sum(1 for f in findings if f["severity"] == "CRITICAL")
    if crit:
        lines.append(f"> {crit} CRITICAL finding(s) in quantitative context.\n")
    by_file: dict[str, list[dict]] = {}
    for f in findings:
        by_file.setdefault(f["file"], []).append(f)
    for fp, hits in by_file.items():
        lines.append(f"\n## `{fp}`\n")
        lines.append("| Line | Severity | Stale Value | Replacement | Context |")
        lines.append("|------|----------|-------------|-------------|---------|")
        for h in sorted(hits, key=lambda x: x["line"]):
            ctx_escaped = h["context"].replace("|", "\\|")
            lines.append(
                f"| {h['line']} | **{h['severity']}** "
                f"| `{h['old']}` | `{h['new']}` | {ctx_escaped} |"
            )
    return "\n".join(lines) + "\n"

def main() -> int:
    ap = argparse.ArgumentParser(description="Find stale/deprecated values in files.")
    ap.add_argument("--files", nargs="+", required=True, help="Files to scan.")
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--deprecated", type=str, help="JSON dict of old→new pairs.")
    grp.add_argument("--deprecated-file", type=str, help="Path to JSON file of old→new pairs.")
    ap.add_argument("--output", type=str, default=None, help="Output markdown report path.")
    ap.add_argument("--case-insensitive", "-i", action="store_true", help="Case-insensitive matching.")
    args = ap.parse_args()

    if args.deprecated:
        deprecated = json.loads(args.deprecated)
    else:
        with open(args.deprecated_file, encoding="utf-8") as f:
            deprecated = json.load(f)
    if not isinstance(deprecated, dict):
        print("ERROR: deprecated values must be a JSON object (old→new).", file=sys.stderr)
        return 2

    all_findings: list[dict] = []
    for fp in args.files:
        all_findings.extend(search_file(fp, deprecated, args.case_insensitive))

    report = build_report(all_findings)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    return 1 if all_findings else 0

if __name__ == "__main__":
    sys.exit(main())
