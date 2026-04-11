#!/usr/bin/env python3
"""
visual_diff.py — Compare original screenshot vs rendered design spec.

Input:  original image path + rendered image path (or spec JSON to auto-render)
Output: JSON with {overall_ssim, per_region_diffs: [{bbox, ssim, issue}], mismatch_px, suggested_fixes}

Uses structural similarity (SSIM) with windowed comparison for localized diffs.
No scipy/skimage dependency — implements SSIM from scratch.
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def _ssim_window(img1: np.ndarray, img2: np.ndarray,
                 C1: float = 6.5025, C2: float = 58.5225) -> float:
    """Compute SSIM between two grayscale patches.
    C1 = (0.01 * 255)^2, C2 = (0.03 * 255)^2 — standard constants.
    """
    mu1 = img1.mean()
    mu2 = img2.mean()
    sigma1_sq = img1.var()
    sigma2_sq = img2.var()
    sigma12 = ((img1 - mu1) * (img2 - mu2)).mean()

    numerator = (2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1**2 + mu2**2 + C1) * (sigma1_sq + sigma2_sq + C2)

    return float(numerator / denominator) if denominator != 0 else 0.0


def compute_ssim(img1_gray: np.ndarray, img2_gray: np.ndarray,
                 window_size: int = 11) -> tuple[float, np.ndarray]:
    """Compute SSIM across entire image using sliding window.
    Returns (mean_ssim, ssim_map).
    """
    h, w = img1_gray.shape
    pad = window_size // 2
    ssim_map = np.zeros((h, w), dtype=float)

    for y in range(pad, h - pad, 2):  # step by 2 for speed
        for x in range(pad, w - pad, 2):
            win1 = img1_gray[y - pad:y + pad + 1, x - pad:x + pad + 1].astype(float)
            win2 = img2_gray[y - pad:y + pad + 1, x - pad:x + pad + 1].astype(float)
            s = _ssim_window(win1, win2)
            ssim_map[y:y+2, x:x+2] = s

    # Fill edges
    ssim_map[:pad, :] = ssim_map[pad, :].mean()
    ssim_map[-pad:, :] = ssim_map[-pad-1, :].mean()
    ssim_map[:, :pad] = ssim_map[:, pad].mean().item()
    ssim_map[:, -pad:] = ssim_map[:, -pad-1].mean().item()

    return float(ssim_map.mean()), ssim_map


def pixel_diff(img1: np.ndarray, img2: np.ndarray, threshold: int = 25) -> tuple[int, np.ndarray]:
    """Count mismatched pixels (per-channel diff > threshold).
    Returns (mismatch_count, diff_image).
    """
    diff = np.abs(img1.astype(int) - img2.astype(int))
    # Mismatch if any channel exceeds threshold
    mismatch = (diff.max(axis=2) > threshold) if diff.ndim == 3 else (diff > threshold)
    count = int(mismatch.sum())

    # Create visual diff (red overlay on mismatches)
    diff_vis = img1.copy()
    if diff_vis.ndim == 3:
        diff_vis[mismatch] = [255, 0, 0]
    else:
        diff_vis[mismatch] = 255

    return count, diff_vis


def _find_diff_regions(ssim_map: np.ndarray, threshold: float = 0.85,
                       min_region_size: int = 100) -> list[dict]:
    """Find contiguous regions where SSIM is below threshold."""
    bad = ssim_map < threshold
    h, w = bad.shape
    visited = np.zeros_like(bad, dtype=bool)
    regions = []

    for y in range(0, h, 4):
        for x in range(0, w, 4):
            if bad[y, x] and not visited[y, x]:
                # BFS
                queue = [(y, x)]
                pts = []
                qi = 0
                while qi < len(queue) and len(queue) < 10000:
                    cy, cx = queue[qi]
                    qi += 1
                    if cy < 0 or cy >= h or cx < 0 or cx >= w:
                        continue
                    if visited[cy, cx] or not bad[cy, cx]:
                        continue
                    visited[cy, cx] = True
                    pts.append((cy, cx))
                    for dy, dx in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        queue.append((cy + dy, cx + dx))

                if len(pts) < min_region_size // 4:
                    continue

                ys = [p[0] for p in pts]
                xs = [p[1] for p in pts]
                regions.append({
                    "bbox": {
                        "x": min(xs),
                        "y": min(ys),
                        "w": max(xs) - min(xs),
                        "h": max(ys) - min(ys),
                    },
                    "area": len(pts) * 4,
                    "mean_ssim": round(float(np.mean([ssim_map[p[0], p[1]] for p in pts[:50]])), 3),
                })

    return regions


def _guess_issue(region: dict, img1: np.ndarray, img2: np.ndarray) -> str:
    """Guess what kind of mismatch this is."""
    bbox = region["bbox"]
    y1 = bbox["y"]
    y2 = min(img1.shape[0], y1 + bbox["h"])
    x1 = bbox["x"]
    x2 = min(img1.shape[1], x1 + bbox["w"])

    patch1 = img1[y1:y2, x1:x2].astype(float)
    patch2 = img2[y1:y2, x1:x2].astype(float)

    if patch1.size == 0 or patch2.size == 0:
        return "region_empty"

    color_diff = abs(patch1.mean() - patch2.mean())
    std_diff = abs(patch1.std() - patch2.std())

    aspect = bbox["w"] / max(bbox["h"], 1)

    if color_diff > 30 and std_diff < 10:
        return "color_mismatch"
    if std_diff > 20 and color_diff < 15:
        return "texture_or_shadow_diff"
    if aspect > 5 and bbox["h"] < 8:
        return "border_or_divider_diff"
    if bbox["w"] < 20 and bbox["h"] < 20:
        return "icon_or_detail_diff"
    if color_diff > 15:
        return "color_shift"

    return "structural_diff"


def visual_diff(
    original_path: str,
    rendered_path: str,
    output_diff_path: str | None = None,
) -> dict:
    img1 = Image.open(original_path).convert("RGB")
    img2 = Image.open(rendered_path).convert("RGB")

    # Resize to match if different sizes
    w1, h1 = img1.size
    w2, h2 = img2.size
    if (w1, h1) != (w2, h2):
        img2 = img2.resize((w1, h1), Image.LANCZOS)

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    gray1 = np.array(img1.convert("L"))
    gray2 = np.array(img2.convert("L"))

    # SSIM
    overall_ssim, ssim_map = compute_ssim(gray1, gray2)

    # Pixel diff
    mismatch_count, diff_vis = pixel_diff(arr1, arr2)
    total_pixels = w1 * h1
    mismatch_pct = round(mismatch_count / total_pixels * 100, 2)

    # Find diff regions
    regions = _find_diff_regions(ssim_map)

    # Classify issues
    region_diffs = []
    for region in regions[:10]:  # Max 10 regions
        issue = _guess_issue(region, arr1, arr2)
        region_diffs.append({
            "bbox": region["bbox"],
            "ssim": region["mean_ssim"],
            "area": region["area"],
            "issue": issue,
        })

    # Save diff image if requested
    if output_diff_path:
        diff_img = Image.fromarray(diff_vis)
        draw = ImageDraw.Draw(diff_img)
        for rd in region_diffs:
            b = rd["bbox"]
            draw.rectangle(
                [b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]],
                outline="red", width=2,
            )
        diff_img.save(output_diff_path)

    # Suggested fixes
    fixes = []
    for rd in region_diffs:
        issue = rd["issue"]
        if issue == "color_mismatch":
            fixes.append(f"Re-check color token at region ({rd['bbox']['x']},{rd['bbox']['y']})")
        elif issue == "texture_or_shadow_diff":
            fixes.append(f"Shadow/gradient params may be off at ({rd['bbox']['x']},{rd['bbox']['y']})")
        elif issue == "border_or_divider_diff":
            fixes.append(f"Border width or color differs at y={rd['bbox']['y']}")
        elif issue == "color_shift":
            fixes.append(f"Slight color shift at ({rd['bbox']['x']},{rd['bbox']['y']}) — check opacity or blend mode")

    return {
        "overall_ssim": round(overall_ssim, 4),
        "mismatch_pixels": mismatch_count,
        "mismatch_percent": mismatch_pct,
        "total_pixels": total_pixels,
        "region_diffs": region_diffs,
        "suggested_fixes": fixes,
        "diff_image": output_diff_path,
        "verdict": "pass" if overall_ssim > 0.92 else ("acceptable" if overall_ssim > 0.85 else "fail"),
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python visual_diff.py <original> <rendered> [--output diff.png]", file=sys.stderr)
        sys.exit(1)

    original = sys.argv[1]
    rendered = sys.argv[2]

    for p in [original, rendered]:
        if not Path(p).exists():
            print(f"Error: {p} not found", file=sys.stderr)
            sys.exit(1)

    output = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output = sys.argv[idx + 1]

    result = visual_diff(original, rendered, output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
