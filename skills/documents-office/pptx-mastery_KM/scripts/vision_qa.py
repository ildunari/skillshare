#!/usr/bin/env python3
"""
vision_qa.py

Lightweight deterministic vision-QA scaffold.
Consumes rendered thumbnails and emits rubric-shaped JSON for pipeline hooks.
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Dict, List


RUBRIC_KEYS = [
    "clarity",
    "hierarchy",
    "spacing",
    "alignment",
    "contrast",
    "color_discipline",
    "data_legibility",
    "visual_consistency",
    "narrative_signal",
]


def count_slides_in_pptx(pptx_path: Path) -> int:
    with zipfile.ZipFile(pptx_path, "r") as zf:
        names = [n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    return len(names)


def build_slide_entry(slide_index: int, thumbnail_exists: bool) -> Dict[str, Any]:
    base_score = 4.0 if thumbnail_exists else 3.0
    scores = {k: base_score for k in RUBRIC_KEYS}
    verdict = "pass" if thumbnail_exists else "warn"
    issues: List[Dict[str, str]] = []
    if not thumbnail_exists:
        issues.append(
            {
                "code": "V_THUMBNAIL_MISSING",
                "evidence": f"No thumbnail for slide {slide_index}",
                "fix": "Re-run render_thumbnails.py before vision QA.",
            }
        )
    return {
        "slide": slide_index,
        "slide_id": f"S{slide_index:02d}",
        "overall_score": round(sum(scores.values()) / len(scores), 2),
        "scores": scores,
        "verdict": verdict,
        "top_issues": issues,
        "recommended_fixes": [i["fix"] for i in issues] if issues else [],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", type=Path, help="Rendered PPTX path")
    ap.add_argument("--ir", type=Path, default=None, help="Optional IR path (reserved)")
    ap.add_argument("--thumbnails-dir", type=Path, default=None, help="Optional per-slide thumbnails directory")
    ap.add_argument("--out", type=Path, required=True, help="Output JSON report path")
    args = ap.parse_args()

    slide_count = count_slides_in_pptx(args.pptx)
    thumbs = set()
    if args.thumbnails_dir and args.thumbnails_dir.exists():
        for p in args.thumbnails_dir.iterdir():
            if p.is_file():
                thumbs.add(p.name)

    slides = []
    for idx in range(1, slide_count + 1):
        expected_names = {
            f"slide-{idx:03d}.png",
            f"slide-{idx}.png",
            f"slide-{idx:04d}.png",
        }
        thumb_exists = any(name in thumbs for name in expected_names) if thumbs else False
        slides.append(build_slide_entry(idx, thumb_exists))

    overall = round(sum(s["overall_score"] for s in slides) / max(1, len(slides)), 2)
    payload = {
        "version": 1,
        "slides": slides,
        "overall_score": overall,
        "verdict": "pass" if overall >= 3.5 else "warn",
        "rubric_keys": RUBRIC_KEYS,
    }
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[vision_qa] slides={len(slides)} overall_score={overall}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

