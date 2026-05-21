#!/usr/bin/env python3
"""
static_validators.py — Validate extracted design specs.

Checks:
  - Token format and consistency (DTCG compliance, near-duplicates, scale coherence)
  - Component sanity (token refs resolve, bbox valid, required styles)
  - Layout consistency (hierarchy complete, spacing on-grid)
  - Confidence thresholds (flag items below accept/iterate/reject levels)

Input:  design spec JSON (matching design-spec.schema.json)
Output: JSON validation report
"""

import json
import sys
import math
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_str: str) -> tuple[int, int, int] | None:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    if len(hex_str) == 6:
        return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
    if len(hex_str) == 8:
        return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
    return None


def _rgb_to_lab(r: int, g: int, b: int) -> tuple[float, float, float]:
    """sRGB → CIE LAB (D65)."""
    def _lin(c):
        c = c / 255.0
        return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92

    rl, gl, bl = _lin(r), _lin(g), _lin(b)
    x = rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375
    y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    z = rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041

    def _f(t):
        return t ** (1/3) if t > 0.008856 else (903.3 * t + 16) / 116

    xn, yn, zn = x / 0.95047, y / 1.0, z / 1.08883
    L = 116 * _f(yn) - 16
    a = 500 * (_f(xn) - _f(yn))
    b_val = 200 * (_f(yn) - _f(zn))
    return L, a, b_val


def _delta_e(hex1: str, hex2: str) -> float:
    """CIE76 ΔE between two hex colors."""
    rgb1 = _hex_to_rgb(hex1)
    rgb2 = _hex_to_rgb(hex2)
    if not rgb1 or not rgb2:
        return 999.0
    lab1 = _rgb_to_lab(*rgb1)
    lab2 = _rgb_to_lab(*rgb2)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(lab1, lab2)))


# ---------------------------------------------------------------------------
# Token tree traversal
# ---------------------------------------------------------------------------

def _flatten_tokens(node: dict, prefix: str = "") -> dict[str, dict]:
    """Flatten DTCG token tree into {path: token_obj}."""
    result = {}
    for key, value in node.items():
        if key.startswith("$"):
            continue
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            if "$value" in value:
                result[path] = value
            else:
                result.update(_flatten_tokens(value, path))
    return result


