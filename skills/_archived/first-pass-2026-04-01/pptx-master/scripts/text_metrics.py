#!/usr/bin/env python3
"""Text measurement helpers for preflight QA.

Tier A: heuristic fallback.
Tier B: Pillow font metrics when available.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

PT_PER_IN = 72.0
PX_PER_IN = 96.0
PX_PER_PT = PX_PER_IN / PT_PER_IN

try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except Exception:  # pragma: no cover - Pillow is optional
    PIL_AVAILABLE = False
    Image = None
    ImageDraw = None
    ImageFont = None


def _split_long_token(token: str, max_width_px: float, draw: Any, font: Any) -> List[str]:
    chunks: List[str] = []
    cur = ""
    for ch in token:
        test = cur + ch
        if draw.textlength(test, font=font) <= max_width_px or not cur:
            cur = test
        else:
            chunks.append(cur)
            cur = ch
    if cur:
        chunks.append(cur)
    return chunks


def _wrap_paragraph_pillow(paragraph: str, max_width_px: float, draw: Any, font: Any) -> List[str]:
    text = paragraph.strip()
    if not text:
        return []

    words = re.split(r"\s+", text)
    lines: List[str] = []
    cur = ""

    for word in words:
        if not word:
            continue
        test = f"{cur} {word}" if cur else word
        if draw.textlength(test, font=font) <= max_width_px:
            cur = test
            continue

        if cur:
            lines.append(cur)
            cur = ""

        if draw.textlength(word, font=font) <= max_width_px:
            cur = word
            continue

        # Single token is wider than the line; split by character width.
        pieces = _split_long_token(word, max_width_px, draw, font)
        if pieces:
            lines.extend(pieces[:-1])
            cur = pieces[-1]

    if cur:
        lines.append(cur)
    return lines


def estimate_text_height_heuristic(
    text: str,
    box_w_in: float,
    font_size_pt: float,
    line_height: float = 1.2,
) -> Dict[str, Any]:
    """Conservative Tier A estimate based on average glyph width."""
    if not text:
        return {"height_pt": 0.0, "line_count": 0, "tier": "A_HEURISTIC"}

    width_pt = max(1.0, box_w_in * PT_PER_IN)
    avg_char_pt = max(1.0, font_size_pt) * 0.52

    paras = re.split(r"\n+", text.strip())
    total_lines = 0
    para_count = 0

    for para in paras:
        p = para.strip()
        if not p:
            continue

        words = re.split(r"\s+", p)
        line_w = 0.0
        lines_here = 1
        for word in words:
            if not word:
                continue
            word_w = len(word) * avg_char_pt
            space_w = avg_char_pt * 0.6 if line_w > 0 else 0.0
            if line_w + space_w + word_w <= width_pt:
                line_w += space_w + word_w
            else:
                lines_here += 1
                line_w = word_w

        total_lines += lines_here
        para_count += 1

    if total_lines == 0:
        return {"height_pt": 0.0, "line_count": 0, "tier": "A_HEURISTIC"}

    gaps = max(0, para_count - 1)
    height_pt = total_lines * font_size_pt * line_height + gaps * font_size_pt * 0.35
    return {"height_pt": height_pt, "line_count": total_lines, "tier": "A_HEURISTIC"}


def _load_pillow_font(font_family: Optional[str], size_px: int, bold: bool) -> Any:
    candidates: List[str] = []
    if font_family and isinstance(font_family, str):
        ff = font_family.strip()
        if ff:
            candidates.extend([ff, f"{ff}.ttf", f"{ff}.otf", ff.replace(" ", "") + ".ttf"])

    if bold:
        candidates.extend(["DejaVuSans-Bold.ttf", "Arial Bold.ttf", "Arial Bold.ttf"])
    candidates.extend(["DejaVuSans.ttf", "Arial.ttf"])

    for cand in candidates:
        try:
            return ImageFont.truetype(cand, size=size_px)
        except Exception:
            continue

    return ImageFont.load_default()


def measure_text_height(
    text: str,
    box_w_in: float,
    font_size_pt: float,
    line_height: float = 1.2,
    font_family: Optional[str] = None,
    bold: bool = False,
) -> Dict[str, Any]:
    """Measure text height, preferring Tier B (Pillow) with Tier A fallback."""
    if not text or not text.strip():
        return {"height_pt": 0.0, "line_count": 0, "tier": "A_HEURISTIC"}

    if PIL_AVAILABLE:
        try:
            size_px = max(1, int(round(max(1.0, font_size_pt) * PX_PER_PT)))
            width_px = max(1.0, box_w_in * PX_PER_IN)

            font = _load_pillow_font(font_family, size_px=size_px, bold=bold)
            canvas = Image.new("RGB", (1, 1))
            draw = ImageDraw.Draw(canvas)

            paras = re.split(r"\n+", text.strip())
            total_lines = 0
            para_count = 0
            for para in paras:
                lines = _wrap_paragraph_pillow(para, width_px, draw, font)
                if not lines:
                    continue
                total_lines += len(lines)
                para_count += 1

            if total_lines > 0:
                try:
                    ascent, descent = font.getmetrics()
                    measured_line_pt = (ascent + descent) / PX_PER_PT
                except Exception:
                    measured_line_pt = font_size_pt

                line_height_pt = max(font_size_pt * line_height, measured_line_pt)
                gaps = max(0, para_count - 1)
                height_pt = total_lines * line_height_pt + gaps * font_size_pt * 0.35
                return {"height_pt": height_pt, "line_count": total_lines, "tier": "B_PIL"}
        except Exception:
            pass

    return estimate_text_height_heuristic(text, box_w_in, font_size_pt, line_height)
