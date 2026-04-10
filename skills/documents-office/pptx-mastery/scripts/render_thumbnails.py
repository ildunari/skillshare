#!/usr/bin/env python3
"""
render_thumbnails.py

Render per-slide PNG thumbnails from a PPTX by using LibreOffice to create PDF
and pdftoppm to rasterize each page.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional


def _find_cmd(candidates: List[str]) -> Optional[str]:
    for name in candidates:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None


def _run(cmd: List[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "command failed\n"
            f"cmd: {' '.join(cmd)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )


def render_thumbnails(pptx: Path, out_dir: Path, dpi: int = 144, prefix: str = "slide") -> List[Path]:
    soffice = _find_cmd(["soffice", "libreoffice"])
    if not soffice:
        raise FileNotFoundError(
            "LibreOffice not found. Install LibreOffice and ensure `soffice` is on PATH."
        )
    pdftoppm = _find_cmd(["pdftoppm"])
    if not pdftoppm:
        raise FileNotFoundError(
            "pdftoppm not found. Install poppler and ensure `pdftoppm` is on PATH."
        )

    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="pptx_thumbs_") as tmp:
        tmp_path = Path(tmp)
        pdf_path = tmp_path / f"{pptx.stem}.pdf"
        raw_prefix = tmp_path / "slide"

        _run(
            [
                soffice,
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(tmp_path),
                str(pptx),
            ]
        )

        if not pdf_path.exists():
            raise RuntimeError(f"LibreOffice did not produce expected PDF: {pdf_path}")

        _run(
            [
                pdftoppm,
                "-png",
                "-r",
                str(int(max(72, dpi))),
                str(pdf_path),
                str(raw_prefix),
            ]
        )

        generated = sorted(tmp_path.glob("slide-*.png"))
        if not generated:
            raise RuntimeError("No slide images were generated from PDF.")

        output_paths: List[Path] = []
        for idx, src in enumerate(generated, start=1):
            dst = out_dir / f"{prefix}-{idx:03d}.png"
            dst.write_bytes(src.read_bytes())
            output_paths.append(dst)
        return output_paths


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", type=Path, help="Input PPTX path")
    ap.add_argument("out_dir", type=Path, help="Output directory for per-slide PNGs")
    ap.add_argument("--dpi", type=int, default=144, help="Rasterization DPI (default: 144)")
    ap.add_argument("--prefix", type=str, default="slide", help="Output filename prefix (default: slide)")
    ap.add_argument("--manifest", type=Path, default=None, help="Optional JSON manifest output path")
    args = ap.parse_args()

    if not args.pptx.exists() or args.pptx.suffix.lower() != ".pptx":
        print(f"[render_thumbnails] error: invalid input PPTX: {args.pptx}")
        return 1

    try:
        rendered = render_thumbnails(args.pptx, args.out_dir, dpi=args.dpi, prefix=args.prefix)
    except FileNotFoundError as exc:
        print(f"[render_thumbnails] unavailable: {exc}")
        return 2
    except Exception as exc:
        print(f"[render_thumbnails] error: {exc}")
        return 1

    if args.manifest:
        manifest: Dict[str, Any] = {
            "pptx": str(args.pptx),
            "out_dir": str(args.out_dir),
            "count": len(rendered),
            "files": [str(p) for p in rendered],
            "dpi": int(max(72, args.dpi)),
        }
        args.manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"[render_thumbnails] rendered {len(rendered)} slide PNG(s) to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
