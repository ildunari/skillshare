#!/usr/bin/env python3
"""
auto_fix_ir.py

Deterministic, localized QA fix ladder for Slide Deck IR.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set


OVERFLOW_CODES = {
    "OVERFLOW",
    "TEXT_WALL",
    "T1_TEXT_OVERFLOW_EST",
    "T2_TEXT_TIGHT_EST",
    "DENSITY_HIGH",
}
ALIGNMENT_CODES = {"A1_ALIGNMENT_OFF", "MISALIGNED_EDGES"}
INVALID_THEME_CODES = {"D0_THEME_NOT_FOUND", "THEME_INVALID", "INVALID_THEME"}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def iter_elements(elements: Iterable[Any]) -> Iterable[Dict[str, Any]]:
    for item in elements:
        if not isinstance(item, dict):
            continue
        yield item
        children = item.get("children")
        if isinstance(children, list):
            yield from iter_elements(children)


def slide_text_elements(slide: Dict[str, Any]) -> List[Dict[str, Any]]:
    elements = slide.get("elements")
    if not isinstance(elements, list):
        return []
    out: List[Dict[str, Any]] = []
    for el in iter_elements(elements):
        semantic = str(el.get("semantic_type") or el.get("type") or "").lower()
        if semantic in {"headline", "text", "caption", "quote", "number", "metric", "footer"}:
            out.append(el)
    return out


def normalize_align(value: Any) -> Any:
    mapping = {
        "centre": "center",
        "middle": "center",
        "mid": "center",
        "start": "left",
        "end": "right",
    }
    if not isinstance(value, str):
        return value
    key = value.strip().lower()
    return mapping.get(key, key if key in {"left", "center", "right", "justify"} else value)


def normalize_valign(value: Any) -> Any:
    mapping = {
        "middle": "mid",
        "center": "mid",
        "centre": "mid",
        "bottom": "bot",
    }
    if not isinstance(value, str):
        return value
    key = value.strip().lower()
    return mapping.get(key, key if key in {"top", "mid", "bot"} else value)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def is_headline_like(el: Dict[str, Any]) -> bool:
    semantic = str(el.get("semantic_type") or el.get("type") or "").lower()
    role = str(el.get("role") or el.get("semantic_role") or "").lower()
    return semantic in {"headline", "number"} or role in {"h1", "h2", "hero_metric"} or "headline" in role


def collect_codes(slide_report: Dict[str, Any]) -> Set[str]:
    out: Set[str] = set()
    for key in ("hard_fail", "warnings", "findings", "top_issues"):
        bucket = slide_report.get(key)
        if not isinstance(bucket, list):
            continue
        for item in bucket:
            if not isinstance(item, dict):
                continue
            code = item.get("code")
            if isinstance(code, str) and code.strip():
                out.add(code.strip())
    return out


def build_slide_report_lookup(qa_report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    lookup: Dict[str, Dict[str, Any]] = {}
    slides = qa_report.get("slides")
    if not isinstance(slides, list):
        return lookup
    for idx, slide_rep in enumerate(slides):
        if not isinstance(slide_rep, dict):
            continue
        lookup[f"idx:{idx}"] = slide_rep
        slide_id = slide_rep.get("slide_id")
        if isinstance(slide_id, str) and slide_id.strip():
            lookup[f"id:{slide_id.strip()}"] = slide_rep
        slide_number = slide_rep.get("slide_number")
        if isinstance(slide_number, int):
            lookup[f"num:{slide_number}"] = slide_rep
    return lookup


def find_report_for_slide(slide: Dict[str, Any], index: int, lookup: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    slide_id = slide.get("id")
    if isinstance(slide_id, str):
        hit = lookup.get(f"id:{slide_id.strip()}")
        if hit:
            return hit
    hit = lookup.get(f"num:{index + 1}")
    if hit:
        return hit
    return lookup.get(f"idx:{index}", {})


def load_theme_ids(themes_path: Optional[Path]) -> Set[str]:
    if not themes_path or not themes_path.exists():
        return set()
    try:
        payload = load_json(themes_path)
    except Exception:
        return set()
    themes = payload.get("themes") if isinstance(payload, dict) else None
    if not isinstance(themes, list):
        return set()
    out = set()
    for item in themes:
        if isinstance(item, dict):
            value = item.get("id")
            if isinstance(value, str) and value.strip():
                out.add(value.strip())
    return out


def normalize_alignment_tokens(slide: Dict[str, Any]) -> int:
    changed = 0
    for el in slide_text_elements(slide):
        st = el.get("style_tokens")
        if not isinstance(st, dict):
            continue
        new_align = normalize_align(st.get("align"))
        if new_align != st.get("align"):
            st["align"] = new_align
            changed += 1
        new_valign = normalize_valign(st.get("valign"))
        if new_valign != st.get("valign"):
            st["valign"] = new_valign
            changed += 1
    return changed


def reduce_text_pressure(
    slide: Dict[str, Any],
    max_font_step: int,
    font_floor_body: float,
    font_floor_headline: float,
) -> int:
    changed = 0
    for el in slide_text_elements(slide):
        st = el.get("style_tokens")
        if not isinstance(st, dict):
            continue

        if isinstance(st.get("lineHeight"), (int, float)):
            current = float(st["lineHeight"])
            floor = 1.0 if is_headline_like(el) else 1.1
            next_value = clamp(round(current - 0.05, 3), floor, 2.0)
            if next_value != current:
                st["lineHeight"] = next_value
                changed += 1

        for key in ("lineSpacingMultiple", "line_spacing"):
            if isinstance(st.get(key), (int, float)):
                current = float(st[key])
                floor = 1.0 if is_headline_like(el) else 1.1
                next_value = clamp(round(current - 0.05, 3), floor, 2.0)
                if next_value != current:
                    st[key] = next_value
                    changed += 1

        if isinstance(st.get("size"), (int, float)):
            size = float(st["size"])
            floor = font_floor_headline if is_headline_like(el) else font_floor_body
            next_size = max(floor, size - float(max(0, max_font_step)))
            if next_size < size:
                st["size"] = round(next_size, 2)
                changed += 1
    return changed


def seed_speaker_notes_from_overflow(slide: Dict[str, Any], max_items: int = 4) -> int:
    if slide.get("speaker_notes"):
        return 0
    extracted: List[str] = []
    for el in slide_text_elements(slide):
        content = el.get("content")
        if isinstance(content, str):
            txt = " ".join(content.strip().split())
            if len(txt) >= 48:
                extracted.append(txt)
        if len(extracted) >= max_items:
            break
    if not extracted:
        return 0
    slide["speaker_notes"] = [f"Overflow context: {item}" for item in extracted]
    return 1


def needs_theme_fallback(ir: Dict[str, Any], qa_report: Dict[str, Any], valid_theme_ids: Set[str]) -> bool:
    deck = ir.get("deck")
    if not isinstance(deck, dict):
        return False
    theme = deck.get("theme")
    theme_id = theme.get("id") if isinstance(theme, dict) else None
    invalid_by_registry = bool(valid_theme_ids) and isinstance(theme_id, str) and theme_id not in valid_theme_ids

    deck_warnings = qa_report.get("deck_warnings")
    if isinstance(deck_warnings, list):
        for item in deck_warnings:
            if isinstance(item, dict):
                code = item.get("code")
                if isinstance(code, str) and code in INVALID_THEME_CODES:
                    return True
    return invalid_by_registry


def apply_theme_fallback(ir: Dict[str, Any]) -> bool:
    deck = ir.get("deck")
    if not isinstance(deck, dict):
        return False
    mode = "light"
    current_theme = deck.get("theme")
    if isinstance(current_theme, dict):
        current_mode = current_theme.get("mode")
        if isinstance(current_mode, str) and current_mode.lower() in {"light", "dark"}:
            mode = current_mode.lower()
    fallback = {
        "id": "atlas",
        "mode": mode,
        "palette": {"id": "consulting_blue", "mode": mode},
    }
    if current_theme == fallback:
        return False
    deck["theme"] = fallback
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("qa_report", type=Path, help="QA report JSON (preflight_ir/preflight_pptx/vision)")
    ap.add_argument("ir", type=Path, help="Input IR JSON to repair")
    ap.add_argument("--out", type=Path, default=None, help="Output IR JSON path")
    ap.add_argument("--in-place", action="store_true", help="Overwrite input IR in place")
    ap.add_argument("--themes", type=Path, default=None, help="Optional themes.json path for theme validation")
    ap.add_argument("--max-font-step", type=int, default=1, help="Max pt reduction per pass (default: 1)")
    ap.add_argument("--font-floor-body", type=float, default=14.0, help="Body font floor in pt (default: 14)")
    ap.add_argument("--font-floor-headline", type=float, default=24.0, help="Headline font floor in pt (default: 24)")
    ap.add_argument("--changes-out", type=Path, default=None, help="Optional JSON change summary output")
    args = ap.parse_args()

    qa_report = load_json(args.qa_report)
    ir = load_json(args.ir)

    if args.in_place:
        out_path = args.ir
    else:
        out_path = args.out or args.ir.with_suffix(".fixed.ir.json")

    slide_lookup = build_slide_report_lookup(qa_report)
    slides = ((ir.get("deck") or {}).get("slides") or []) if isinstance(ir.get("deck"), dict) else []
    if not isinstance(slides, list):
        raise SystemExit("IR deck.slides must be a list")

    changes: List[Dict[str, Any]] = []
    total_changes = 0

    for idx, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        report_for_slide = find_report_for_slide(slide, idx, slide_lookup)
        codes = collect_codes(report_for_slide)
        if not codes:
            continue

        slide_id = str(slide.get("id") or f"S{idx + 1:02d}")
        slide_changes = {"slide_id": slide_id, "codes": sorted(codes), "applied": []}

        if codes & ALIGNMENT_CODES:
            changed = normalize_alignment_tokens(slide)
            if changed > 0:
                slide_changes["applied"].append({"fix": "normalize_alignment_tokens", "count": changed})
                total_changes += changed

        if codes & OVERFLOW_CODES:
            changed = reduce_text_pressure(
                slide,
                max_font_step=max(0, args.max_font_step),
                font_floor_body=float(args.font_floor_body),
                font_floor_headline=float(args.font_floor_headline),
            )
            if changed > 0:
                slide_changes["applied"].append({"fix": "reduce_text_pressure", "count": changed})
                total_changes += changed
            notes_added = seed_speaker_notes_from_overflow(slide)
            if notes_added > 0:
                slide_changes["applied"].append({"fix": "seed_speaker_notes_from_overflow", "count": notes_added})
                total_changes += notes_added

        if slide_changes["applied"]:
            changes.append(slide_changes)

    themes_path = args.themes or (Path(__file__).resolve().parents[1] / "assets" / "themes.json")
    valid_theme_ids = load_theme_ids(themes_path)
    theme_changed = False
    if needs_theme_fallback(ir, qa_report, valid_theme_ids):
        theme_changed = apply_theme_fallback(ir)
        if theme_changed:
            total_changes += 1

    save_json(out_path, ir)

    summary = {
        "qa_report": str(args.qa_report),
        "input_ir": str(args.ir),
        "output_ir": str(out_path),
        "total_changes": total_changes,
        "theme_fallback_applied": theme_changed,
        "slides_touched": len(changes),
        "slide_changes": changes,
    }

    if args.changes_out:
        save_json(args.changes_out, summary)

    print(
        "[auto_fix_ir] "
        f"slides_touched={summary['slides_touched']} "
        f"total_changes={summary['total_changes']} "
        f"theme_fallback_applied={summary['theme_fallback_applied']} "
        f"output={out_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
