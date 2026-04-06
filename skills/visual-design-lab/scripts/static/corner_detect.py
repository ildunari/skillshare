#!/usr/bin/env python3
"""
corner_detect.py — Border radius estimation from screenshot elements.

Input:  image path + optional element bboxes (JSON on stdin or --bboxes arg)
Output: JSON list of {element_id, corners: [{x,y,radius}], avg_radius, classification, confidence}

Method:
  1. Edge detection on element crop
  2. Contour tracing
  3. Curvature analysis at corners (circle fitting to corner arc points)
  4. Classification: sharp (<2px), small (2-6), medium (6-12), large (12-24), pill (>24)
"""

import json
import sys
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def _fit_circle_3pts(p1, p2, p3):
    """Fit a circle through 3 points. Returns (cx, cy, radius) or None."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3

    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-10:
        return None

    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    r = math.sqrt((ax - ux)**2 + (ay - uy)**2)

    return ux, uy, r


def _trace_contour(binary: np.ndarray) -> list[tuple[int, int]]:
    """Simple contour tracing via boundary following."""
    h, w = binary.shape
    contour = []

    # Find starting point (top-left edge pixel)
    start = None
    for y in range(h):
        for x in range(w):
            if binary[y, x]:
                start = (y, x)
                break
        if start:
            break

    if not start:
        return contour

    # 8-connected boundary following
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    cy, cx = start
    direction = 0
    contour.append((cx, cy))

    for _ in range(max(h * w, 10000)):
        found = False
        search_start = (direction + 5) % 8  # start searching from dir-3

        for di in range(8):
            d = (search_start + di) % 8
            ny, nx = cy + dirs[d][0], cx + dirs[d][1]

            if 0 <= ny < h and 0 <= nx < w and binary[ny, nx]:
                contour.append((nx, ny))
                cy, cx = ny, nx
                direction = d
                found = True
                break

        if not found or (len(contour) > 4 and (cx, cy) == contour[0]):
            break

    return contour


def _measure_corner_radius(contour: list[tuple], corner_region: tuple, sample_range: int = 15) -> tuple[float, float]:
    """Measure radius at a corner region by fitting circles to nearby contour points."""
    if len(contour) < 20:
        return 0.0, 0.2

    cx, cy = corner_region
    # Find contour points near this corner
    dists = [(i, math.sqrt((p[0] - cx)**2 + (p[1] - cy)**2)) for i, p in enumerate(contour)]
    dists.sort(key=lambda x: x[1])

    nearby = [contour[d[0]] for d in dists[:sample_range * 3] if d[1] < sample_range * 2]

    if len(nearby) < 6:
        return 0.0, 0.2

    # Try fitting circles to triplets of nearby points
    radii = []
    step = max(1, len(nearby) // 10)
    for i in range(0, len(nearby) - 2 * step, step):
        result = _fit_circle_3pts(nearby[i], nearby[i + step], nearby[i + 2 * step])
        if result and 0.5 < result[2] < 200:
            radii.append(result[2])

    if not radii:
        return 0.0, 0.3

    # Median radius (robust to outliers)
    radii.sort()
    median_r = radii[len(radii) // 2]
    # Confidence from consistency
    if len(radii) > 2:
        iqr = radii[int(len(radii) * 0.75)] - radii[int(len(radii) * 0.25)]
        consistency = 1.0 - min(1.0, iqr / max(median_r, 1))
        confidence = 0.5 + consistency * 0.4
    else:
        confidence = 0.4

    return round(median_r, 1), round(confidence, 3)


def _classify_radius(r: float) -> str:
    if r < 2:
        return "sharp"
    elif r < 6:
        return "small"
    elif r < 12:
        return "medium"
    elif r < 24:
        return "large"
    else:
        return "pill"


def detect_corners_for_bbox(img: Image.Image, bbox: dict) -> dict:
    """Detect corner radii for a single element bbox."""
    w_img, h_img = img.size
    x, y, bw, bh = bbox["x"], bbox["y"], bbox["w"], bbox["h"]

    # Expand crop slightly to capture edges
    pad = 4
    cx1 = max(0, x - pad)
    cy1 = max(0, y - pad)
    cx2 = min(w_img, x + bw + pad)
    cy2 = min(h_img, y + bh + pad)

    crop = img.crop((cx1, cy1, cx2, cy2)).convert("L")
    crop_arr = np.array(crop)

    # Edge detection
    edges = np.array(Image.fromarray(crop_arr).filter(ImageFilter.FIND_EDGES))
    threshold = max(edges.mean() + edges.std(), 30)
    binary = edges > threshold

    # Trace contour
    contour = _trace_contour(binary)

    ch, cw = crop_arr.shape
    # Define corner regions (relative to crop)
    corner_positions = {
        "top_left": (pad, pad),
        "top_right": (cw - pad, pad),
        "bottom_right": (cw - pad, ch - pad),
        "bottom_left": (pad, ch - pad),
    }

    corners = []
    radii_values = []

    for name, (ccx, ccy) in corner_positions.items():
        radius, conf = _measure_corner_radius(contour, (ccx, ccy))
        corners.append({
            "position": name,
            "x": x + ccx - pad,
            "y": y + ccy - pad,
            "radius": radius,
            "confidence": conf,
        })
        radii_values.append(radius)

    avg_radius = round(np.mean(radii_values), 1) if radii_values else 0
    avg_conf = round(np.mean([c["confidence"] for c in corners]), 3)

    return {
        "corners": corners,
        "avg_radius": avg_radius,
        "classification": _classify_radius(avg_radius),
        "confidence": avg_conf,
    }


def detect_corners(image_path: str, bboxes: list[dict] | None = None) -> list[dict]:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    if not bboxes:
        # Auto-detect large rectangular regions
        from segment_ui import segment_ui
        segments = segment_ui(image_path)
        bboxes = [
            {"id": s["id"], **s["bbox_px"]}
            for s in segments
            if s["type_guess"] in ("button", "input", "container", "card", "unknown")
            and s["area"] > 500
        ]

    results = []
    for bbox in bboxes:
        eid = bbox.get("id", f"elem_{len(results)}")
        try:
            info = detect_corners_for_bbox(img, bbox)
            info["element_id"] = eid
            info["bbox"] = {"x": bbox["x"], "y": bbox["y"], "w": bbox["w"], "h": bbox["h"]}
            results.append(info)
        except Exception as e:
            results.append({
                "element_id": eid,
                "error": str(e),
                "avg_radius": 0,
                "classification": "unknown",
                "confidence": 0.1,
            })

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python corner_detect.py <image_path> [--bboxes '<json>']", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: {image_path} not found", file=sys.stderr)
        sys.exit(1)

    bboxes = None
    if "--bboxes" in sys.argv:
        idx = sys.argv.index("--bboxes")
        if idx + 1 < len(sys.argv):
            bboxes = json.loads(sys.argv[idx + 1])

    result = detect_corners(image_path, bboxes)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
