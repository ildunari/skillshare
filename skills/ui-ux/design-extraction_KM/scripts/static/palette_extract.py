#!/usr/bin/env python3
"""
palette_extract.py — K-means color clustering on screenshots.

Input:  image path (PNG/JPG)
Output: JSON list of {hex, rgb, lab, frequency, role_guess, samples, confidence}

Method:
  1. Downsample to 256px max side for stability
  2. Convert to CIE LAB for perceptual clustering
  3. K-means with elbow method for optimal K (range 4–16)
  4. Merge near-duplicates by ΔE2000 < 5
  5. Assign semantic roles via frequency + luminance heuristics
"""

import json
import sys
import math
from pathlib import Path

import numpy as np
from PIL import Image


# ---------------------------------------------------------------------------
# CIE LAB / ΔE helpers (no scipy needed)
# ---------------------------------------------------------------------------

def _rgb_to_xyz(rgb: np.ndarray) -> np.ndarray:
    """sRGB [0,255] → XYZ D65."""
    rgb_lin = rgb.astype(np.float64) / 255.0
    mask = rgb_lin > 0.04045
    rgb_lin[mask] = ((rgb_lin[mask] + 0.055) / 1.055) ** 2.4
    rgb_lin[~mask] = rgb_lin[~mask] / 12.92
    mat = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    return rgb_lin @ mat.T


def _xyz_to_lab(xyz: np.ndarray) -> np.ndarray:
    """XYZ D65 → CIE LAB."""
    ref = np.array([0.95047, 1.0, 1.08883])
    xyz_n = xyz / ref
    eps = 0.008856
    kappa = 903.3
    mask = xyz_n > eps
    f = np.where(mask, np.cbrt(xyz_n), (kappa * xyz_n + 16.0) / 116.0)
    L = 116.0 * f[:, 1] - 16.0
    a = 500.0 * (f[:, 0] - f[:, 1])
    b = 200.0 * (f[:, 1] - f[:, 2])
    return np.column_stack([L, a, b])


def rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    return _xyz_to_lab(_rgb_to_xyz(rgb))


def delta_e_cie76(lab1: np.ndarray, lab2: np.ndarray) -> float:
    """Simple Euclidean ΔE (CIE76). Good enough for merge decisions."""
    return float(np.sqrt(np.sum((lab1 - lab2) ** 2)))


# ---------------------------------------------------------------------------
# K-means implementation (avoid sklearn dependency)
# ---------------------------------------------------------------------------

def _kmeans(data: np.ndarray, k: int, max_iter: int = 30, seed: int = 42) -> tuple:
    rng = np.random.RandomState(seed)
    idx = rng.choice(len(data), k, replace=False)
    centers = data[idx].copy()
    labels = np.zeros(len(data), dtype=int)

    for _ in range(max_iter):
        dists = np.linalg.norm(data[:, None, :] - centers[None, :, :], axis=2)
        new_labels = dists.argmin(axis=1)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for c in range(k):
            mask = labels == c
            if mask.any():
                centers[c] = data[mask].mean(axis=0)

    inertia = 0.0
    for c in range(k):
        mask = labels == c
        if mask.any():
            inertia += np.sum((data[mask] - centers[c]) ** 2)
    return centers, labels, inertia


def _find_optimal_k(data: np.ndarray, k_min: int = 4, k_max: int = 14) -> int:
    """Elbow method: find K where adding more clusters gives diminishing returns."""
    inertias = []
    ks = list(range(k_min, k_max + 1))
    for k in ks:
        _, _, inertia = _kmeans(data, k)
        inertias.append(inertia)

    # Find elbow via maximum second derivative
    if len(inertias) < 3:
        return k_min
    d1 = [inertias[i] - inertias[i + 1] for i in range(len(inertias) - 1)]
    d2 = [d1[i] - d1[i + 1] for i in range(len(d1) - 1)]
    elbow_idx = np.argmax(d2)
    return ks[elbow_idx + 1]


# ---------------------------------------------------------------------------
# Semantic role assignment
# ---------------------------------------------------------------------------

