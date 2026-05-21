#!/usr/bin/env python3
"""
easing_fit.py — Easing curve fitting from observed motion data

Given a normalized (t, progress) time series extracted from video tracking,
fits candidate easing models and selects the best one.

Supports:
1. Cubic-bezier fitting (4-parameter optimization)
2. Spring/damped oscillator fitting
3. Linear detection
4. Steps detection
5. Snap-to-preset matching against known easing libraries

Output: Best-fit model with parameters, residual, and nearest preset name.
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional

import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.signal import find_peaks


# ─── Known Presets ────────────────────────────────────────────────────────────

BEZIER_PRESETS = {
    # CSS standard
    "ease": (0.25, 0.1, 0.25, 1.0),
    "ease-in": (0.42, 0.0, 1.0, 1.0),
    "ease-out": (0.0, 0.0, 0.58, 1.0),
    "ease-in-out": (0.42, 0.0, 0.58, 1.0),

    # Material Design
    "material-standard": (0.4, 0.0, 0.2, 1.0),
    "material-decelerate": (0.0, 0.0, 0.2, 1.0),
    "material-accelerate": (0.4, 0.0, 1.0, 1.0),
    "material-emphasized-decelerate": (0.05, 0.7, 0.1, 1.0),
    "material-emphasized-accelerate": (0.3, 0.0, 0.8, 0.15),

    # Apple (approximate)
    "ios-default": (0.25, 0.46, 0.45, 0.94),

    # GSAP equivalents
    "power2-out": (0.0, 0.0, 0.2, 1.0),
    "power3-inOut": (0.65, 0.0, 0.35, 1.0),
    "back-out": (0.34, 1.56, 0.64, 1.0),
}


# ─── Cubic Bezier Math ───────────────────────────────────────────────────────

def cubic_bezier_y(t_input: float, x1: float, y1: float, x2: float, y2: float, iterations: int = 20) -> float:
    """
    Evaluate CSS cubic-bezier at a given input time t_input ∈ [0,1].

    CSS cubic-bezier maps t → progress via a parametric curve:
    - x(u) = 3(1-u)²u·x1 + 3(1-u)u²·x2 + u³  (time axis)
    - y(u) = 3(1-u)²u·y1 + 3(1-u)u²·y2 + u³  (progress axis)

    We need to invert x(u) = t_input to find u, then evaluate y(u).
    """
    # Newton's method to find u such that x(u) = t_input
    u = t_input  # initial guess

    for _ in range(iterations):
        # x(u) = 3(1-u)^2 * u * x1 + 3(1-u) * u^2 * x2 + u^3
        x = 3 * (1 - u)**2 * u * x1 + 3 * (1 - u) * u**2 * x2 + u**3
        # dx/du
        dx = 3 * (1 - u)**2 * x1 + 6 * (1 - u) * u * (x2 - x1) + 3 * u**2 * (1 - x2)

        if abs(dx) < 1e-10:
            break

        u -= (x - t_input) / dx
        u = max(0.0, min(1.0, u))

    # Evaluate y at found u
    y = 3 * (1 - u)**2 * u * y1 + 3 * (1 - u) * u**2 * y2 + u**3
    return y


def bezier_curve(t_array: np.ndarray, x1: float, y1: float, x2: float, y2: float) -> np.ndarray:
    """Evaluate cubic-bezier for array of time values."""
    return np.array([cubic_bezier_y(t, x1, y1, x2, y2) for t in t_array])


# ─── Spring / Damped Oscillator ──────────────────────────────────────────────

def spring_curve(
    t_array: np.ndarray,
    stiffness: float,
    damping: float,
    mass: float = 1.0,
) -> np.ndarray:
    """
    Evaluate damped spring model: progress from 0 → 1 with possible overshoot.

    Uses the standard damped harmonic oscillator solution.
    """
    omega_n = np.sqrt(stiffness / mass)  # natural frequency
    zeta = damping / (2 * np.sqrt(stiffness * mass))  # damping ratio

    # Scale time: spring settles based on its own timescale
    # We work in absolute time here (t_array should be in seconds)
    t = t_array * omega_n  # dimensionless time

    if zeta < 1.0:  # underdamped (overshoot)
        omega_d = omega_n * np.sqrt(1 - zeta**2)
        t_real = t_array
        envelope = np.exp(-zeta * omega_n * t_real)
        progress = 1.0 - envelope * (
            np.cos(omega_d * t_real) +
            (zeta * omega_n / omega_d) * np.sin(omega_d * t_real)
        )
    elif zeta == 1.0:  # critically damped
        t_real = t_array
        progress = 1.0 - (1.0 + omega_n * t_real) * np.exp(-omega_n * t_real)
    else:  # overdamped
        s1 = -omega_n * (zeta + np.sqrt(zeta**2 - 1))
        s2 = -omega_n * (zeta - np.sqrt(zeta**2 - 1))
        c2 = -s1 / (s2 - s1)
        c1 = 1 - c2
        t_real = t_array
        progress = 1.0 - (c1 * np.exp(s1 * t_real) + c2 * np.exp(s2 * t_real))

    return np.clip(progress, -0.5, 1.5)  # allow overshoot but not crazy values


# ─── Classifiers ─────────────────────────────────────────────────────────────

def detect_overshoot(progress: np.ndarray, threshold: float = 0.02) -> dict:
    """Detect if progress overshoots 1.0 (spring behavior)."""
    max_val = np.max(progress)
    has_overshoot = max_val > (1.0 + threshold)

    # Count oscillations
    above_one = progress > 1.0 + threshold / 2
    crossings = np.diff(above_one.astype(int))
    oscillation_count = np.sum(crossings > 0)

    return {
        "hasOvershoot": bool(has_overshoot),
        "maxProgress": round(float(max_val), 4),
        "overshootAmount": round(float(max_val - 1.0), 4) if has_overshoot else 0.0,
        "oscillationCount": int(oscillation_count),
    }


def detect_steps(t_norm: np.ndarray, progress: np.ndarray, threshold: float = 0.1) -> Optional[int]:
    """Detect if motion is step-wise (CSS steps() easing)."""
    # Look for flat plateaus with sudden jumps
    diffs = np.abs(np.diff(progress))
    large_jumps = diffs > threshold
    flat_regions = diffs < 0.01

    if np.sum(large_jumps) >= 2 and np.sum(flat_regions) > len(progress) * 0.5:
        return int(np.sum(large_jumps))
    return None


def detect_linear(t_norm: np.ndarray, progress: np.ndarray, max_residual: float = 0.02) -> bool:
    """Detect if motion is approximately linear."""
    residual = np.sqrt(np.mean((progress - t_norm) ** 2))
    return residual < max_residual


# ─── Fitters ─────────────────────────────────────────────────────────────────

def fit_cubic_bezier(
    t_norm: np.ndarray,
    progress: np.ndarray,
) -> dict:
    """
    Fit cubic-bezier control points to observed progress curve.

    Returns {x1, y1, x2, y2, residual, presetMatch}.
    """
    def objective(params):
        x1, y1, x2, y2 = params
        predicted = bezier_curve(t_norm, x1, y1, x2, y2)
        return np.sum((predicted - progress) ** 2)

    # Bounds: x1,x2 in [0,1]; y1,y2 can slightly exceed for "back" eases
    bounds = [(0, 1), (-0.5, 2.0), (0, 1), (-0.5, 2.0)]

    # Try differential evolution for global search
    result = differential_evolution(objective, bounds, seed=42, maxiter=200, tol=1e-6)

    x1, y1, x2, y2 = result.x
    predicted = bezier_curve(t_norm, x1, y1, x2, y2)
    residual = float(np.sqrt(np.mean((predicted - progress) ** 2)))

    # Find closest preset
    preset_match = find_closest_preset(x1, y1, x2, y2)

    return {
        "type": "cubic-bezier",
        "x1": round(float(x1), 4),
        "y1": round(float(y1), 4),
        "x2": round(float(x2), 4),
        "y2": round(float(y2), 4),
        "residual": round(residual, 5),
        "presetMatch": preset_match,
    }


def fit_spring(
    t_norm: np.ndarray,
    progress: np.ndarray,
    duration_sec: float,
) -> dict:
    """
    Fit damped spring parameters to observed progress curve.

    Returns {stiffness, damping, mass, dampingRatio, residual}.
    """
    t_real = t_norm * duration_sec  # convert to real seconds

    def objective(params):
        stiffness, damping = params
        predicted = spring_curve(t_real, stiffness, damping, mass=1.0)
        return np.sum((predicted - progress) ** 2)

    bounds = [(10, 5000), (1, 200)]
    result = differential_evolution(objective, bounds, seed=42, maxiter=300, tol=1e-6)

    stiffness, damping = result.x
    mass = 1.0
    predicted = spring_curve(t_real, stiffness, damping, mass)
    residual = float(np.sqrt(np.mean((predicted - progress) ** 2)))

    omega_n = np.sqrt(stiffness / mass)
    damping_ratio = damping / (2 * np.sqrt(stiffness * mass))

    # Platform-specific mappings
    # iOS: response ≈ 2π/ω_n, dampingFraction ≈ ζ
    response = (2 * np.pi) / omega_n if omega_n > 0 else 1.0

    return {
        "type": "spring",
        "stiffness": round(float(stiffness), 1),
        "damping": round(float(damping), 1),
        "mass": mass,
        "dampingRatio": round(float(damping_ratio), 4),
        "residual": round(residual, 5),
        "platformHints": {
            "ios": {
                "response": round(float(response), 4),
                "dampingFraction": round(float(min(damping_ratio, 1.0)), 4),
            },
            "android": {
                "stiffness": round(float(stiffness), 1),
                "dampingRatio": round(float(damping_ratio), 4),
            },
            "framerMotion": {
                "stiffness": round(float(stiffness), 1),
                "damping": round(float(damping), 1),
                "mass": mass,
            },
        },
    }


def find_closest_preset(x1: float, y1: float, x2: float, y2: float) -> Optional[dict]:
    """Find the closest known easing preset to the fitted bezier."""
    best_name = None
    best_dist = float("inf")

    fitted = np.array([x1, y1, x2, y2])

    for name, preset in BEZIER_PRESETS.items():
        dist = float(np.linalg.norm(fitted - np.array(preset)))
        if dist < best_dist:
            best_dist = dist
            best_name = name

    if best_dist < 0.15:  # close enough to snap
        return {
            "name": best_name,
            "bezier": list(BEZIER_PRESETS[best_name]),
            "distance": round(best_dist, 4),
            "isExactMatch": best_dist < 0.02,
        }
    return None


# ─── Main Fit Pipeline ───────────────────────────────────────────────────────

def fit_easing(
    t_norm: np.ndarray,
    progress: np.ndarray,
    duration_sec: float,
) -> dict:
    """
    Full easing fitting pipeline. Tries all models, returns best fit.

    Args:
        t_norm: Normalized time array [0..1]
        progress: Normalized progress array [0..1] (may exceed 1 for springs)
        duration_sec: Actual duration in seconds (needed for spring fitting)

    Returns dict with:
        - bestModel: "linear" | "cubic-bezier" | "spring" | "steps"
        - models: {linear, cubicBezier, spring, steps} with params and residuals
        - recommendation: human-readable summary
        - overshoot: overshoot detection results
    """
    results = {
        "durationSec": round(duration_sec, 4),
        "sampleCount": len(t_norm),
    }

    # 1. Detect overshoot
    overshoot = detect_overshoot(progress)
    results["overshoot"] = overshoot

    # 2. Check for steps
    step_count = detect_steps(t_norm, progress)
    if step_count:
        results["bestModel"] = "steps"
        results["steps"] = {"steps": step_count}
        results["recommendation"] = f"Step-wise animation with {step_count} steps"
        return results

    # 3. Check for linear
    if detect_linear(t_norm, progress):
        results["bestModel"] = "linear"
        results["linear"] = {"residual": round(float(np.sqrt(np.mean((progress - t_norm)**2))), 5)}
        results["recommendation"] = "Linear easing (constant speed)"
        return results

    # 4. Fit cubic-bezier
    bezier_fit = fit_cubic_bezier(t_norm, progress)
    results["cubicBezier"] = bezier_fit

    # 5. Fit spring (only if overshoot or if bezier fit is poor)
    spring_fit = None
    if overshoot["hasOvershoot"] or bezier_fit["residual"] > 0.05:
        spring_fit = fit_spring(t_norm, progress, duration_sec)
        results["spring"] = spring_fit

    # 6. Select best model
    if spring_fit and overshoot["hasOvershoot"]:
        if spring_fit["residual"] < bezier_fit["residual"] * 1.2:
            results["bestModel"] = "spring"
            results["recommendation"] = (
                f"Spring animation (ζ={spring_fit['dampingRatio']:.2f}, "
                f"k={spring_fit['stiffness']:.0f}). "
                f"Overshoot: {overshoot['overshootAmount']:.1%}"
            )
        else:
            results["bestModel"] = "cubic-bezier"
            preset = bezier_fit.get("presetMatch")
            preset_str = f" (≈ {preset['name']})" if preset else ""
            results["recommendation"] = (
                f"Cubic-bezier{preset_str} despite overshoot — "
                f"bezier fit is better (residual: {bezier_fit['residual']:.4f})"
            )
    else:
        results["bestModel"] = "cubic-bezier"
        preset = bezier_fit.get("presetMatch")
        preset_str = f" (≈ {preset['name']})" if preset else ""
        results["recommendation"] = f"Cubic-bezier{preset_str}"

    return results


# ─── Convenience ─────────────────────────────────────────────────────────────

def fit_from_progress_list(
    progress_points: list[dict],  # [{tNorm, progress}, ...]
    duration_sec: float,
) -> dict:
    """Convenience: fit from the format stored in evidence.progressCurve."""
    t_norm = np.array([p["tNorm"] for p in progress_points])
    progress = np.array([p["progress"] for p in progress_points])
    return fit_easing(t_norm, progress, duration_sec)


if __name__ == "__main__":
    # Demo: fit a known material-standard curve with some noise
    np.random.seed(42)
    t = np.linspace(0, 1, 30)
    # Generate material-standard curve + noise
    true_progress = bezier_curve(t, 0.4, 0.0, 0.2, 1.0)
    noisy_progress = true_progress + np.random.normal(0, 0.01, len(t))
    noisy_progress = np.clip(noisy_progress, 0, 1)

    result = fit_easing(t, noisy_progress, duration_sec=0.3)
    print(json.dumps(result, indent=2))
