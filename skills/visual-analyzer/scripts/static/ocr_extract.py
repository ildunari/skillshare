#!/usr/bin/env python3
"""
ocr_extract.py — Text extraction with font size/weight estimation.

Input:  image path (PNG/JPG)
Output: JSON list of {id, text, bbox_px, bbox_norm, fontSize_px, fontWeight_guess, lineHeight_px, role_hint, confidence}

Uses Pillow for rendering comparisons when Tesseract isn't available.
Falls back to simple contour-based text detection if no OCR engine found.
"""

import json
import sys
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


# ---------------------------------------------------------------------------
# OCR backends (Tesseract preferred, fallback to basic detection)
# ---------------------------------------------------------------------------

def _try_tesseract(image_path: str) -> list[dict] | None:
    """Try Tesseract OCR via subprocess. Returns None if not available."""
    try:
        result = subprocess.run(
            ["tesseract", image_path, "stdout", "--psm", "11", "-c",
             "tessedit_create_tsv=1"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return None

        lines = result.stdout.strip().split("\n")
        if len(lines) < 2:
            return None

        headers = lines[0].split("\t")
        blocks = []
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) != len(headers):
                continue
            row = dict(zip(headers, parts))
            conf = int(row.get("conf", "-1"))
            text = row.get("text", "").strip()
            if conf < 30 or not text:
                continue
            blocks.append({
                "text": text,
                "x": int(row["left"]),
                "y": int(row["top"]),
                "w": int(row["width"]),
                "h": int(row["height"]),
                "conf": conf / 100.0,
            })
        return blocks
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def _basic_text_detect(img: Image.Image) -> list[dict]:
    """Fallback: detect dark regions on light background as likely text."""
    gray = np.array(img.convert("L"))
    h, w = gray.shape

    # Binary threshold (dark text on light bg)
    mean_val = gray.mean()
    if mean_val > 128:
        binary = gray < (mean_val - 40)
    else:
        binary = gray > (mean_val + 40)

    # Connected component analysis via flood fill
    visited = np.zeros_like(binary, dtype=bool)
    blocks = []

    def _flood(sy, sx):
        stack = [(sy, sx)]
        pts = []
        while stack:
            cy, cx = stack.pop()
            if cy < 0 or cy >= h or cx < 0 or cx >= w:
                continue
            if visited[cy, cx] or not binary[cy, cx]:
                continue
            visited[cy, cx] = True
            pts.append((cy, cx))
            stack.extend([(cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)])
        return pts

    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if binary[y, x] and not visited[y, x]:
                pts = _flood(y, x)
                if len(pts) < 10:
                    continue
                ys = [p[0] for p in pts]
                xs = [p[1] for p in pts]
                bx, by = min(xs), min(ys)
                bw, bh = max(xs) - bx, max(ys) - by
                # Filter: text blocks are wider than tall, or small
                if bw > 3 and bh > 3 and bw * bh < (w * h * 0.5):
                    aspect = bw / max(bh, 1)
                    if 0.2 < aspect < 50:
                        blocks.append({
                            "text": "[detected]",
                            "x": bx, "y": by, "w": bw, "h": bh,
                            "conf": 0.3,
                        })

    # Merge overlapping blocks on same line
    merged = _merge_horizontal(blocks)
    return merged


def _merge_horizontal(blocks, y_tol=8, x_gap=20):
    if not blocks:
        return blocks
    blocks.sort(key=lambda b: (b["y"], b["x"]))
    merged = [blocks[0]]
    for b in blocks[1:]:
        prev = merged[-1]
        # Same line?
        if abs(b["y"] - prev["y"]) < y_tol and b["x"] - (prev["x"] + prev["w"]) < x_gap:
            new_x = min(prev["x"], b["x"])
            new_y = min(prev["y"], b["y"])
            new_r = max(prev["x"] + prev["w"], b["x"] + b["w"])
            new_b = max(prev["y"] + prev["h"], b["y"] + b["h"])
            prev["x"], prev["y"] = new_x, new_y
            prev["w"], prev["h"] = new_r - new_x, new_b - new_y
        else:
            merged.append(b)
    return merged


# ---------------------------------------------------------------------------
# Font size / weight estimation
# ---------------------------------------------------------------------------

def _estimate_font_size(bbox_h: int, dpr: float = 1.0) -> float:
    """Estimate font size in px from text bbox height. Heuristic: fontSize ≈ bbox_height * 0.75."""
    return round(bbox_h * 0.75 / dpr, 1)


def _estimate_weight(img_crop: np.ndarray) -> tuple[int, float]:
    """Estimate font weight from stroke thickness. Returns (weight, confidence)."""
    if img_crop.size == 0:
        return 400, 0.2

    gray = img_crop if img_crop.ndim == 2 else np.mean(img_crop, axis=2)
    mean_val = gray.mean()

    # Threshold to get text pixels
    if mean_val > 128:
        text_mask = gray < (mean_val - 30)
    else:
        text_mask = gray > (mean_val + 30)

    if not text_mask.any():
        return 400, 0.2

    # Measure average horizontal run length (proxy for stroke width)
    runs = []
    for row in text_mask:
        in_run = False
        run_len = 0
        for val in row:
            if val:
                in_run = True
                run_len += 1
            elif in_run:
                runs.append(run_len)
                in_run = False
                run_len = 0

    if not runs:
        return 400, 0.2

    avg_run = np.mean(runs)
    h = text_mask.shape[0]
    ratio = avg_run / max(h, 1)

    # Map ratio to weight
    if ratio < 0.04:
        return 100, 0.5
    elif ratio < 0.06:
        return 300, 0.5
    elif ratio < 0.09:
        return 400, 0.6
    elif ratio < 0.12:
        return 500, 0.55
    elif ratio < 0.16:
        return 600, 0.5
    elif ratio < 0.22:
        return 700, 0.5
    else:
        return 900, 0.45


def _guess_text_role(font_size: float, weight: int, bbox_norm_y: float) -> str:
    """Guess typographic role from size/weight/position."""
    if font_size > 28:
        return "display" if font_size > 40 else "heading"
    if font_size > 20:
        return "title"
    if font_size > 16:
        return "subtitle" if weight >= 600 else "body-large"
    if font_size > 13:
        return "body"
    if font_size > 10:
        return "caption"
    return "overline"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def extract_text(image_path: str) -> list[dict]:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # Try Tesseract first
    blocks = _try_tesseract(image_path)
    if blocks is None:
        blocks = _basic_text_detect(img)

    img_array = np.array(img)
    results = []
    for i, block in enumerate(blocks):
        bx, by, bw, bh = block["x"], block["y"], block["w"], block["h"]

        # Crop for weight estimation
        crop = img_array[
            max(0, by):min(h, by + bh),
            max(0, bx):min(w, bx + bw),
        ]
        weight, weight_conf = _estimate_weight(crop)
        font_size = _estimate_font_size(bh)

        bbox_norm = {
            "x": round(bx / w, 4),
            "y": round(by / h, 4),
            "w": round(bw / w, 4),
            "h": round(bh / h, 4),
        }

        role = _guess_text_role(font_size, weight, bbox_norm["y"])

        results.append({
            "id": f"text_{i:03d}",
            "text": block["text"],
            "bbox_px": {"x": bx, "y": by, "w": bw, "h": bh},
            "bbox_norm": bbox_norm,
            "fontSize_px": font_size,
            "fontWeight_guess": weight,
            "lineHeight_px": round(bh * 1.0, 1),
            "role_hint": role,
            "confidence": round(block["conf"] * 0.8 + weight_conf * 0.2, 3),
        })

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr_extract.py <image_path>", file=sys.stderr)
        sys.exit(1)
    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: {image_path} not found", file=sys.stderr)
        sys.exit(1)
    result = extract_text(image_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