def _guess_role(lab: np.ndarray, frequency: float, rank: int, total_colors: int) -> str:
    L, a, b = lab
    chroma = math.sqrt(a ** 2 + b ** 2)

    # Very light, high frequency → surface/background
    if L > 92 and frequency > 0.15:
        return "surface"
    # Very dark, high frequency → surface-dark (dark mode)
    if L < 15 and frequency > 0.15:
        return "surface-dark"
    # High chroma, moderate frequency → accent or primary
    if chroma > 30:
        if rank == 0 or frequency > 0.05:
            return "primary"
        return "accent"
    # Low chroma, moderate L → neutral/text
    if chroma < 15:
        if L < 35:
            return "text-primary"
        if L < 60:
            return "text-secondary"
        return "neutral"
    # Medium chroma → semantic colors
    if a > 15 and b < 0:
        return "error"  # reddish
    if a < -10 and b > 10:
        return "success"  # greenish
    if b > 30 and a > -5:
        return "warning"  # yellowish

    return "unknown"


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------

def extract_palette(
    image_path: str,
    max_side: int = 256,
    k_min: int = 4,
    k_max: int = 14,
    merge_threshold_de: float = 5.0,
) -> list[dict]:
    img = Image.open(image_path).convert("RGB")

    # Downsample
    w, h = img.size
    scale = max_side / max(w, h)
    if scale < 1.0:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    pixels = np.array(img).reshape(-1, 3)
    total_pixels = len(pixels)

    # Convert to LAB
    lab_pixels = rgb_to_lab(pixels)

    # Find optimal K
    k = _find_optimal_k(lab_pixels, k_min, k_max)
    centers_lab, labels, _ = _kmeans(lab_pixels, k)

    # Compute per-cluster stats
    clusters = []
    for c in range(k):
        mask = labels == c
        count = mask.sum()
        if count == 0:
            continue
        freq = count / total_pixels
        center_lab = centers_lab[c]
        # Convert center back to RGB
        cluster_rgb = pixels[mask].mean(axis=0).astype(int)
        # Sample 3 representative pixel locations
        indices = np.where(mask)[0]
        sample_indices = indices[np.linspace(0, len(indices) - 1, min(3, len(indices)), dtype=int)]
        sw, sh = img.size
        samples = [
            {"x": int(idx % sw), "y": int(idx // sw)}
            for idx in sample_indices
        ]
        clusters.append({
            "rgb": [int(cluster_rgb[0]), int(cluster_rgb[1]), int(cluster_rgb[2])],
            "lab": [float(center_lab[0]), float(center_lab[1]), float(center_lab[2])],
            "frequency": round(freq, 4),
            "samples": samples,
        })

    # Sort by frequency descending
    clusters.sort(key=lambda c: c["frequency"], reverse=True)

    # Merge near-duplicates
    merged = []
    for cluster in clusters:
        is_dup = False
        for existing in merged:
            de = delta_e_cie76(
                np.array(cluster["lab"]),
                np.array(existing["lab"]),
            )
            if de < merge_threshold_de:
                existing["frequency"] += cluster["frequency"]
                existing["samples"].extend(cluster["samples"])
                is_dup = True
                break
        if not is_dup:
            merged.append(cluster)

    # Re-sort after merging
    merged.sort(key=lambda c: c["frequency"], reverse=True)

    # Build output with hex + role
    results = []
    for rank, c in enumerate(merged):
        r, g, b = c["rgb"]
        hex_val = f"#{r:02X}{g:02X}{b:02X}"
        role = _guess_role(np.array(c["lab"]), c["frequency"], rank, len(merged))
        confidence = min(0.95, 0.7 + c["frequency"] * 2)  # Higher frequency → higher confidence
        results.append({
            "hex": hex_val,
            "rgb": c["rgb"],
            "lab": [round(v, 2) for v in c["lab"]],
            "frequency": c["frequency"],
            "role_guess": role,
            "confidence": round(confidence, 3),
            "samples": c["samples"][:3],
        })

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python palette_extract.py <image_path> [--json]", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: {image_path} not found", file=sys.stderr)
        sys.exit(1)

    result = extract_palette(image_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
