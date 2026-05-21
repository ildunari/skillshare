#!/usr/bin/env python3
"""
asset_planning.py

Deterministic asset planning pass for deck IR.

Produces a machine-readable report used by pipeline/preflight to reason about
missing assets before rendering.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_elements(slide: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    stack = list(slide.get("elements") or [])
    while stack:
        el = stack.pop(0)
        if isinstance(el, dict):
            yield el
            children = el.get("children") or []
            if isinstance(children, list):
                stack[0:0] = children


def classify_asset(el: Dict[str, Any]) -> str:
    stype = str(el.get("semantic_type") or el.get("type") or "").lower()
    if stype in {"image", "picture"}:
        return "image"
    if stype in {"icon"}:
        return "icon"
    if stype in {"chart", "sparkline"}:
        return "chart"
    return "none"


def has_resolved_asset(el: Dict[str, Any], asset_type: str) -> bool:
    if asset_type == "image":
        for key in ("src", "path", "image", "url"):
            val = el.get(key)
            if isinstance(val, str) and val.strip():
                return True
        image_ref = el.get("imageRef")
        if isinstance(image_ref, dict):
            for key in ("src", "path", "url"):
                val = image_ref.get(key)
                if isinstance(val, str) and val.strip():
                    return True
        return False
    if asset_type == "icon":
        icon_ref = el.get("iconRef")
        return isinstance(icon_ref, dict) and bool(icon_ref.get("set")) and bool(icon_ref.get("name"))
    if asset_type == "chart":
        spec = el.get("chartSpec") or el.get("data")
        return isinstance(spec, dict) and bool(spec)
    return True


def plan_assets(ir: Dict[str, Any]) -> Dict[str, Any]:
    deck = ir.get("deck") if isinstance(ir.get("deck"), dict) else {}
    slides = deck.get("slides") if isinstance(deck.get("slides"), list) else []
    report: Dict[str, Any] = {
        "version": 1,
        "slides": [],
        "missing_assets": [],
        "unresolved_assets": 0,
    }

    for idx, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        sid = str(slide.get("id") or f"S{idx+1:02d}")
        row = {
            "slide_id": sid,
            "archetype": slide.get("archetype"),
            "assets": [],
        }
        for el in iter_elements(slide):
            asset_type = classify_asset(el)
            if asset_type == "none":
                continue
            required = asset_type in {"image", "chart"}
            resolved = has_resolved_asset(el, asset_type)
            item = {
                "element_id": el.get("id"),
                "asset_type": asset_type,
                "required": required,
                "resolved": resolved,
                "fallback": "use themed abstract background" if asset_type == "image" else "omit non-critical decorative asset",
            }
            row["assets"].append(item)
            if required and not resolved:
                report["missing_assets"].append(
                    {
                        "slide_id": sid,
                        "asset_type": asset_type,
                        "element_id": el.get("id"),
                    }
                )
        report["slides"].append(row)

    report["unresolved_assets"] = len(report["missing_assets"])
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ir", type=Path, help="Input deck IR JSON")
    ap.add_argument("--out", type=Path, required=True, help="Output asset planning report JSON")
    args = ap.parse_args()

    ir = load_json(args.ir)
    report = plan_assets(ir)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"[asset_planning] slides={len(report['slides'])} "
        f"unresolved_assets={report['unresolved_assets']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

