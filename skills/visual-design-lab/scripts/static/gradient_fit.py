#!/usr/bin/env python3
"""
gradient_fit.py — Linear/radial gradient detection and CSS stop extraction.

Input:  image path + optional region bbox
Output: JSON with {type, angle|center, stops: [{color, position}], css, confidence}

Approach (inspired by dont-crop fitGradient):
  1. Detect gradient regions via directional color variance
  2. Classify linear vs radial
  3. For linear: compute dominant gradient direction, sample along axis
  4. For radial: find variance centroid, sample along radii
  5. Cluster sampled colors into gradient stops
  6. Output CSS gradient string
"""

import json
import sys
import math
from pathlib import Path

import numpy as np
from PIL import Image


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


def _sample_line(img_arr: np.ndarray, start: tuple, end: tuple, num_samples: int = 32) -> list[np.ndarray]:
    """Sample pixel colors along a line."""
    h, w = img_arr.shape[:2]
    samples = []
    for t in np.linspace(0, 1, num_samples):
        x = int(start[0] + t * (end[0] - start[0]))
        y = int(start[1] + t * (end[1] - start[1]))
        x = max(0, min(w - 1, x))
        y = max(0, min(h - 1, y))
        # Average a small neighborhood for noise reduction
        y1, y2 = max(0, y - 1), min(h, y + 2)
        x1, x2 = max(0, x - 1), min(w, x + 2)
        patch = img_arr[y1:y2, x1:x2]
        if patch.size > 0:
            samples.append(patch.reshape(-1, 3).mean(axis=0))
        else:
            samples.append(img_arr[y, x].astype(float))
    return samples


