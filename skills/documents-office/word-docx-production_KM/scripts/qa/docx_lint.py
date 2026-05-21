#!/usr/bin/env python3
"""DOCX structural linter for docx-enhanced.

Gap 4 fix: automate checks that are painful to eyeball in Word.

This linter is intentionally conservative:
- It looks for common failure modes (bad heading levels, missing table header repetition,
  direct paragraph formatting overrides, tracked changes).
- It does not try to enforce every stylistic preference.

It works by unzipping the DOCX and reading OOXML (document.xml, styles.xml, settings.xml).

Usage:
    python scripts/qa/docx_lint.py --docx out.docx --style business

Exit code:
- 0 if no errors (warnings are allowed)
- 1 if errors exist (or --fail-on warn)
"""

from __future__ import annotations

import argparse
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def qn(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def load_style_spec(name_or_path: str) -> Dict[str, Any]:
    p = Path(name_or_path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf8"))

    aliases = {
        "academic": "academic_manuscript_generic",
        "business": "business_report_modern",
        "technical": "technical_report_engineering",
    }
    name = aliases.get(name_or_path, name_or_path)
    spec_path = Path(__file__).resolve().parents[2] / "assets" / "style-specs" / f"{name}.json"
    if not spec_path.exists():
        raise FileNotFoundError(f"Style spec not found: {spec_path}")
    return json.loads(spec_path.read_text(encoding="utf8"))


def get_text(el: ET.Element) -> str:
    """Concatenate all w:t descendants in order."""
    parts: List[str] = []
    for t in el.findall(".//w:t", NS):
        if t.text:
            parts.append(t.text)
    return "".join(parts).strip()


def heading_level_from_style_id(style_id: Optional[str]) -> Optional[int]:
    if not style_id:
        return None
    # Typical ids: Heading1, Heading2, Heading3
    if style_id.startswith("Heading") and style_id[7:].isdigit():
        return int(style_id[7:])
    return None


@dataclass
class Issue:
    severity: str  # ERROR | WARN | INFO
    code: str
    message: str
    location: Optional[Dict[str, Any]] = None


def add_issue(
    issues: List[Issue],
    severity: str,
    code: str,
    message: str,
    location: Optional[Dict[str, Any]] = None,
) -> None:
    issues.append(Issue(severity=severity, code=code, message=message, location=location))


def lint_docx(docx_path: Path, spec: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Issue] = []

    if not docx_path.exists():
        raise FileNotFoundError(docx_path)

    with zipfile.ZipFile(docx_path, "r") as z:

        def read_xml(member: str) -> Optional[ET.Element]:
            try:
                data = z.read(member)
            except KeyError:
                return None
            return ET.fromstring(data)

        document = read_xml("word/document.xml")
        styles = read_xml("word/styles.xml")
        settings = read_xml("word/settings.xml")

        if document is None:
            raise RuntimeError("DOCX missing word/document.xml")

        # ------------------------------------
        # Tracked changes detection
        # ------------------------------------
        has_ins = document.find(".//w:ins", NS) is not None
        has_del = document.find(".//w:del", NS) is not None
        has_move = (document.find(".//w:moveFrom", NS) is not None) or (document.find(".//w:moveTo", NS) is not None)
        if has_ins or has_del or has_move:
            add_issue(
                issues,
                "WARN",
                "TRACKED_CHANGES_PRESENT",
                "Document contains tracked changes (w:ins/w:del/w:move*). Consider accepting/rejecting or converting via the tracked-changes preflight.",
            )

        if settings is not None:
            track = settings.find(".//w:trackRevisions", NS)
            if track is not None:
                add_issue(
                    issues,
                    "INFO",
                    "TRACK_REVISIONS_ENABLED",
                    "Document settings enable Track Revisions (w:trackRevisions).",
                )

        # ------------------------------------
        # Paragraph scan (styles, headings, direct formatting)
        # ------------------------------------
        paragraph_style_counts: Dict[str, int] = {}
        headings: List[Tuple[int, str, int]] = []  # (level, text, paragraph_index)

        forbidden_ppr_tags = {
            "spacing",
            "ind",
                        "tabs",
            "shd",
            "pBdr",
            "framePr",
            "textDirection",
        }
        allowed_ppr_tags = {
            "pStyle",
            "numPr",
            "sectPr",
            "keepNext",
            "keepLines",
            "widowControl",
            "outlineLvl",
            "pageBreakBefore",
            "contextualSpacing",
            "jc",
        }

        for idx, p in enumerate(document.findall(".//w:p", NS)):
            ppr = p.find("./w:pPr", NS)
            style_id = None
            if ppr is not None:
                pstyle = ppr.find("./w:pStyle", NS)
                if pstyle is not None:
                    style_id = pstyle.get(qn("val"))
            if style_id:
                paragraph_style_counts[style_id] = paragraph_style_counts.get(style_id, 0) + 1

            text = get_text(p)
            hlevel = heading_level_from_style_id(style_id)
            if hlevel is not None and text:
                headings.append((hlevel, text, idx))

            # direct formatting overrides (heuristic)
            if ppr is not None:
                for child in list(ppr):
                    tag = child.tag.split("}")[-1]
                    if tag in forbidden_ppr_tags:
                        add_issue(
                            issues,
                            "WARN",
                            "DIRECT_PARAGRAPH_FORMATTING",
                            f"Paragraph has direct formatting <w:{tag}>; prefer styles instead.",
                            location={"paragraph_index": idx, "style_id": style_id, "text": text[:80]},
                        )
                    elif tag not in allowed_ppr_tags:
                        add_issue(
                            issues,
                            "INFO",
                            "PARAGRAPH_PROPERTY_PRESENT",
                            f"Paragraph has property <w:{tag}> (may be fine).",
                            location={"paragraph_index": idx, "style_id": style_id, "text": text[:80]},
                        )

        # Heading sequencing checks
        if not headings:
            add_issue(issues, "WARN", "NO_HEADINGS", "No Heading1/Heading2/Heading3 paragraphs detected.")
        else:
            first_level = headings[0][0]
            if first_level != 1:
                add_issue(
                    issues,
                    "WARN",
                    "FIRST_HEADING_NOT_H1",
                    f"First detected heading is Heading{first_level}; expected Heading1.",
                    location={"paragraph_index": headings[0][2], "text": headings[0][1]},
                )

            prev = first_level
            for level, text, pidx in headings[1:]:
                if level > prev + 1:
                    add_issue(
                        issues,
                        "WARN",
                        "HEADING_LEVEL_SKIP",
                        f"Heading level jumps from Heading{prev} to Heading{level}.",
                        location={"paragraph_index": pidx, "text": text},
                    )
                prev = level

        # ------------------------------------
        # Style usage / unused styles
        # ------------------------------------
        defined_styles: Dict[str, str] = {}  # id -> name
        if styles is not None:
            for st in styles.findall(".//w:style", NS):
                style_id = st.get(qn("styleId"))
                if not style_id:
                    continue
                name_el = st.find("./w:name", NS)
                name = name_el.get(qn("val")) if name_el is not None else style_id
                defined_styles[style_id] = name

        required = set((spec.get("paragraphStyles") or {}).keys())
        missing = sorted([s for s in required if s not in defined_styles])
        if missing:
            add_issue(
                issues,
                "ERROR",
                "MISSING_REQUIRED_STYLES",
                f"Document is missing required styles from the selected style system: {', '.join(missing)}",
            )

        used = set(paragraph_style_counts.keys())
        unused_custom = [sid for sid in defined_styles.keys() if sid not in used and sid not in {"Normal"}]
        if unused_custom:
            add_issue(
                issues,
                "INFO",
                "UNUSED_STYLES",
                f"{len(unused_custom)} styles are defined but unused (example: {unused_custom[0]}).",
            )

        # ------------------------------------
        # Heading style properties (keepNext / outline level) in styles.xml
        # ------------------------------------
        if styles is not None:
            for hid in ["Heading1", "Heading2", "Heading3"]:
                st = styles.find(f".//w:style[@w:styleId='{hid}']", NS)
                if st is None:
                    continue
                ppr = st.find("./w:pPr", NS)
                if ppr is None:
                    continue
                if ppr.find("./w:keepNext", NS) is None:
                    add_issue(
                        issues,
                        "WARN",
                        "HEADING_STYLE_MISSING_KEEPNEXT",
                        f"{hid} style does not include <w:keepNext>. Orphan headings are more likely.",
                    )
                if ppr.find("./w:outlineLvl", NS) is None:
                    add_issue(
                        issues,
                        "WARN",
                        "HEADING_STYLE_MISSING_OUTLINE",
                        f"{hid} style does not include <w:outlineLvl>. TOC/outline may not work.",
                    )

        # ------------------------------------
        # Table checks (repeat header row)
        # ------------------------------------
        tables = document.findall(".//w:tbl", NS)
        for t_idx, tbl in enumerate(tables):
            # Skip layout tables (no explicit borders). Repeating header rows only matter for data tables.
            tblpr = tbl.find("./w:tblPr", NS)
            tbl_borders = tblpr.find(".//w:tblBorders", NS) if tblpr is not None else None
            if tbl_borders is None:
                continue

            # If all borders are NONE/NIL, treat as a layout table.
            visible_border = False
            for b in list(tbl_borders):
                val = b.get(qn("val"))
                if val and val.lower() not in {"none", "nil"}:
                    visible_border = True
                    break
            if not visible_border:
                continue

            rows = tbl.findall("./w:tr", NS)
            if len(rows) < 2:
                continue

            first = rows[0]
            trpr = first.find("./w:trPr", NS)
            has_header_flag = trpr is not None and trpr.find("./w:tblHeader", NS) is not None
            if not has_header_flag:
                add_issue(
                    issues,
                    "WARN",
                    "TABLE_HEADER_NOT_REPEATING",
                    "Table first row is not marked as a repeating header (<w:tblHeader/>).",
                    location={"table_index": t_idx, "rows": len(rows)},
                )

            inside_v = tblpr.find(".//w:tblBorders/w:insideV", NS) if tblpr is not None else None
            if inside_v is not None:
                add_issue(
                    issues,
                    "INFO",
                    "TABLE_VERTICAL_BORDERS",
                    "Table defines inside vertical borders (<w:insideV>). If you want a cleaner look, remove vertical gridlines.",
                    location={"table_index": t_idx},
                )

        # ------------------------------------
        # Section margins vs style spec (first section only)
        # ------------------------------------
        sectpr = document.find(".//w:sectPr", NS)
        if sectpr is not None:
            pgmar = sectpr.find("./w:pgMar", NS)
            if pgmar is not None:

                def _twips(attr: str) -> Optional[int]:
                    v = pgmar.get(qn(attr))
                    if v is None:
                        return None
                    try:
                        return int(v)
                    except Exception:
                        return None

                top = _twips("top")
                left = _twips("left")
                right = _twips("right")
                bottom = _twips("bottom")

                margins_in = spec.get("page", {}).get("margins_in", {})
                exp = {
                    "top": int(round(float(margins_in.get("top", 1.0)) * 1440)),
                    "left": int(round(float(margins_in.get("left", 1.0)) * 1440)),
                    "right": int(round(float(margins_in.get("right", 1.0)) * 1440)),
                    "bottom": int(round(float(margins_in.get("bottom", 1.0)) * 1440)),
                }

                tol = 60  # twips (~0.04in)
                for k, got in [("top", top), ("left", left), ("right", right), ("bottom", bottom)]:
                    if got is None:
                        continue
                    if abs(got - exp[k]) > tol:
                        add_issue(
                            issues,
                            "WARN",
                            "SECTION_MARGIN_MISMATCH",
                            f"Section margin {k} is {got} twips; expected about {exp[k]} twips for this style system.",
                        )

    errors = sum(1 for i in issues if i.severity == "ERROR")
    warnings = sum(1 for i in issues if i.severity == "WARN")
    infos = sum(1 for i in issues if i.severity == "INFO")

    return {
        "docx": str(docx_path),
        "style": spec.get("name"),
        "summary": {"errors": errors, "warnings": warnings, "infos": infos},
        "issues": [
            {"severity": i.severity, "code": i.code, "message": i.message, "location": i.location}
            for i in issues
        ],
        "stats": {
            "paragraphStylesUsed": paragraph_style_counts,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True, help="Path to .docx")
    ap.add_argument("--style", default="business", help="Style spec: business|academic|technical or path to JSON spec")
    ap.add_argument("--json", dest="json_out", help="Write report JSON to this path")
    ap.add_argument("--fail-on", choices=["error", "warn", "info"], default="error", help="Exit non-zero at this severity")
    args = ap.parse_args()

    spec = load_style_spec(args.style)
    report = lint_docx(Path(args.docx), spec)

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf8")
    else:
        print(json.dumps(report, indent=2))

    sev_order = {"info": 1, "warn": 2, "error": 3}
    threshold = sev_order[args.fail_on]
    if report["summary"]["errors"] > 0 and threshold <= sev_order["error"]:
        return 1
    if report["summary"]["warnings"] > 0 and threshold <= sev_order["warn"]:
        return 1
    if report["summary"]["infos"] > 0 and threshold <= sev_order["info"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())