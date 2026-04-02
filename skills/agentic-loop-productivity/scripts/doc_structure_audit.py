#!/usr/bin/env python3
"""Validate document heading hierarchy and section completeness.
Usage: python doc_structure_audit.py --document paper.md --template NIH_R01 --output report.md
"""
import argparse, re
from pathlib import Path

TEMPLATES = {
    "NIH_R01": {"label": "NIH R01",
                "required": ["Specific Aims", "Significance", "Innovation", "Approach"]},
    "IMRAD":   {"label": "IMRAD",
                "required": ["Introduction", "Methods", "Results", "Discussion"]},
    "general": {"label": "General", "required": []},
}

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")

def parse_sections(text):
    lines = text.splitlines()
    secs = []
    for i, line in enumerate(lines, 1):
        m = _HEADING_RE.match(line)
        if m:
            secs.append({"level": len(m.group(1)), "title": m.group(2).strip(),
                         "line": i, "wc": 0})
    hlines = [s["line"] for s in secs]
    for idx, sec in enumerate(secs):
        end = hlines[idx + 1] - 1 if idx + 1 < len(hlines) else len(lines)
        sec["wc"] = len(" ".join(lines[sec["line"]:end]).split())
    return secs

def check_hierarchy(secs):
    issues = []
    for i in range(1, len(secs)):
        pl, cl = secs[i - 1]["level"], secs[i]["level"]
        if cl > pl + 1:
            issues.append({"type": "hierarchy_gap", "line": secs[i]["line"],
                "detail": f'Heading "{secs[i]["title"]}" is H{cl} but follows '
                          f'H{pl} "{secs[i-1]["title"]}" \u2014 missing H{pl+1}'})
    return issues

def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def check_required(secs, tpl_key):
    tpl = TEMPLATES.get(tpl_key)
    if not tpl: return []
    found = {_norm(s["title"]) for s in secs}
    return [{"type": "missing_section",
             "detail": f'Required section "{r}" not found (template: {tpl["label"]})'}
            for r in tpl["required"] if _norm(r) not in found]

_XREF1 = re.compile(r"(?:see(?:\s+the)?|in\s+the)\s+([A-Z][\w]+(?:\s+[A-Z][\w]+)*)\s+section", re.I)
_XREF2 = re.compile(r"\bsection\s+(?:on\s+)?([A-Z][\w]+(?:\s+[A-Z][\w]+)*)")
_STOP = frozenset({"this","that","each","next","previous","following","above","below",
                    "a","the","our","their","its","for","which","where","some","any"})

def check_dangling(text, secs):
    hnorms = {_norm(s["title"]) for s in secs}
    issues, seen = [], set()
    for pat in (_XREF1, _XREF2):
        for lineno, line in enumerate(text.splitlines(), 1):
            if _HEADING_RE.match(line): continue
            for m in pat.finditer(line):
                name = m.group(1).strip()
                n = _norm(name)
                if n in seen or n in _STOP or len(n) < 3: continue
                if n not in hnorms:
                    seen.add(n)
                    issues.append({"type": "dangling_ref", "line": lineno,
                        "detail": f'Cross-reference to "{name}" but no matching heading exists'})
    return issues

_TYPE_LABEL = {"hierarchy_gap": "Hierarchy Gap", "missing_section": "Missing Section",
               "dangling_ref": "Dangling Reference"}
_TYPE_ICON  = {"hierarchy_gap": "WARNING", "missing_section": "ERROR",
               "dangling_ref": "WARNING"}

def report(secs, hier, miss, dang, tpl_key, doc):
    tl = TEMPLATES.get(tpl_key, {}).get("label", tpl_key)
    tw = sum(s["wc"] for s in secs)
    L = ["# Document Structure Audit\n",
         "| Field | Value |", "|-------|-------|",
         f"| Document | `{doc}` |", f"| Template | {tl} |",
         f"| Total sections | {len(secs)} |", f"| Total words | {tw} |", "",
         "## Section Outline\n",
         "| Line | Level | Heading | Words |",
         "|------|-------|---------|-------|"]
    for s in secs:
        pad = "\u2003" * (s["level"] - 1)
        L.append(f"| {s['line']} | H{s['level']} | {pad}{s['title']} | {s['wc']} |")
    L.append("")
    all_issues = hier + miss + dang
    if all_issues:
        L.append("## Issues\n")
        for iss in all_issues:
            lab = _TYPE_LABEL.get(iss["type"], iss["type"])
            ico = _TYPE_ICON.get(iss["type"], "INFO")
            loc = f" (line {iss['line']})" if "line" in iss else ""
            L.append(f"- **[{ico}]** {lab}{loc}: {iss['detail']}")
        L.append("")
    else:
        L += ["## Issues\n", "No issues detected.\n"]
    L += ["## Summary\n",
          f"- Hierarchy violations: {len(hier)}",
          f"- Missing required sections: {len(miss)}",
          f"- Dangling cross-references: {len(dang)}", ""]
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description="Audit document structure and heading hierarchy.")
    ap.add_argument("--document", required=True)
    ap.add_argument("--template", choices=list(TEMPLATES.keys()), default="general")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    text = Path(args.document).read_text("utf-8")
    secs = parse_sections(text)
    h, m, d = check_hierarchy(secs), check_required(secs, args.template), check_dangling(text, secs)
    out = report(secs, h, m, d, args.template, args.document)
    if args.output:
        Path(args.output).write_text(out, "utf-8"); print(f"Report written to {args.output}")
    else: print(out)

if __name__ == "__main__":
    main()
