#!/usr/bin/env python3
"""Regression tests for docx-enhanced.

Gap 10 fix: guard against regressions in tables + cover pages.

This is a light-weight test runner (no pytest dependency). It:
- Generates one template DOCX per style using scripts/create_template.js
- Unzips OOXML and checks invariants

Run:
  python tests/regression_test.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W_NS, "r": R_NS}


def qn(ns: str, tag: str) -> str:
    return f"{{{ns}}}{tag}"


def read_doc_xml(docx_path: Path, member: str) -> ET.Element:
    with zipfile.ZipFile(docx_path, "r") as z:
        return ET.fromstring(z.read(member))


def rels_map(docx_path: Path) -> Dict[str, str]:
    """Map rId -> target (relative path under word/)."""
    rels = read_doc_xml(docx_path, "word/_rels/document.xml.rels")
    out: Dict[str, str] = {}
    for rel in rels.findall(".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
        rid = rel.get("Id")
        target = rel.get("Target")
        if rid and target:
            out[rid] = target
    return out


def find_all_sectpr(doc_root: ET.Element) -> List[ET.Element]:
    return doc_root.findall(".//w:sectPr", NS)


def border_is_visible(border_el: Optional[ET.Element]) -> bool:
    if border_el is None:
        return False
    val = border_el.get(qn(W_NS, "val")) or border_el.get("val")
    if not val:
        return True
    return val.lower() not in {"none", "nil"}


def tbl_has_visible_borders(tbl: ET.Element) -> bool:
    tblpr = tbl.find("./w:tblPr", NS)
    if tblpr is None:
        return False
    borders = tblpr.find(".//w:tblBorders", NS)
    if borders is None:
        return False
    for b in list(borders):
        if border_is_visible(b):
            return True
    return False


def first_row_is_repeating_header(tbl: ET.Element) -> bool:
    rows = tbl.findall("./w:tr", NS)
    if not rows:
        return False
    trpr = rows[0].find("./w:trPr", NS)
    return trpr is not None and trpr.find("./w:tblHeader", NS) is not None


def inside_vertical_is_none(tbl: ET.Element) -> bool:
    tblpr = tbl.find("./w:tblPr", NS)
    if tblpr is None:
        return True
    iv = tblpr.find(".//w:tblBorders/w:insideV", NS)
    if iv is None:
        return True
    val = iv.get(qn(W_NS, "val")) or ""
    return val.lower() in {"none", "nil"}


@dataclass
class Failure:
    style: str
    message: str


def generate_doc(style: str, out_path: Path) -> None:
    cmd = [
        "node",
        "scripts/create_template.js",
        "--style",
        style,
        "--title",
        f"Regression {style} template",
        "--authors",
        "Jane Doe",
        "--output",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, cwd=Path(__file__).resolve().parents[1])


def test_cover_sections(style: str, docx_path: Path) -> List[Failure]:
    failures: List[Failure] = []
    doc = read_doc_xml(docx_path, "word/document.xml")
    sectprs = find_all_sectpr(doc)

    if style in {"business", "technical"}:
        if len(sectprs) < 2:
            failures.append(Failure(style, f"Expected >=2 sections (cover + body). Found {len(sectprs)}."))
            return failures
        # Body section should restart numbering at 1
        last = sectprs[-1]
        pgnum = last.find(".//w:pgNumType", NS)
        if pgnum is None or (pgnum.get(qn(W_NS, "start")) != "1"):
            failures.append(Failure(style, "Body section should restart page numbering at 1 (w:pgNumType w:start='1')."))

    return failures


def test_tables(style: str, docx_path: Path) -> List[Failure]:
    failures: List[Failure] = []
    doc = read_doc_xml(docx_path, "word/document.xml")
    tables = doc.findall(".//w:tbl", NS)
    if not tables:
        failures.append(Failure(style, "Expected at least one table in template."))
        return failures

    # For any visible-bordered table with >=2 rows, require repeating header and no vertical gridlines.
    for t in tables:
        rows = t.findall("./w:tr", NS)
        if len(rows) < 2:
            continue
        if not tbl_has_visible_borders(t):
            continue
        if not first_row_is_repeating_header(t):
            failures.append(Failure(style, "Visible-bordered data table is missing repeating header row (w:tblHeader)."))
        if not inside_vertical_is_none(t):
            failures.append(Failure(style, "Data table should not include vertical inside borders (insideV should be none)."))

    return failures


def test_header_footer_binding(style: str, docx_path: Path) -> List[Failure]:
    """Basic sanity: running header text should appear in a header part for business."""
    failures: List[Failure] = []
    if style != "business":
        return failures

    doc = read_doc_xml(docx_path, "word/document.xml")
    sectprs = find_all_sectpr(doc)
    if len(sectprs) < 2:
        return failures

    relmap = rels_map(docx_path)
    # Use last section (body) headerReference
    last = sectprs[-1]
    href = last.find("./w:headerReference[@w:type='default']", NS)
    if href is None:
        failures.append(Failure(style, "Expected default headerReference on body section."))
        return failures
    rid = href.get(qn(R_NS, "id"))
    if not rid or rid not in relmap:
        failures.append(Failure(style, "Could not resolve headerReference relationship id."))
        return failures
    target = relmap[rid]  # e.g., 'header1.xml'
    header_xml = read_doc_xml(docx_path, f"word/{target}")
    header_text = "".join([t.text or "" for t in header_xml.findall(".//w:t", NS)])
    if "Confidential" not in header_text:
        failures.append(Failure(style, "Business running header should contain 'Confidential' text in header part."))

    return failures


def main() -> int:
    failures: List[Failure] = []
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        for style in ("academic", "business", "technical"):
            out_docx = td_path / f"reg_{style}.docx"
            generate_doc(style, out_docx)
            failures.extend(test_cover_sections(style, out_docx))
            failures.extend(test_tables(style, out_docx))
            failures.extend(test_header_footer_binding(style, out_docx))

    if failures:
        for f in failures:
            print(f"[FAIL] {f.style}: {f.message}", file=sys.stderr)
        return 1

    print("All regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
