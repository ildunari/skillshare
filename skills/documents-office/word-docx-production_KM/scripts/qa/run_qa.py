#!/usr/bin/env python3
"""Run the docx-enhanced QA pipeline.

Gap 4 fix (wrapper): one command to run OOXML lint + PDF composition checks.

It will:
1) Run docx_lint on the DOCX.
2) Export DOCX -> PDF using LibreOffice (unless --pdf is provided).
3) Run page_composition on the PDF.

Usage:
    python scripts/qa/run_qa.py --docx out.docx --style business --out out_qa.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import docx_lint
import page_composition


def convert_docx_to_pdf(docx_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", str(docx_path), "--outdir", str(out_dir)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    pdf_path = out_dir / (docx_path.stem + ".pdf")
    if not pdf_path.exists():
        raise FileNotFoundError(f"LibreOffice did not create expected PDF: {pdf_path}")
    return pdf_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True, help="Path to DOCX to QA")
    ap.add_argument("--style", default="business", help="Style spec: business|academic|technical or path to JSON spec")
    ap.add_argument("--pdf", help="Optional: use an existing PDF instead of converting")
    ap.add_argument("--skip-pdf", action="store_true", help="Skip PDF conversion and page composition checks")
    ap.add_argument("--out", help="Write combined report JSON to this path")
    ap.add_argument("--fail-on", choices=["error", "warn", "info"], default="error", help="Failure threshold for docx_lint")
    args = ap.parse_args()

    docx_path = Path(args.docx)
    spec = docx_lint.load_style_spec(args.style)

    lint_report = docx_lint.lint_docx(docx_path, spec)

    pdf_report: Optional[dict] = None
    pdf_path: Optional[Path] = None
    if not args.skip_pdf:
        if args.pdf:
            pdf_path = Path(args.pdf)
        else:
            with tempfile.TemporaryDirectory() as td:
                pdf_path = convert_docx_to_pdf(docx_path, Path(td))
                pdf_report = page_composition.analyze(pdf_path, spec, docx_path)
        if args.pdf:
            pdf_report = page_composition.analyze(pdf_path, spec, docx_path)

    combined = {
        "docx": str(docx_path),
        "pdf": str(pdf_path) if pdf_path else None,
        "style": spec.get("name"),
        "docx_lint": lint_report,
        "page_composition": pdf_report,
        "summary": {
            "docx_errors": lint_report["summary"]["errors"],
            "docx_warnings": lint_report["summary"]["warnings"],
            "pdf_warnings": (pdf_report or {}).get("summary", {}).get("warnings", 0),
        },
    }

    if args.out:
        Path(args.out).write_text(json.dumps(combined, indent=2), encoding="utf8")
    else:
        print(json.dumps(combined, indent=2))

    sev_order = {"info": 1, "warn": 2, "error": 3}
    threshold = sev_order[args.fail_on]
    if combined["summary"]["docx_errors"] > 0 and threshold <= sev_order["error"]:
        return 1
    if combined["summary"]["docx_warnings"] > 0 and threshold <= sev_order["warn"]:
        return 1
    if combined["summary"]["pdf_warnings"] > 0 and threshold <= sev_order["warn"]:
        # PDF warnings are not fatal by default unless user set --fail-on warn
        return 1 if threshold <= sev_order["warn"] else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