def _parse_dimension(value) -> float | None:
    """Extract numeric value from dimension token."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = re.match(r"([\d.]+)", value)
        if m:
            return float(m.group(1))
    return None


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------

def validate_tokens(spec: dict, config: dict) -> list[dict]:
    """Validate token format, consistency, and near-duplicates."""
    checks = []
    tokens = _flatten_tokens(spec.get("tokens", {}))
    token_meta = spec.get("tokenMeta", {})

    # Check DTCG format
    for path, token in tokens.items():
        if "$type" not in token:
            checks.append({
                "name": f"missing_$type:{path}",
                "category": "token_consistency",
                "passed": False,
                "score": 0.0,
                "notes": f"Token {path} missing required $type field",
            })

    # Check color near-duplicates
    color_tokens = {p: t for p, t in tokens.items() if t.get("$type") == "color"}
    color_hexes = {}
    for path, token in color_tokens.items():
        val = token.get("$value", "")
        if isinstance(val, str) and val.startswith("#"):
            color_hexes[path] = val

    checked_pairs = set()
    for p1, h1 in color_hexes.items():
        for p2, h2 in color_hexes.items():
            if p1 >= p2:
                continue
            pair = (p1, p2)
            if pair in checked_pairs:
                continue
            checked_pairs.add(pair)
            de = _delta_e(h1, h2)
            if de < 8:
                checks.append({
                    "name": f"near_duplicate_colors",
                    "category": "token_consistency",
                    "passed": de > 5,
                    "score": round(1.0 - (8 - de) / 8, 2),
                    "notes": f"{p1} ({h1}) and {p2} ({h2}) differ by ΔE={de:.1f} — consider merging",
                })

    # Check spacing scale consistency
    space_tokens = {p: t for p, t in tokens.items() if "space" in p}
    space_values = []
    for path, token in space_tokens.items():
        val = _parse_dimension(token.get("$value"))
        if val is not None:
            space_values.append(val)

    if len(space_values) >= 3:
        space_values.sort()
        on_grid = sum(1 for v in space_values if v % 4 < 1.5) / len(space_values)
        checks.append({
            "name": "spacing_scale_consistency",
            "category": "token_consistency",
            "passed": on_grid > 0.7,
            "score": round(on_grid, 3),
            "notes": f"{on_grid*100:.0f}% of spacing values on 4px grid",
        })

    # Check confidence thresholds
    thresholds = config.get("thresholds", {})
    for path, meta in token_meta.items():
        conf = meta.get("confidence", 0)
        token_type = path.split(".")[0]  # e.g. "color", "space", "typography"
        thresh = thresholds.get(token_type, thresholds.get("default", {}))
        accept = thresh.get("accept", 0.8)
        reject = thresh.get("reject", 0.4)

        if conf < reject:
            checks.append({
                "name": f"confidence_below_reject:{path}",
                "category": "token_consistency",
                "passed": False,
                "score": round(conf, 3),
                "notes": f"{path} confidence {conf:.2f} below reject threshold {reject}",
            })
        elif conf < accept:
            checks.append({
                "name": f"confidence_needs_iteration:{path}",
                "category": "token_consistency",
                "passed": True,
                "score": round(conf, 3),
                "notes": f"{path} confidence {conf:.2f} — iteration recommended (accept={accept})",
            })

    if not checks:
        checks.append({
            "name": "token_format_valid",
            "category": "token_consistency",
            "passed": True,
            "score": 0.95,
        })

    return checks


def validate_components(spec: dict) -> list[dict]:
    """Validate component structure and token references."""
    checks = []
    tokens = _flatten_tokens(spec.get("tokens", {}))
    token_paths = set(tokens.keys())
    components = spec.get("components", [])

    for comp in components:
        comp_id = comp.get("id", "unknown")

        # Check bbox validity
        bbox = comp.get("bbox", {})
        if bbox:
            x, y, bw, bh = bbox.get("x", 0), bbox.get("y", 0), bbox.get("w", 0), bbox.get("h", 0)
            if bw <= 0 or bh <= 0:
                checks.append({
                    "name": f"invalid_bbox:{comp_id}",
                    "category": "component_sanity",
                    "passed": False,
                    "score": 0.0,
                    "notes": f"Component {comp_id} has zero or negative dimensions",
                })
            if bbox.get("unit") == "norm" and (x + bw > 1.05 or y + bh > 1.05):
                checks.append({
                    "name": f"bbox_out_of_bounds:{comp_id}",
                    "category": "component_sanity",
                    "passed": False,
                    "score": 0.3,
                    "notes": f"Component {comp_id} bbox extends beyond screen bounds",
                })

        # Check token references resolve
        styles = comp.get("styles", {})
        token_refs = styles.get("tokenRefs", {})
        for prop, ref in token_refs.items():
            if ref not in token_paths:
                checks.append({
                    "name": f"broken_token_ref:{comp_id}.{prop}",
                    "category": "component_sanity",
                    "passed": False,
                    "score": 0.2,
                    "notes": f"Component {comp_id} references token '{ref}' which doesn't exist",
                })

        # Type-specific checks
        comp_type = comp.get("type", "").lower()
        if comp_type == "button":
            if not comp.get("text") and "text" not in token_refs:
                checks.append({
                    "name": f"button_missing_text:{comp_id}",
                    "category": "component_sanity",
                    "passed": False,
                    "score": 0.5,
                    "notes": f"Button {comp_id} has no text content",
                })
            if "background" not in token_refs and "background" not in styles.get("raw", {}):
                checks.append({
                    "name": f"button_missing_bg:{comp_id}",
                    "category": "component_sanity",
                    "passed": False,
                    "score": 0.6,
                    "notes": f"Button {comp_id} has no background color",
                })

    if not checks:
        checks.append({
            "name": "components_valid",
            "category": "component_sanity",
            "passed": True,
            "score": 0.90,
        })

    return checks


def validate_layout(spec: dict) -> list[dict]:
    """Validate layout hierarchy and spacing consistency."""
    checks = []
    layout = spec.get("layout", {})
    components = spec.get("components", [])
    comp_ids = {c["id"] for c in components}

    # Check hierarchy contains all components
    hierarchy = layout.get("hierarchy", {})

    def _collect_ids(node):
        ids = set()
        nid = node.get("id", "")
        if nid:
            ids.add(nid)
        for child in node.get("children", []):
            ids.update(_collect_ids(child))
        return ids

    hierarchy_ids = _collect_ids(hierarchy)
    missing = comp_ids - hierarchy_ids
    if missing:
        checks.append({
            "name": "hierarchy_incomplete",
            "category": "layout_consistency",
            "passed": False,
            "score": round(1.0 - len(missing) / max(len(comp_ids), 1), 2),
            "notes": f"Components not in hierarchy: {', '.join(sorted(missing))}",
        })
    else:
        checks.append({
            "name": "hierarchy_complete",
            "category": "layout_consistency",
            "passed": True,
            "score": 0.95,
        })

    # Check grid consistency
    grid = layout.get("grid", {})
    spacing_unit = grid.get("spacingUnitPx", 0)
    if spacing_unit > 0:
        margin = grid.get("marginPx", 0)
        gutter = grid.get("gutterPx", 0)
        margin_on_grid = margin % spacing_unit < 2
        gutter_on_grid = gutter % spacing_unit < 2
        checks.append({
            "name": "grid_values_consistent",
            "category": "layout_consistency",
            "passed": margin_on_grid and gutter_on_grid,
            "score": 0.85 if (margin_on_grid and gutter_on_grid) else 0.5,
            "notes": f"Margin={margin}px, Gutter={gutter}px on {spacing_unit}px grid",
        })

    return checks


# ---------------------------------------------------------------------------
# Main validator
# ---------------------------------------------------------------------------

def validate_spec(spec: dict, config: dict | None = None) -> dict:
    """Run all validation checks and compute overall score."""
    if config is None:
        config = {"thresholds": {"default": {"accept": 0.8, "reject": 0.4}}}

    all_checks = []
    all_checks.extend(validate_tokens(spec, config))
    all_checks.extend(validate_components(spec))
    all_checks.extend(validate_layout(spec))

    # Compute weighted overall score
    weights = {
        "token_consistency": 0.30,
        "component_sanity": 0.25,
        "layout_consistency": 0.20,
        "visual_parity": 0.25,
    }

    category_scores = {}
    for check in all_checks:
        cat = check.get("category", "other")
        if cat not in category_scores:
            category_scores[cat] = []
        category_scores[cat].append(check["score"])

    overall = 0.0
    for cat, w in weights.items():
        scores = category_scores.get(cat, [])
        if scores:
            overall += w * (sum(scores) / len(scores))
        else:
            overall += w * 0.5  # Unknown categories get neutral score

    passed = all(c["passed"] for c in all_checks if c["score"] >= 0.5)
    failed_critical = [c for c in all_checks if not c["passed"] and c["score"] < 0.3]

    return {
        "passed": len(failed_critical) == 0 and overall >= 0.7,
        "overallScore": round(overall, 3),
        "checks": all_checks,
        "summary": {
            "total_checks": len(all_checks),
            "passed": sum(1 for c in all_checks if c["passed"]),
            "failed": sum(1 for c in all_checks if not c["passed"]),
            "critical_failures": len(failed_critical),
        },
        "decision": (
            "finalize" if overall >= 0.85
            else "iterate" if overall >= 0.65
            else "human_review"
        ),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python static_validators.py <spec.json> [config.json]", file=sys.stderr)
        sys.exit(1)

    spec_path = sys.argv[1]
    with open(spec_path) as f:
        spec = json.load(f)

    config = None
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            config = json.load(f)

    result = validate_spec(spec, config)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
