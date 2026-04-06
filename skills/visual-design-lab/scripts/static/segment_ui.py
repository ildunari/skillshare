#!/usr/bin/env python3
"""
segment_ui.py — Non-text UI element detection via edge detection + contours.

Input:  image path
Output: JSON list of {id, bbox_px, bbox_norm, area, aspect_ratio, type_guess, confidence}

Detects rectangles, icons, images, and containers using:
  - Canny edge detection with auto threshold
  - Contour detection + rectangle fitting
  - Connected component analysis for small elements
  - Type classification from shape heuristics
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def _auto_canny(gray: np.ndarray, sigma: float = 0.33) -> np.ndarray:
    """Canny edge detection with automatic threshold selection."""
    median = np.median(gray)
    low = int(max(0, (1.0 - sigma) * median))
    high = int(min(255, (1.0 + sigma) * median))

    # Simple Sobel-based edge detection (no OpenCV dependency)
    from PIL import Image as _Im, ImageFilter as _If
    pil_img = _Im.fromarray(gray)
    edges = pil_img.filter(_If.FIND_EDGES)
    edge_arr = np.array(edges)

    # Threshold
    binary = (edge_arr > low).astype(np.uint8) * 255
    return binary


def _find_contour_rects(binary: np.ndarray, min_area: int = 100) -> list[dict]:
    """Find rectangular regions from binary edge image using flood fill."""
    h, w = binary.shape
    visited = np.zeros((h, w), dtype=bool)
    rects = []

    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if binary[y, x] > 128 and not visited[y, x]:
                # BFS to find connected edge pixels
                queue = [(y, x)]
                pts = []
                qi = 0
                while qi < len(queue) and len(queue) < 50000:
                    cy, cx = queue[qi]
                    qi += 1
                    if cy < 0 or cy >= h or cx < 0 or cx >= w:
                        continue
                    if visited[cy, cx]:
                        continue
                    if binary[cy, cx] < 64:
                        continue
                    visited[cy, cx] = True
                    pts.append((cy, cx))
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                            queue.append((ny, nx))

                if len(pts) < 8:
                    continue

                ys = [p[0] for p in pts]
                xs = [p[1] for p in pts]
                bx, by = min(xs), min(ys)
                bw = max(xs) - bx
                bh = max(ys) - by
                area = bw * bh

                if area < min_area or bw < 4 or bh < 4:
                    continue
                if area > (w * h * 0.9):
                    continue

                rects.append({
                    "x": bx, "y": by, "w": bw, "h": bh,
                    "area": area,
                    "edge_density": len(pts) / max(area, 1),
                })

    return rects


def _classify_element(rect: dict, img_w: int, img_h: int) -> tuple[str, float]:
    """Classify UI element type from shape heuristics."""
    w, h = rect["w"], rect["h"]
    area = rect["area"]
    aspect = w / max(h, 1)
    rel_area = area / (img_w * img_h)
    density = rect["edge_density"]

    # Icon: small, roughly square
    if rel_area < 0.005 and 0.5 < aspect < 2.0:
        return "icon", 0.65

    # Button: medium width, short height, wide aspect
    if 0.003 < rel_area < 0.08 and 2.0 < aspect < 10.0 and h < img_h * 0.1:
        return "button", 0.60

    # Input field: wide, short, moderate area
    if 0.005 < rel_area < 0.1 and aspect > 3.0 and h < img_h * 0.08:
        return "input", 0.55

    # Card/container: large area, moderate aspect
    if rel_area > 0.03 and 0.3 < aspect < 3.0:
        return "container", 0.50

    # Image: moderate area, low edge density (smooth content)
    if 0.01 < rel_area < 0.5 and density < 0.15:
        return "image", 0.45

    # Navigation bar: very wide, at top or bottom
    if aspect > 5.0 and (rect["y"] < img_h * 0.1 or rect["y"] > img_h * 0.85):
        return "navigation", 0.55

    # Scrollbar: very tall and narrow
    if aspect < 0.15 and h > img_h * 0.3:
        return "scrollbar", 0.50

    # Divider: very wide and thin
    if aspect > 10.0 and h < 5:
        return "divider", 0.60

    return "unknown", 0.30


def _remove_overlaps(rects: list[dict], iou_threshold: float = 0.5) -> list[dict]:
    """Remove heavily overlapping detections, keeping higher confidence."""
    if not rects:
        return rects

    rects.sort(key=lambda r: r.get("confidence", 0), reverse=True)
    keep = []

    for rect in rects:
        is_dup = False
        for kept in keep:
            # Compute IoU
            x1 = max(rect["x"], kept["x"])
            y1 = max(rect["y"], kept["y"])
            x2 = min(rect["x"] + rect["w"], kept["x"] + kept["w"])
            y2 = min(rect["y"] + rect["h"], kept["y"] + kept["h"])
            inter = max(0, x2 - x1) * max(0, y2 - y1)
            union = rect["area"] + kept["area"] - inter
            iou = inter / max(union, 1)
            if iou > iou_threshold:
                is_dup = True
                break
        if not is_dup:
            keep.append(rect)

    return keep


def segment_ui(image_path: str) -> list[dict]:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # Work at reduced resolution for speed
    max_side = 800
    scale = min(1.0, max_side / max(w, h))
    if scale < 1.0:
        sw, sh = int(w * scale), int(h * scale)
        img_small = img.resize((sw, sh), Image.LANCZOS)
    else:
        sw, sh = w, h
        img_small = img
        scale = 1.0

    gray = np.array(img_small.convert("L"))
    edges = _auto_canny(gray)
    raw_rects = _find_contour_rects(edges)

    # Scale back to original coordinates
    for r in raw_rects:
        r["x"] = int(r["x"] / scale)
        r["y"] = int(r["y"] / scale)
        r["w"] = int(r["w"] / scale)
        r["h"] = int(r["h"] / scale)
        r["area"] = r["w"] * r["h"]

    # Classify and build output
    results = []
    for i, rect in enumerate(raw_rects):
        type_guess, conf = _classify_element(rect, w, h)
        rect["type_guess"] = type_guess
        rect["confidence"] = conf
        results.append(rect)

    # Remove overlaps
    results = _remove_overlaps(results)

    # Format output
    output = []
    for i, r in enumerate(results):
        output.append({
            "id": f"elem_{i:03d}",
            "bbox_px": {"x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"]},
            "bbox_norm": {
                "x": round(r["x"] / w, 4),
                "y": round(r["y"] / h, 4),
                "w": round(r["w"] / w, 4),
                "h": round(r["h"] / h, 4),
            },
            "area": r["area"],
            "aspect_ratio": round(r["w"] / max(r["h"], 1), 3),
            "type_guess": r["type_guess"],
            "confidence": round(r["confidence"], 3),
        })

    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python segment_ui.py <image_path>", file=sys.stderr)
        sys.exit(1)
    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: {image_path} not found", file=sys.stderr)
        sys.exit(1)
    result = segment_ui(image_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