def _color_variance_direction(img_arr: np.ndarray) -> tuple[float, float]:
    """Compute the dominant direction of color change.
    Returns (angle_degrees, variance_ratio) where ratio > 2 suggests strong linear gradient.
    """
    h, w = img_arr.shape[:2]
    gray = img_arr.mean(axis=2) if img_arr.ndim == 3 else img_arr.astype(float)

    # Compute horizontal and vertical variance
    h_var = np.var(np.diff(gray, axis=1))
    v_var = np.var(np.diff(gray, axis=0))

    # Also check diagonal
    diag_samples_main = [gray[i, i] for i in range(min(h, w))]
    diag_samples_anti = [gray[i, w - 1 - i] for i in range(min(h, w))]
    d_var = np.var(np.diff(diag_samples_main)) if len(diag_samples_main) > 2 else 0
    a_var = np.var(np.diff(diag_samples_anti)) if len(diag_samples_anti) > 2 else 0

    # Direction with maximum variance of gradient
    variances = {
        0: h_var,      # horizontal gradient (left→right)
        90: v_var,     # vertical gradient (top→bottom)
        45: d_var,     # diagonal
        135: a_var,    # anti-diagonal
    }

    # Actually we want the direction where the *mean* changes most (not variance of diff)
    h_change = abs(gray[:, -1].mean() - gray[:, 0].mean())
    v_change = abs(gray[-1, :].mean() - gray[0, :].mean())

    if h_change > v_change * 1.5:
        angle = 90  # CSS angle: to right
    elif v_change > h_change * 1.5:
        angle = 180  # CSS angle: to bottom
    else:
        # Check diagonals
        tl = gray[:h//4, :w//4].mean()
        br = gray[3*h//4:, 3*w//4:].mean()
        tr = gray[:h//4, 3*w//4:].mean()
        bl = gray[3*h//4:, :w//4].mean()

        main_diag = abs(br - tl)
        anti_diag = abs(bl - tr)

        if main_diag > anti_diag:
            angle = 135  # to bottom-right
        else:
            angle = 225  # to bottom-left

    max_change = max(h_change, v_change)
    return angle, max_change


def _is_radial(img_arr: np.ndarray) -> tuple[bool, tuple[int, int], float]:
    """Detect if gradient is radial. Returns (is_radial, center, confidence)."""
    h, w = img_arr.shape[:2]
    gray = img_arr.mean(axis=2) if img_arr.ndim == 3 else img_arr.astype(float)

    # Check if center is distinctly different from edges
    center_region = gray[h//3:2*h//3, w//3:2*w//3]
    edge_top = gray[:h//6, :].mean()
    edge_bottom = gray[5*h//6:, :].mean()
    edge_left = gray[:, :w//6].mean()
    edge_right = gray[:, 5*w//6:].mean()
    center_val = center_region.mean()

    edge_mean = (edge_top + edge_bottom + edge_left + edge_right) / 4
    edge_std = np.std([edge_top, edge_bottom, edge_left, edge_right])

    center_diff = abs(center_val - edge_mean)
    # Radial if center is uniformly different from all edges
    is_rad = center_diff > 20 and edge_std < center_diff * 0.5

    # Find the center of radial gradient (brightest or darkest point)
    # Blur to smooth noise
    from PIL import ImageFilter
    blurred = np.array(Image.fromarray(gray.astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=5)))

    if center_val > edge_mean:
        cy, cx = np.unravel_index(blurred.argmax(), blurred.shape)
    else:
        cy, cx = np.unravel_index(blurred.argmin(), blurred.shape)

    conf = min(0.85, 0.3 + center_diff / 100)
    return is_rad, (int(cx), int(cy)), round(conf, 3)


def _cluster_stops(colors: list[np.ndarray], positions: list[float], max_stops: int = 5) -> list[dict]:
    """Cluster sampled gradient colors into discrete stops."""
    if len(colors) < 2:
        return []

    # Always include first and last
    stops = [{"position": 0.0, "color": colors[0]}]

    # Find positions where color changes significantly
    for i in range(1, len(colors) - 1):
        prev = colors[i - 1]
        curr = colors[i]
        next_c = colors[i + 1]

        # Check if this is a color "knee point" (change in rate of change)
        d1 = np.linalg.norm(curr - prev)
        d2 = np.linalg.norm(next_c - curr)

        if abs(d1 - d2) > 15 and len(stops) < max_stops - 1:
            stops.append({"position": positions[i], "color": curr})

    stops.append({"position": 1.0, "color": colors[-1]})

    # Convert colors to hex
    for stop in stops:
        c = stop["color"]
        r, g, b = int(c[0]), int(c[1]), int(c[2])
        stop["hex"] = _rgb_to_hex(r, g, b)
        stop["rgb"] = [r, g, b]
        del stop["color"]

    return stops


def _to_css_linear(angle: float, stops: list[dict]) -> str:
    """Generate CSS linear-gradient string."""
    stop_strs = [f"{s['hex']} {s['position']*100:.0f}%" for s in stops]
    return f"linear-gradient({angle:.0f}deg, {', '.join(stop_strs)})"


def _to_css_radial(center: tuple, stops: list[dict]) -> str:
    """Generate CSS radial-gradient string."""
    stop_strs = [f"{s['hex']} {s['position']*100:.0f}%" for s in stops]
    cx, cy = center
    return f"radial-gradient(circle at {cx}% {cy}%, {', '.join(stop_strs)})"


def detect_gradient(
    image_path: str,
    bbox: dict | None = None,
) -> dict:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    if bbox:
        crop = img.crop((bbox["x"], bbox["y"], bbox["x"] + bbox["w"], bbox["y"] + bbox["h"]))
    else:
        crop = img

    arr = np.array(crop)
    ch, cw = arr.shape[:2]

    # First check: is the region even a gradient? (vs solid or image)
    color_std = arr.reshape(-1, 3).std(axis=0).mean()
    if color_std < 5:
        return {
            "type": "solid",
            "color": _rgb_to_hex(*arr.reshape(-1, 3).mean(axis=0).astype(int)),
            "confidence": 0.9,
        }
    if color_std > 80:
        return {
            "type": "image_or_complex",
            "note": "High color variance suggests an image, not a CSS gradient",
            "confidence": 0.3,
        }

    # Check radial
    is_radial, center, rad_conf = _is_radial(arr)

    if is_radial:
        # Sample along radii from center
        cx, cy = center
        num_samples = 24
        max_r = min(cx, cy, cw - cx, ch - cy)
        samples = []
        positions = []
        for t in np.linspace(0, 1, num_samples):
            r = t * max_r
            # Sample at 4 angles and average
            pts = []
            for angle in [0, 90, 180, 270]:
                sx = int(cx + r * math.cos(math.radians(angle)))
                sy = int(cy + r * math.sin(math.radians(angle)))
                sx = max(0, min(cw - 1, sx))
                sy = max(0, min(ch - 1, sy))
                pts.append(arr[sy, sx].astype(float))
            samples.append(np.mean(pts, axis=0))
            positions.append(t)

        stops = _cluster_stops(samples, positions)
        center_pct = (round(cx / cw * 100), round(cy / ch * 100))
        css = _to_css_radial(center_pct, stops)

        return {
            "type": "radial",
            "center": {"x": center_pct[0], "y": center_pct[1]},
            "stops": [{"hex": s["hex"], "position": round(s["position"], 3)} for s in stops],
            "css": css,
            "confidence": round(rad_conf, 3),
        }
    else:
        # Linear gradient
        angle, magnitude = _color_variance_direction(arr)

        # Sample along the gradient direction
        angle_rad = math.radians(angle - 90)  # Convert CSS angle to math angle
        # Start/end points based on angle
        if 80 < angle < 100:  # left to right
            start, end = (0, ch // 2), (cw - 1, ch // 2)
        elif 170 < angle < 190:  # top to bottom
            start, end = (cw // 2, 0), (cw // 2, ch - 1)
        elif 125 < angle < 145:  # to bottom-right
            start, end = (0, 0), (cw - 1, ch - 1)
        else:  # to bottom-left
            start, end = (cw - 1, 0), (0, ch - 1)

        samples = _sample_line(arr, start, end)
        positions = list(np.linspace(0, 1, len(samples)))
        stops = _cluster_stops(samples, positions)
        css = _to_css_linear(angle, stops)

        confidence = min(0.85, 0.4 + magnitude / 200)

        return {
            "type": "linear",
            "angle": angle,
            "stops": [{"hex": s["hex"], "position": round(s["position"], 3)} for s in stops],
            "css": css,
            "confidence": round(confidence, 3),
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python gradient_fit.py <image_path> [--bbox '<json>']", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: {image_path} not found", file=sys.stderr)
        sys.exit(1)

    bbox = None
    if "--bbox" in sys.argv:
        idx = sys.argv.index("--bbox")
        if idx + 1 < len(sys.argv):
            bbox = json.loads(sys.argv[idx + 1])

    result = detect_gradient(image_path, bbox)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
