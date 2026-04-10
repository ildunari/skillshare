#!/usr/bin/env python3
"""Diff citations between two versions of a document.
Usage: python citation_integrity_check.py --before original.md --after edited.md --format brackets --output report.md
"""
import argparse, re
from collections import OrderedDict
from pathlib import Path

def _expand_bracket(m):
    inner, ids = m.group(1), []
    for part in inner.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            try: ids.extend(str(i) for i in range(int(lo), int(hi) + 1))
            except ValueError: ids.append(part)
        else: ids.append(part)
    return ids

def extract_brackets(text):
    results = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"\[([\d ,\-]+)\]", line):
            for cid in _expand_bracket(m):
                results.append({"id": cid.strip(), "ctx": line.strip(), "line": lineno})
    return results

def extract_author_year(text):
    results, pat = [], re.compile(r"\(([A-Z][A-Za-z'.  &]+(?:\s+et\s+al\.?)?),?\s*(\d{4}[a-z]?)\)")
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in pat.finditer(line):
            results.append({"id": f"{m.group(1).strip()}, {m.group(2)}", "ctx": line.strip(), "line": lineno})
    return results

EXTRACTORS = {"brackets": extract_brackets, "author-year": extract_author_year}
_REF_ENTRY = re.compile(r"^\s*\[(\d+)\]")

def extract_reference_list(text):
    ids, in_refs = set(), False
    for line in text.splitlines():
        low = line.lower().strip()
        if low in ("# references", "## references", "# bibliography", "## bibliography"):
            in_refs = True; continue
        if in_refs:
            if line.startswith("#"): break
            m = _REF_ENTRY.match(line)
            if m: ids.add(m.group(1))
    return ids

_QUANT = re.compile(
    r"(\d+\.?\d*\s*(%|fold|mg|μ[gLmM]|nm|mM|nM|μM|pg|ng|kDa|mL|±|p\s*[<=]))"
    r"|(\bp\s*[<=]\s*0\.\d+)|(CI\s*[=:])|(\d+\s*/\s*\d+)", re.I)

def severity(kind, ctx):
    if kind == "removed": return "P0" if _QUANT.search(ctx) else "P1"
    return "P1" if kind == "moved" else "P3"

def compare(before, after):
    def group(lst):
        d = OrderedDict()
        for c in lst: d.setdefault(c["id"], []).append(c)
        return d
    b, a, changes = group(before), group(after), []
    for cid, entries in b.items():
        if cid not in a:
            for e in entries:
                changes.append({"type": "removed", "id": cid, "sev": severity("removed", e["ctx"]),
                                "bline": e["line"], "ctx": e["ctx"]})
        else:
            bl, al = {e["line"] for e in entries}, {e["line"] for e in a[cid]}
            if bl != al:
                changes.append({"type": "moved", "id": cid, "sev": severity("moved", entries[0]["ctx"]),
                                "blines": sorted(bl), "alines": sorted(al), "ctx": entries[0]["ctx"]})
    for cid, entries in a.items():
        if cid not in b:
            for e in entries:
                changes.append({"type": "added", "id": cid, "sev": severity("added", e["ctx"]),
                                "aline": e["line"], "ctx": e["ctx"]})
    return changes

def report(changes, orphaned, fmt, bpath, apath):
    L = ["# Citation Integrity Report\n", "| Field | Value |", "|-------|-------|",
         f"| Before | `{bpath}` |", f"| After  | `{apath}` |",
         f"| Format | {fmt} |", f"| Total changes | {len(changes)} |", ""]
    for sev in ("P0", "P1", "P3"):
        sub = [c for c in changes if c["sev"] == sev]
        if not sub: continue
        L.append(f"## {sev} Changes\n")
        for c in sub:
            if c["type"] == "removed":
                L.append(f"- **REMOVED** citation `{c['id']}` (line {c['bline']})")
            elif c["type"] == "moved":
                L.append(f"- **MOVED** citation `{c['id']}` (lines {c['blines']} -> {c['alines']})")
            elif c["type"] == "added":
                L.append(f"- **ADDED** citation `{c['id']}` (line {c['aline']})")
            L.append(f"  > {c['ctx']}")
        L.append("")
    if orphaned:
        L.append("## Orphaned Citations\n")
        L.append("Citations in text but absent from reference list:\n")
        for cid in sorted(orphaned, key=lambda x: (not x.isdigit(), x)):
            L.append(f"- `{cid}`")
        L.append("")
    if not changes and not orphaned:
        L.append("No citation differences detected.\n")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description="Diff citations between document versions.")
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--format", choices=["brackets", "author-year"], default="brackets")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    bt, at = Path(args.before).read_text("utf-8"), Path(args.after).read_text("utf-8")
    ext = EXTRACTORS[args.format]
    bc, ac = ext(bt), ext(at)
    changes = compare(bc, ac)
    orphaned = set()
    if args.format == "brackets":
        ref_ids = extract_reference_list(at)
        if ref_ids: orphaned = {c["id"] for c in ac} - ref_ids
    out = report(changes, orphaned, args.format, args.before, args.after)
    if args.output:
        Path(args.output).write_text(out, "utf-8"); print(f"Report written to {args.output}")
    else: print(out)

if __name__ == "__main__":
    main()
