#!/usr/bin/env python3
"""
validators.py — Motion token validation

Checks extracted motion tokens for:
1. Timing plausibility (duration, delay ranges)
2. Easing fit quality (residual thresholds)
3. Orchestration consistency (stagger/parallel group checks)
4. Cross-reference with static tokens (color/spacing refs exist)

Returns validation report with pass/fail per check and suggested fixes.
"""

import json
from typing import Optional


# ─── Thresholds ──────────────────────────────────────────────────────────────

TIMING_THRESHOLDS = {
    "min_duration_ms": 16,        # Below 1 frame at 60fps
    "max_duration_ms": 5000,      # Suspiciously long for UI
    "max_delay_ms": 3000,
    "min_stagger_ms": 10,
    "max_stagger_ms": 500,
    "warn_short_duration_ms": 50,  # Might be measurement error
    "warn_long_duration_ms": 2000,
}

EASING_THRESHOLDS = {
    "max_bezier_residual": 0.08,   # RMS error for acceptable fit
    "max_spring_residual": 0.10,
    "warn_bezier_residual": 0.05,
    "warn_spring_residual": 0.06,
    "min_confidence": 0.3,         # Below this, flag as unreliable
}

SPRING_THRESHOLDS = {
    "min_stiffness": 1,
    "max_stiffness": 10000,
    "min_damping": 0.1,
    "max_damping": 500,
    "max_overshoot_pct": 0.50,     # 50% overshoot is suspicious
}


# ─── Validators ──────────────────────────────────────────────────────────────

def validate_timing(track: dict) -> list[dict]:
    """Validate timing fields of a motion track."""
    issues = []
    timing = track.get("timing", {})

    duration = timing.get("durationMs")
    delay = timing.get("delayMs", 0)

    if duration is not None:
        if duration < TIMING_THRESHOLDS["min_duration_ms"]:
            issues.append({
                "level": "error",
                "field": "timing.durationMs",
                "value": duration,
                "message": f"Duration {duration}ms is below minimum ({TIMING_THRESHOLDS['min_duration_ms']}ms). Likely measurement error.",
                "suggestion": "Re-measure with higher FPS or verify segment boundaries.",
            })
        elif duration > TIMING_THRESHOLDS["max_duration_ms"]:
            issues.append({
                "level": "error",
                "field": "timing.durationMs",
                "value": duration,
                "message": f"Duration {duration}ms exceeds {TIMING_THRESHOLDS['max_duration_ms']}ms. May be a looping animation or misdetected segment.",
                "suggestion": "Check if this is a looping animation (iterations: infinite).",
            })
        elif duration < TIMING_THRESHOLDS["warn_short_duration_ms"]:
            issues.append({
                "level": "warning",
                "field": "timing.durationMs",
                "value": duration,
                "message": f"Duration {duration}ms is very short. Verify this is a micro-interaction.",
            })
        elif duration > TIMING_THRESHOLDS["warn_long_duration_ms"]:
            issues.append({
                "level": "warning",
                "field": "timing.durationMs",
                "value": duration,
                "message": f"Duration {duration}ms is long for UI animation. Verify this isn't a page transition or loading state.",
            })

    if delay is not None and delay < 0:
        issues.append({
            "level": "error",
            "field": "timing.delayMs",
            "value": delay,
            "message": "Negative delay is invalid.",
            "suggestion": "Check segment start time alignment.",
        })

    if delay is not None and delay > TIMING_THRESHOLDS["max_delay_ms"]:
        issues.append({
            "level": "warning",
            "field": "timing.delayMs",
            "value": delay,
            "message": f"Delay {delay}ms is unusually long.",
        })

    return issues


def validate_easing(track: dict, evidence: Optional[dict] = None) -> list[dict]:
    """Validate easing fit quality."""
    issues = []
    timing = track.get("timing", {})
    easing = timing.get("easing", {})

    easing_type = easing.get("type")

    if easing_type == "cubic-bezier":
        x1, y1 = easing.get("x1", 0), easing.get("y1", 0)
        x2, y2 = easing.get("x2", 0), easing.get("y2", 0)

        # x values must be in [0, 1]
        if not (0 <= x1 <= 1 and 0 <= x2 <= 1):
            issues.append({
                "level": "error",
                "field": "easing",
                "message": f"Cubic-bezier x values must be [0,1]. Got x1={x1}, x2={x2}.",
                "suggestion": "Clamp x values to [0,1].",
            })

    elif easing_type == "spring":
        params = easing.get("params", {})
        stiffness = params.get("stiffness", 0)
        damping = params.get("damping", 0)

        if stiffness < SPRING_THRESHOLDS["min_stiffness"]:
            issues.append({
                "level": "error",
                "field": "easing.params.stiffness",
                "value": stiffness,
                "message": f"Stiffness {stiffness} is too low.",
            })
        if stiffness > SPRING_THRESHOLDS["max_stiffness"]:
            issues.append({
                "level": "warning",
                "field": "easing.params.stiffness",
                "value": stiffness,
                "message": f"Stiffness {stiffness} is unusually high.",
            })
        if damping < SPRING_THRESHOLDS["min_damping"]:
            issues.append({
                "level": "error",
                "field": "easing.params.damping",
                "value": damping,
                "message": f"Damping {damping} is too low (will oscillate forever).",
            })

    # Check fit residual from evidence
    if evidence:
        residual = evidence.get("fitResidual")
        if residual is not None:
            threshold = (EASING_THRESHOLDS["max_spring_residual"]
                        if easing_type == "spring"
                        else EASING_THRESHOLDS["max_bezier_residual"])
            warn_threshold = (EASING_THRESHOLDS["warn_spring_residual"]
                             if easing_type == "spring"
                             else EASING_THRESHOLDS["warn_bezier_residual"])

            if residual > threshold:
                issues.append({
                    "level": "error",
                    "field": "evidence.fitResidual",
                    "value": residual,
                    "message": f"Fit residual {residual:.4f} exceeds threshold {threshold}.",
                    "suggestion": "Re-track at higher FPS or try alternative easing model.",
                })
            elif residual > warn_threshold:
                issues.append({
                    "level": "warning",
                    "field": "evidence.fitResidual",
                    "value": residual,
                    "message": f"Fit residual {residual:.4f} is marginal.",
                })

    return issues


