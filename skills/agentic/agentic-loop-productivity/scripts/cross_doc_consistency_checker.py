#!/usr/bin/env python3
"""Cross-document consistency checker. Compares metric values across files and flags discrepancies."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path


def read_file(path: Path) -> str:
    """Read text from .md, .txt, or .docx files."""
    if path.suffix == ".docx":
        try:
            from docx import Document  # type: ignore[import-untyped]
        except ImportError:
            sys.exit(f"Error: python-docx required for '{path}'. pip install python-docx")
        return "\n".join(p.text for p in Document(str(path)).paragraphs)
    return path.read_text(encoding="utf-8")


def extract_values(text: str, pattern: str) -> list[str]:
    """Return deduplicated match strings (joined capture groups or full match)."""
    vals: list[str] = []
    for m in re.finditer(pattern, text):
        g = m.groups()
        v = "-".join(g) if g else m.group(0)
        if v not in vals:
            vals.append(v)
    return vals


def build_matrix(files: list[Path], metrics: dict[str, str]) -> dict[str, dict[str, list[str]]]:
    """Return {metric: {filename: [values]}}."""
    matrix: dict[str, dict[str, list[str]]] = {}
    for metric, pat in metrics.items():
        matrix[metric] = {f.name: extract_values(read_file(f), pat) for f in files}
    return matrix


def find_mismatches(matrix: dict[str, dict[str, list[str]]]) -> list[dict[str, str]]:
    """Return mismatch records with severity."""
    issues: list[dict[str, str]] = []
    for metric, fv in matrix.items():
        unique = {v for vals in fv.values() for v in vals}
        if len(unique) <= 1:
            continue
        detail = "; ".join(f"{fn}: {', '.join(vs) or '(not found)'}" for fn, vs in fv.items())
        issues.append({"metric": metric, "severity": "CRITICAL", "detail": detail})
    return issues


def render_report(matrix: dict[str, dict[str, list[str]]],
                  issues: list[dict[str, str]], files: list[Path]) -> str:
    """Render Markdown comparison report."""
    mm = {i["metric"] for i in issues}
    hdr = "| Metric | " + " | ".join(f.name for f in files) + " | Status |"
    sep = "|---" * (len(files) + 2) + "|"
    rows = [hdr, sep]
    for metric, fv in matrix.items():
        cells = " | ".join(", ".join(v) if v else "---" for v in fv.values())
        ok = metric not in mm
        rows.append(f"| {metric} | {cells} | {'checkmark OK' if ok else 'x CRITICAL'} |")
    lines = ["# Cross-Document Consistency Report\n"] + rows + ["\n## Summary\n"]
    if not issues:
        lines.append("All metrics are consistent across documents.")
    else:
        lines.append(f"**{len(issues)} mismatch(es) found:**\n")
        lines.extend(f"- **{i['severity']}** `{i['metric']}`: {i['detail']}" for i in issues)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare metrics across documents and flag discrepancies.")
    ap.add_argument("--files", nargs="+", required=True, type=Path,
                    help="Document paths to compare (.md, .txt, .docx).")
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--metrics", type=str,
                     help="JSON dict of metric_name -> regex pattern (with capture groups).")
    grp.add_argument("--metrics-file", type=Path,
                     help="Path to a JSON file containing the metrics dict.")
    ap.add_argument("--output", type=Path, default=None,
                    help="Path for the Markdown report (default: stdout).")
    args = ap.parse_args()

    for f in args.files:
        if not f.exists():
            sys.exit(f"Error: file not found: {f}")

    try:
        raw = args.metrics_file.read_text(encoding="utf-8") if args.metrics_file else args.metrics
        metrics: dict[str, str] = json.loads(raw)
    except (json.JSONDecodeError, OSError) as exc:
        sys.exit(f"Error loading metrics: {exc}")
    if not isinstance(metrics, dict) or not metrics:
        sys.exit("Error: metrics must be a non-empty JSON object {name: pattern}.")
    for name, pat in metrics.items():
        try:
            re.compile(pat)
        except re.error as exc:
            sys.exit(f"Error: invalid regex for metric '{name}': {exc}")

    matrix = build_matrix(args.files, metrics)
    issues = find_mismatches(matrix)
    report = render_report(matrix, issues, args.files)

    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Report written to {args.output} ({'mismatch' if issues else 'consistent'})")
    else:
        print(report)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
