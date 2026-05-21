#!/usr/bin/env python3
"""PDF page-composition analyzer for docx-enhanced.

Gap 4 fix (part 2): analyze an exported PDF to catch layout problems that OOXML
linting can't reliably detect.

It uses:
- LibreOffice (optional) to export DOCX -> PDF
- pdftotext -bbox-layout (Poppler) to get per-word bounding boxes

Checks (heuristics):
- Header/footer collisions (body text overlapping header/footer bands)
- Orphan headings (a heading near the bottom of a page with < N body lines after it)
- Likely missing repeating table header rows for long tables (requires the DOCX)

This tool is best-effort: it errs on the side of warnings and is designed to
help an agent spot issues quickly.

Usage:
    python scripts/qa/page_composition.py --pdf out.pdf --style business --docx out.docx
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = {"w": W_NS}
XHTML_NS = "http://www.w3.org/1999/xhtml"
H = {"h": XHTML_NS}


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


def _page_size_in(spec: Dict[str, Any]) -> Tuple[float, float]:
    size = str(spec.get("page", {}).get("size", "Letter")).lower().strip()
    if size == "a4":
        return (8.2677, 11.6929)
    return (8.5, 11.0)


def _margins_in(spec: Dict[str, Any]) -> Dict[str, float]:
    m = spec.get("page", {}).get("margins_in", {}) or {}
    return {
        "top": float(m.get("top", 1.0)),
        "bottom": float(m.get("bottom", 1.0)),
        "left": float(m.get("left", 1.0)),
        "right": float(m.get("right", 1.0)),
    }


def inches_to_points(inches: float) -> float:
    return inches * 72.0


def run_pdftotext_bbox(pdf_path: Path, out_xhtml: Path) -> None:
    # pdftotext accepts output file path (not stdout) for bbox output.
    subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf_path), str(out_xhtml)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


@dataclass
class Line:
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    text: str


def parse_bbox_xhtml(xhtml_path: Path) -> List[Dict[str, Any]]:
    root = ET.fromstring(xhtml_path.read_bytes())
    pages_out: List[Dict[str, Any]] = []
    for p_idx, page in enumerate(root.findall(".//h:page", H), start=1):
        width = float(page.get("width", "0"))
        height = float(page.get("height", "0"))

        lines: List[Line] = []
        for line in page.findall(".//h:line", H):
            words = [w.text for w in line.findall("./h:word", H) if w.text]
            text = " ".join(words).strip()
            if not text:
                continue
            lines.append(
                Line(
                    x_min=float(line.get("xMin", "0")),
                    y_min=float(line.get("yMin", "0")),
                    x_max=float(line.get("xMax", "0")),
                    y_max=float(line.get("yMax", "0")),
                    text=text,
                )
            )

        # Stable order for analysis
        lines.sort(key=lambda l: (l.y_min, l.x_min))
        pages_out.append({"page": p_idx, "width": width, "height": height, "lines": lines})
    return pages_out


def normalize_text(s: str) -> str:
    return " ".join(s.split()).strip()


def extract_headings_from_docx(docx_path: Path) -> List[str]:
    headings: List[str] = []
    with zipfile.ZipFile(docx_path, "r") as z:
        doc_xml = z.read("word/document.xml")
    root = ET.fromstring(doc_xml)

    for p in root.findall(".//w:p", W):
        ppr = p.find("./w:pPr", W)
        if ppr is None:
            continue
        pstyle = ppr.find("./w:pStyle", W)
        if pstyle is None:
            continue
        style_id = pstyle.get(f"{{{W_NS}}}val")
        if not style_id:
            continue
        if style_id.startswith("Heading") and style_id[7:].isdigit():
            # Get concatenated text
            parts = [t.text for t in p.findall(".//w:t", W) if t.text]
            text = normalize_text("".join(parts))
            if text:
                headings.append(text)
    return headings


def extract_table_header_labels(docx_path: Path) -> List[List[str]]:
    """Return a list of header label lists (one per table)."""
    tables: List[List[str]] = []
    with zipfile.ZipFile(docx_path, "r") as z:
        doc_xml = z.read("word/document.xml")
    root = ET.fromstring(doc_xml)

    for tbl in root.findall(".//w:tbl", W):
        rows = tbl.findall("./w:tr", W)
        if not rows:
            continue
        first = rows[0]
        cells = first.findall("./w:tc", W)
        labels: List[str] = []
        for tc in cells:
            parts = [t.text for t in tc.findall(".//w:t", W) if t.text]
            txt = normalize_text("".join(parts))
            if txt:
                labels.append(txt)
        if labels:
            tables.append(labels)
    return tables


def estimate_rows_per_page(spec: Dict[str, Any]) -> int:
    # Very rough heuristic based on body area height / table line height.
    page_w_in, page_h_in = _page_size_in(spec)
    margins = _margins_in(spec)
    content_h_pt = inches_to_points(page_h_in - margins["top"] - margins["bottom"])

    # Use table font size if available, else body size, else 11.
    table_styles = spec.get("tableStyles") or {}
    # pick first style
    font_pt = None
    for _, tdef in table_styles.items():
        if isinstance(tdef, dict):
            f = tdef.get("font") or {}
            if isinstance(f, dict) and isinstance(f.get("size_pt"), (int, float)):
                font_pt = float(f["size_pt"])
                break
    if font_pt is None:
        body = (spec.get("fonts") or {}).get("body") or {}
        font_pt = float(body.get("size_pt", 11.0)) if isinstance(body, dict) else 11.0

    line_mult = 1.15
    line_h = font_pt * line_mult
    if line_h <= 0:
        return 30
    # Leave space for caption and header row
    return max(10, int(content_h_pt // line_h) - 6)


def analyze(pdf_path: Path, spec: Dict[str, Any], docx_path: Optional[Path] = None) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []

    # Create bbox XHTML
    with tempfile.TemporaryDirectory() as td:
        xhtml = Path(td) / "bbox.xhtml"
        run_pdftotext_bbox(pdf_path, xhtml)
        pages = parse_bbox_xhtml(xhtml)

    # Spec-derived body band
    margins = _margins_in(spec)
    body_top_pt = inches_to_points(margins["top"])
    # page height comes from PDF itself
    min_gap_pt = 4.0
    overlap_tol = 2.0

    heading_texts: List[str] = []
    heading_set: set[str] = set()
    table_headers: List[List[str]] = []
    rows_per_page_est: Optional[int] = None
    if docx_path and docx_path.exists():
        heading_texts = [normalize_text(h) for h in extract_headings_from_docx(docx_path)]
        heading_set = {h.lower() for h in heading_texts if h}
        table_headers = extract_table_header_labels(docx_path)
        rows_per_page_est = estimate_rows_per_page(spec)

    def is_heading_candidate(line_text: str) -> bool:
        t = normalize_text(line_text)
        if not t:
            return False
        low = t.lower()
        if low in heading_set:
            return True
        # Wrapped heading line: prefix match
        if heading_texts and len(t) >= 12:
            for h in heading_texts:
                if h.lower().startswith(low):
                    return True
        # Heuristic fallback (if docx not provided)
        if not heading_texts:
            if len(t) <= 80 and t.isupper() and any(c.isalpha() for c in t):
                return True
            import re

            if re.match(r"^\d+(\.\d+)*\s+\S+", t) and len(t) <= 120:
                return True
        return False

    # Collect page text for table header matching
    page_text_lower: Dict[int, str] = {}
    for p in pages:
        page_text_lower[p["page"]] = "\n".join([ln.text for ln in p["lines"]]).lower()

    # Per-page analysis
    for p in pages:
        pno = p["page"]
        height = p["height"] or 792.0
        body_bottom_pt = height - inches_to_points(margins["bottom"])

        header_lines = [ln for ln in p["lines"] if ln.y_max <= body_top_pt - overlap_tol]
        body_lines = [ln for ln in p["lines"] if ln.y_min >= body_top_pt + overlap_tol and ln.y_max <= body_bottom_pt - overlap_tol]
        footer_lines = [ln for ln in p["lines"] if ln.y_min >= body_bottom_pt + overlap_tol]

        # Collision: any line that crosses the body boundary
        for ln in p["lines"]:
            if ln.y_min < body_top_pt - overlap_tol and ln.y_max > body_top_pt + overlap_tol:
                issues.append(
                    {
                        "severity": "WARN",
                        "code": "HEADER_BODY_OVERLAP",
                        "page": pno,
                        "message": "A text line overlaps the header/body boundary (possible header collision).",
                        "sample": ln.text[:120],
                    }
                )
                break

        for ln in p["lines"]:
            if ln.y_min < body_bottom_pt - overlap_tol and ln.y_max > body_bottom_pt + overlap_tol:
                issues.append(
                    {
                        "severity": "WARN",
                        "code": "BODY_FOOTER_OVERLAP",
                        "page": pno,
                        "message": "A text line overlaps the body/footer boundary (possible footer collision).",
                        "sample": ln.text[:120],
                    }
                )
                break

        # Gap check (too tight)
        if header_lines and body_lines:
            max_header = max(ln.y_max for ln in header_lines)
            min_body = min(ln.y_min for ln in body_lines)
            if min_body - max_header < min_gap_pt:
                issues.append(
                    {
                        "severity": "INFO",
                        "code": "HEADER_BODY_GAP_SMALL",
                        "page": pno,
                        "message": f"Header-to-body gap is small ({min_body - max_header:.1f} pt).",
                    }
                )

        if footer_lines and body_lines:
            min_footer = min(ln.y_min for ln in footer_lines)
            max_body = max(ln.y_max for ln in body_lines)
            if min_footer - max_body < min_gap_pt:
                issues.append(
                    {
                        "severity": "INFO",
                        "code": "BODY_FOOTER_GAP_SMALL",
                        "page": pno,
                        "message": f"Body-to-footer gap is small ({min_footer - max_body:.1f} pt).",
                    }
                )

        # Orphan headings
        # Consider heading candidates within body region, close to bottom.
        bottom_zone = body_bottom_pt - inches_to_points(1.25)  # last ~1.25 in
        body_lines_sorted = sorted(body_lines, key=lambda l: l.y_min)
        for i, ln in enumerate(body_lines_sorted):
            if ln.y_max < bottom_zone:
                continue
            if not is_heading_candidate(ln.text):
                continue
            # Count non-empty body lines after it on the same page.
            after = [x for x in body_lines_sorted[i + 1 :] if normalize_text(x.text)]
            if len(after) < 2:
                issues.append(
                    {
                        "severity": "WARN",
                        "code": "ORPHAN_HEADING_POSSIBLE",
                        "page": pno,
                        "message": "Heading near bottom of page with fewer than 2 body lines following. Consider keep-with-next or manual page break.",
                        "heading": ln.text[:160],
                    }
                )

    # Table header repetition heuristics
    if docx_path and rows_per_page_est is not None:
        # Estimate table sizes from docx row count
        with zipfile.ZipFile(docx_path, "r") as z:
            doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)
        tables = root.findall(".//w:tbl", W)

        for t_idx, tbl in enumerate(tables):
            rows = tbl.findall("./w:tr", W)
            row_count = len(rows)
            if row_count <= rows_per_page_est:
                continue  # likely single-page
            labels = table_headers[t_idx] if t_idx < len(table_headers) else []
            if not labels:
                continue
            # Determine pages containing (most of) the header labels
            hit_pages: List[int] = []
            for pno, txt in page_text_lower.items():
                hits = sum(1 for lab in labels if lab.lower() in txt)
                if hits >= max(2, min(len(labels), 3)):
                    hit_pages.append(pno)

            if len(hit_pages) <= 1:
                issues.append(
                    {
                        "severity": "WARN",
                        "code": "TABLE_HEADER_REPEAT_POSSIBLE",
                        "message": "A long table (many rows) may be spanning pages, but header labels were only detected on one page. Ensure the header row repeats.",
                        "table_index": t_idx,
                        "rows": row_count,
                        "header_labels_sample": labels[:4],
                    }
                )

    return {
        "pdf": str(pdf_path),
        "docx": str(docx_path) if docx_path else None,
        "style": spec.get("name"),
        "summary": {
            "warnings": sum(1 for i in issues if i["severity"] == "WARN"),
            "infos": sum(1 for i in issues if i["severity"] == "INFO"),
        },
        "issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="Path to PDF exported from DOCX")
    ap.add_argument("--style", default="business", help="Style spec: business|academic|technical or path to JSON spec")
    ap.add_argument("--docx", help="Optional DOCX source to improve heading/table detection")
    ap.add_argument("--json", dest="json_out", help="Write report JSON to this path")
    args = ap.parse_args()

    spec = load_style_spec(args.style)
    report = analyze(Path(args.pdf), spec, Path(args.docx) if args.docx else None)

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf8")
    else:
        print(json.dumps(report, indent=2))

    # Only fail hard if WARNs exist.
    return 1 if report["summary"]["warnings"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