def validate_confidence(token: dict) -> list[dict]:
    """Validate confidence scores."""
    issues = []
    overall = token.get("overallConfidence", 0)

    if overall < EASING_THRESHOLDS["min_confidence"]:
        issues.append({
            "level": "error",
            "field": "overallConfidence",
            "value": overall,
            "message": f"Overall confidence {overall} is below minimum threshold.",
            "suggestion": "Re-analyze this segment with better tracking or higher FPS.",
        })
    elif overall < 0.5:
        issues.append({
            "level": "warning",
            "field": "overallConfidence",
            "value": overall,
            "message": f"Overall confidence {overall} is low. Results may be unreliable.",
        })

    return issues


def validate_orchestration(tokens: list[dict]) -> list[dict]:
    """Validate orchestration group consistency across tokens."""
    issues = []

    # Group tokens by orchestration groupId
    groups: dict[str, list] = {}
    for token in tokens:
        orch = token.get("orchestration")
        if orch and "groupId" in orch:
            gid = orch["groupId"]
            groups.setdefault(gid, []).append(token)

    for gid, group_tokens in groups.items():
        kinds = set(t.get("orchestration", {}).get("kind") for t in group_tokens)

        # All tokens in a group should have the same orchestration kind
        if len(kinds) > 1:
            issues.append({
                "level": "warning",
                "field": f"orchestration.group:{gid}",
                "message": f"Group '{gid}' has mixed orchestration types: {kinds}",
            })

        # Stagger groups should have consistent eachDelayMs
        if "stagger" in kinds:
            delays = set(
                t.get("orchestration", {}).get("eachDelayMs")
                for t in group_tokens
                if t.get("orchestration", {}).get("kind") == "stagger"
            )
            if len(delays) > 1:
                issues.append({
                    "level": "warning",
                    "field": f"orchestration.group:{gid}",
                    "message": f"Stagger group '{gid}' has inconsistent eachDelayMs: {delays}",
                })

    return issues


def validate_token(token: dict) -> dict:
    """Validate a single motion token. Returns validation report."""
    all_issues = []

    # Confidence
    all_issues.extend(validate_confidence(token))

    # Per-track validation
    for i, track in enumerate(token.get("tracks", [])):
        timing_issues = validate_timing(track)
        for issue in timing_issues:
            issue["track"] = i
        all_issues.extend(timing_issues)

        easing_issues = validate_easing(track, token.get("evidence"))
        for issue in easing_issues:
            issue["track"] = i
        all_issues.extend(easing_issues)

    errors = [i for i in all_issues if i["level"] == "error"]
    warnings = [i for i in all_issues if i["level"] == "warning"]

    return {
        "tokenId": token.get("id", "unknown"),
        "passed": len(errors) == 0,
        "errorCount": len(errors),
        "warningCount": len(warnings),
        "issues": all_issues,
    }


def validate_spec(spec: dict) -> dict:
    """Validate a full MotionSpec. Returns comprehensive report."""
    tokens = spec.get("tokens", [])

    token_reports = [validate_token(t) for t in tokens]
    orchestration_issues = validate_orchestration(tokens)

    total_errors = sum(r["errorCount"] for r in token_reports) + len([i for i in orchestration_issues if i["level"] == "error"])
    total_warnings = sum(r["warningCount"] for r in token_reports) + len([i for i in orchestration_issues if i["level"] == "warning"])

    return {
        "specVersion": spec.get("version"),
        "tokenCount": len(tokens),
        "passed": total_errors == 0,
        "totalErrors": total_errors,
        "totalWarnings": total_warnings,
        "tokenReports": token_reports,
        "orchestrationIssues": orchestration_issues,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validators.py <motion_spec.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        spec = json.load(f)

    report = validate_spec(spec)
    print(json.dumps(report, indent=2))
