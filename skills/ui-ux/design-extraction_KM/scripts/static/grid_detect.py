#!/usr/bin/env python3
"""
grid_detect.py — Grid structure + spacing scale detection from screenshots.

Input:  image path
Output: JSON with {columns, rows, columnGap, rowGap, spacingScale, margins, confidence}

Method:
  1. Edge detection → horizontal/vertical line detection via projection profiles
  2. Cluster line positions to find repeating gaps
  3. Infer column count + gutter from gap clusters
  4. Extract spacing scale (common multiples, snap to 4px grid)
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from collections import Counter


def _projection_profile(gray: np.ndarray, axis: int) -> np.ndarray:
    """Sum pixel intensities along axis. axis=0 → vertical profile, axis=1 → horizontal."""
    inverted = 255 - gray  # dark pixels become high values
    return inverted.sum(axis=axis).astype(float)


def _find_peaks(profile: np.ndarray, min_distance: int = 8, threshold_ratio: float = 0.3) -> list[int]:
    """Simple peak detection without scipy."""
    threshold = profile.max() * threshold_ratio
    peaks = []
    for i in range(1, len(profile) - 1):
        if profile[i] > threshold and profile[i] >= profile[i-1] and profile[i] >= profile[i+1]:
            if not peaks or (i - peaks[-1]) >= min_distance:
                peaks.append(i)
    return peaks


def _find_gaps(profile: np.ndarray, min_gap: int = 4) -> list[dict]:
    """Find low-value regions in projection profile (gaps between elements)."""
    threshold = profile.mean() * 0.2
    gaps = []
    in_gap = False
    gap_start = 0

    for i, val in enumerate(profile):
        if val < threshold:
            if not in_gap:
                gap_start = i
                in_gap = True
        else:
            if in_gap and (i - gap_start) >= min_gap:
                gaps.append({"start": gap_start, "end": i, "width": i - gap_start})
            in_gap = False

    return gaps


def _cluster_values(values: list[int], tolerance: int = 3) -> list[dict]:
    """Cluster nearby integer values and return {value, count}."""
    if not values:
        return []
    values = sorted(values)
    clusters = [{"values": [values[0]], "sum": values[0]}]

    for v in values[1:]:
        if v - (clusters[-1]["sum"] / len(clusters[-1]["values"])) <= tolerance:
            clusters[-1]["values"].append(v)
            clusters[-1]["sum"] += v
        else:
            clusters.append({"values": [v], "sum": v})

    return [
        {"value": round(c["sum"] / len(c["values"])), "count": len(c["values"])}
        for c in clusters
    ]


def _snap_to_grid(value: int, base: int = 4) -> int:
    """Snap a value to nearest multiple of base."""
    return round(value / base) * base


def _infer_spacing_scale(gap_widths: list[int], base: int = 4) -> list[int]:
    """Extract a spacing scale from observed gap widths."""
    if not gap_widths:
        return [4, 8, 12, 16, 24, 32]

    snapped = [_snap_to_grid(g, base) for g in gap_widths if g >= base]
    snapped = [s for s in snapped if s > 0]

    if not snapped:
        return [4, 8, 12, 16, 24, 32]

    # Count occurrences
    counter = Counter(snapped)
    # Keep values that appear more than once, or are common multiples
    scale = sorted(set(snapped))

    # Also add standard values if they're close to observed
    standard = [4, 8, 12, 16, 20, 24, 32, 40, 48, 64]
    for s in standard:
        for obs in scale:
            if abs(s - obs) <= base:
                if s not in scale:
                    scale.append(s)
                break

    return sorted(set(scale))[:12]


def _detect_columns(v_gaps: list[dict], img_w: int) -> dict:
    """Detect column structure from vertical gaps."""
    if len(v_gaps) < 1:
        return {"columns": 1, "gutterPx": 0, "marginPx": 0, "confidence": 0.3}

    gap_widths = [g["width"] for g in v_gaps]
    gap_positions = [(g["start"] + g["end"]) // 2 for g in v_gaps]

    # Cluster gap widths to find the gutter size
    width_clusters = _cluster_values(gap_widths)
    if not width_clusters:
        return {"columns": 1, "gutterPx": 0, "marginPx": 0, "confidence": 0.3}

    # Most common gap width is likely the gutter
    gutter_cluster = max(width_clusters, key=lambda c: c["count"])
    gutter = gutter_cluster["value"]

    # Count internal gaps (not margins)
    margin_left = v_gaps[0]["start"] if v_gaps else 0
    margin_right = img_w - v_gaps[-1]["end"] if v_gaps else 0

    # Internal gaps = those not at edges
    internal_gaps = [g for g in v_gaps if g["start"] > margin_left * 0.5 and g["end"] < img_w - margin_right * 0.5]
    columns = len(internal_gaps) + 1 if internal_gaps else 1

    confidence = min(0.95, 0.5 + gutter_cluster["count"] * 0.1)
    if columns > 1 and gutter_cluster["count"] >= columns - 1:
        confidence = min(0.95, confidence + 0.15)

    return {
        "columns": columns,
        "gutterPx": _snap_to_grid(gutter),
        "marginPx": _snap_to_grid(max(margin_left, margin_right)),
        "confidence": round(confidence, 3),
    }


def detect_grid(image_path: str) -> dict:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # Downsample for speed
    max_side = 800
    scale = min(1.0, max_side / max(w, h))
    if scale < 1.0:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    gray = np.array(img.convert("L"))
    ih, iw = gray.shape

    # Edge-enhanced version
    edge_img = Image.fromarray(gray).filter(ImageFilter.FIND_EDGES)
    edges = np.array(edge_img)

    # Horizontal projection (sum along rows → find vertical gaps)
    h_profile = _projection_profile(edges, axis=0)
    # Vertical projection (sum along columns → find horizontal gaps)
    v_profile = _projection_profile(edges, axis=1)

    h_gaps = _find_gaps(h_profile)
    v_gaps = _find_gaps(v_profile)

    # Scale gaps back to original coordinates
    for g in h_gaps:
        g["start"] = int(g["start"] / scale)
        g["end"] = int(g["end"] / scale)
        g["width"] = int(g["width"] / scale)
    for g in v_gaps:
        g["start"] = int(g["start"] / scale)
        g["end"] = int(g["end"] / scale)
        g["width"] = int(g["width"] / scale)

    # Detect column structure
    col_info = _detect_columns(h_gaps, w)

    # Row analysis
    row_gaps = [g["width"] for g in v_gaps]
    row_clusters = _cluster_values(row_gaps) if row_gaps else []

    # Spacing scale from all gaps
    all_gaps = [g["width"] for g in h_gaps] + [g["width"] for g in v_gaps]
    spacing_scale = _infer_spacing_scale(all_gaps)

    # Detect base spacing unit
    if spacing_scale:
        # Most common smallest value
        small_gaps = [g for g in all_gaps if 2 <= g <= 32]
        if small_gaps:
            counter = Counter([_snap_to_grid(g) for g in small_gaps])
            base_unit = counter.most_common(1)[0][0] if counter else 8
        else:
            base_unit = 8
    else:
        base_unit = 8

    return {
        "columns": col_info["columns"],
        "gutterPx": col_info["gutterPx"],
        "marginPx": col_info["marginPx"],
        "spacingUnitPx": _snap_to_grid(base_unit),
        "spacingScale": spacing_scale,
        "rowGaps": [c["value"] for c in row_clusters[:5]] if row_clusters else [],
        "detectedGaps": {
            "horizontal": len(h_gaps),
            "vertical": len(v_gaps),
        },
        "confidence": col_info["confidence"],
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python grid_detect.py <image_path>", file=sys.stderr)
        sys.exit(1)
    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: {image_path} not found", file=sys.stderr)
        sys.exit(1)
    result = detect_grid(image_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
