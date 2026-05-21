
#!/usr/bin/env python3
"""
preflight_ir.py

Static QA for pptx-master IR (before rendering).

What it checks (high-level):
- alignment consistency (existing)
- density/whitespace heuristics (existing)
- bbox overflow and text overflow risk (improved heuristic)
- WCAG contrast (NEW)
- cross-slide consistency (NEW)
- validation of newer IR features: theme refs, gradients, icons, animations (NEW)

The goal is to catch problems before PptxGenJS/OOXML rendering.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from text_metrics import measure_text_height
from validate_ir import validate_instance

EMU_PER_IN = 914400.0


# -------------------------
# Utilities
# -------------------------

def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_elements(slide: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """Yield slide elements recursively (includes children)."""
    stack = list(slide.get("elements") or [])
    while stack:
        el = stack.pop(0)
        yield el
        kids = el.get("children") or []
        if isinstance(kids, list):
            stack[0:0] = kids


def get_bbox(el: Dict[str, Any]) -> Optional[Dict[str, float]]:
    b = el.get("bbox")
    if not isinstance(b, dict):
        return None
    try:
        return {"x": float(b["x"]), "y": float(b["y"]), "w": float(b["w"]), "h": float(b["h"])}
    except Exception:
        return None


def bbox_contains(a: Dict[str, float], b: Dict[str, float], pad: float = 0.0) -> bool:
    return (
        a["x"] - pad <= b["x"]
        and a["y"] - pad <= b["y"]
        and a["x"] + a["w"] + pad >= b["x"] + b["w"]
        and a["y"] + a["h"] + pad >= b["y"] + b["h"]
    )


def bbox_area(b: Dict[str, float]) -> float:
    return max(0.0, b["w"]) * max(0.0, b["h"])


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


# -------------------------
# Colors + contrast
# -------------------------

HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")


def normalize_hex(s: str) -> Optional[str]:
    if not isinstance(s, str):
        return None
    s = s.strip()
    if not HEX_RE.match(s):
        return None
    if not s.startswith("#"):
        s = "#" + s
    return s.upper()


def hex_to_rgb(hex_s: str) -> Tuple[float, float, float]:
    hs = normalize_hex(hex_s)
    if hs is None:
        raise ValueError(f"Invalid hex color: {hex_s!r}")
    r = int(hs[1:3], 16) / 255.0
    g = int(hs[3:5], 16) / 255.0
    b = int(hs[5:7], 16) / 255.0
    return r, g, b


def srgb_to_linear(c: float) -> float:
    # WCAG conversion
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(hex_s: str) -> float:
    r, g, b = hex_to_rgb(hex_s)
    rl = srgb_to_linear(r)
    gl = srgb_to_linear(g)
    bl = srgb_to_linear(b)
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    L1 = rel_luminance(fg_hex)
    L2 = rel_luminance(bg_hex)
    lighter = max(L1, L2)
    darker = min(L1, L2)
    return (lighter + 0.05) / (darker + 0.05)


def resolve_color(value: Any, color_tokens: Dict[str, Any]) -> Optional[str]:
    """
    Resolve a color from:
      - token name (e.g. "fg")
      - hex literal "#RRGGBB"
    """
    if value is None:
        return None
    if isinstance(value, str):
        v = value.strip()
        # token name
        if v in color_tokens and isinstance(color_tokens[v], str):
            return normalize_hex(color_tokens[v])
        # hex literal
        hx = normalize_hex(v)
        if hx:
            return hx
    return None


def resolve_fill(value: Any, color_tokens: Dict[str, Any]) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Returns (solid_hex, gradient_obj).
    - If value is a token/hex: returns (hex, None)
    - If value is a gradient object: returns (None, gradient)
    """
    if value is None:
        return None, None
    if isinstance(value, str):
        return resolve_color(value, color_tokens), None
    if isinstance(value, dict) and value.get("type") in ("linear", "radial") and isinstance(value.get("stops"), list):
        return None, value
    return None, None


def min_contrast_against_gradient(fg_hex: str, grad: Dict[str, Any]) -> Optional[float]:
    stops = grad.get("stops")
    if not isinstance(stops, list) or len(stops) < 2:
        return None
    ratios = []
    for st in stops:
        if not isinstance(st, dict):
            continue
        c = st.get("color")
        hx = normalize_hex(c) if isinstance(c, str) else None
        if not hx:
            continue
        ratios.append(contrast_ratio(fg_hex, hx))
    if not ratios:
        return None
    return min(ratios)


# -------------------------
# Text measurement heuristic
# -------------------------

def resolve_font_size_pt(style_tokens: Dict[str, Any], tokens_sizes: Dict[str, Any], theme_sizes: Dict[str, Any]) -> float:
    v = (style_tokens or {}).get("size")
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        # token key lookups
        if v in tokens_sizes and isinstance(tokens_sizes[v], (int, float)):
            return float(tokens_sizes[v])
        if v in theme_sizes and isinstance(theme_sizes[v], (int, float)):
            return float(theme_sizes[v])
    # fallback
    if "body" in tokens_sizes and isinstance(tokens_sizes["body"], (int, float)):
        return float(tokens_sizes["body"])
    if "body" in theme_sizes and isinstance(theme_sizes["body"], (int, float)):
        return float(theme_sizes["body"])
    return 18.0


def is_bold(style_tokens: Dict[str, Any]) -> bool:
    if not isinstance(style_tokens, dict):
        return False
    if style_tokens.get("bold") is True:
        return True
    # allow 'weight' if provided
    w = style_tokens.get("weight")
    if isinstance(w, (int, float)) and w >= 600:
        return True
    return False


def _token_ref_name(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    name = value.strip()
    if not name:
        return None
    if normalize_hex(name):
        return None
    return name


def _append_finding(bucket: List[Dict[str, Any]], code: str, evidence: str, fix: str, target: str = "") -> None:
    item = {"code": code, "evidence": evidence, "fix": fix}
    if target:
        item["target"] = target
    bucket.append(item)


def _is_dominant_image_intent(element: Dict[str, Any]) -> bool:
    role = str(element.get("role") or "").lower()
    metadata = element.get("metadata") if isinstance(element.get("metadata"), dict) else {}
    intent = str(metadata.get("intent") or "").lower() if isinstance(metadata, dict) else ""
    return any(token in role for token in ("hero", "dominant", "main", "cover", "full")) or intent == "dominant" or metadata.get("dominant") is True


def _density_class(words: int, whitespace_ratio: float, dominant_image: bool) -> str:
    if dominant_image or whitespace_ratio >= 0.55:
        return "light"
    if words >= 40 or whitespace_ratio < 0.28:
        return "heavy"
    return "medium"


def load_ir(path: Path) -> Dict[str, Any]:
    return load_json(path)


def preflight(ir: Dict[str, Any], themes_path: Optional[Path] = None, palettes_path: Optional[Path] = None) -> Dict[str, Any]:
    deck = ir.get("deck", {}) if isinstance(ir.get("deck"), dict) else {}
    slides = deck.get("slides", [])
    if not isinstance(slides, list):
        slides = []
    tokens = deck.get("tokens", {}) if isinstance(deck.get("tokens"), dict) else {}
    color_tokens = dict(tokens.get("colors") or {}) if isinstance(tokens.get("colors"), dict) else {}
    size_tokens = tokens.get("sizes", {}) if isinstance(tokens.get("sizes"), dict) else {}
    theme_id = ((deck.get("theme") or {}).get("id")) if isinstance(deck.get("theme"), dict) else None
    theme_mode = ((deck.get("theme") or {}).get("mode")) if isinstance(deck.get("theme"), dict) else None

    report: Dict[str, Any] = {
        "summary": {
            "slides": len(slides),
            "hard_fail": 0,
            "warnings": 0,
            "deck_hard_fail": 0,
            "deck_warnings": 0,
            "schema_engine": "none",
            "schema_hard_fail": 0,
            "text_measure_tiers": {},
        },
        "deck": {
            "theme_id": theme_id,
            "theme_mode": theme_mode,
            "narrative_arc": deck.get("narrative_arc"),
        },
        "deck_hard_fail": [],
        "deck_warnings": [],
        "slides": [],
    }

    # First pass: full schema validation.
    schema_path = repo_root() / "references" / "ir.schema.json"
    schema_errors: List[Dict[str, str]] = []
    if not schema_path.exists():
        schema_errors = [{"path": "<schema>", "message": f"Schema not found at {schema_path}"}]
        report["summary"]["schema_engine"] = "missing"
    else:
        try:
            schema = load_json(schema_path)
            schema_engine, schema_errors = validate_instance(ir, schema)
            report["summary"]["schema_engine"] = schema_engine
        except Exception as exc:
            schema_errors = [{"path": "<root>", "message": f"Schema validation error: {exc}"}]
            report["summary"]["schema_engine"] = "error"

    for err in schema_errors:
        _append_finding(
            report["deck_hard_fail"],
            code="S1_SCHEMA_INVALID",
            evidence=f"{err.get('path', '<root>')}: {err.get('message', 'schema violation')}",
            fix="Update IR to conform to references/ir.schema.json.",
        )
    report["summary"]["schema_hard_fail"] = len(schema_errors)

    themes = None
    palettes = None
    theme_sizes: Dict[str, Any] = {}
    if themes_path and themes_path.exists():
        try:
            themes = load_json(themes_path)
        except Exception:
            themes = None
    if palettes_path and palettes_path.exists():
        try:
            palettes = load_json(palettes_path)
        except Exception:
            palettes = None

    if theme_id and themes and isinstance(themes, dict):
        tmatch = next((t for t in (themes.get("themes") or []) if isinstance(t, dict) and t.get("id") == theme_id), None)
        if not tmatch:
            _append_finding(
                report["deck_warnings"],
                code="D0_THEME_NOT_FOUND",
                evidence=f"deck.theme.id='{theme_id}' not present in themes.json",
                fix="Use a valid theme id from assets/themes.json or omit deck.theme.",
            )
        else:
            if isinstance(tmatch.get("typography"), dict):
                theme_sizes = (tmatch.get("typography") or {}).get("sizes_pt") or {}
            pal_ref = tmatch.get("palette")
            if not isinstance(pal_ref, dict) or not pal_ref.get("id"):
                _append_finding(
                    report["deck_hard_fail"],
                    code="D8_THEME_PALETTE_LINK_MISSING",
                    evidence=f"theme '{theme_id}' is missing palette linkage",
                    fix="Set theme.palette.id (and optional mode) in assets/themes.json.",
                )
            else:
                pal_id = pal_ref.get("id")
                pal_mode = theme_mode or pal_ref.get("mode") or "light"
                if palettes and isinstance(palettes, dict):
                    pmatch = next((p for p in (palettes.get("palettes") or []) if isinstance(p, dict) and p.get("id") == pal_id), None)
                    if not pmatch:
                        _append_finding(
                            report["deck_hard_fail"],
                            code="D9_THEME_PALETTE_NOT_FOUND",
                            evidence=f"theme '{theme_id}' links palette '{pal_id}', but it is missing in palettes.json",
                            fix="Fix theme.palette.id or add the missing palette entry.",
                        )
                    else:
                        modes = pmatch.get("modes") or {}
                        mode_tokens = modes.get(pal_mode) if isinstance(modes, dict) else None
                        if not isinstance(mode_tokens, dict):
                            _append_finding(
                                report["deck_hard_fail"],
                                code="D10_THEME_PALETTE_MODE_MISSING",
                                evidence=f"palette '{pal_id}' has no mode '{pal_mode}'",
                                fix="Use a valid deck.theme.mode or add that mode to palettes.json.",
                            )
                        else:
                            for key, value in mode_tokens.items():
                                if key not in color_tokens and isinstance(value, str):
                                    color_tokens[key] = value

    core_color_tokens = ("bg", "fg", "surface", "border")
    missing_core = [key for key in core_color_tokens if key not in color_tokens]
    if missing_core:
        _append_finding(
            report["deck_hard_fail"],
            code="D11_CORE_TOKENS_MISSING",
            evidence=f"missing required color tokens: {missing_core}",
            fix="Define core colors in deck.tokens.colors or through linked palette mode tokens.",
        )

    slide_ids = [str(s.get("id")) for s in slides if isinstance(s, dict) and s.get("id")]
    slide_index = {sid: idx for idx, sid in enumerate(slide_ids)}

    narrative_sections: set = set()
    narrative_arc = deck.get("narrative_arc")
    if isinstance(narrative_arc, list):
        for item in narrative_arc:
            if isinstance(item, str) and item.strip():
                narrative_sections.add(item.strip())
            elif isinstance(item, dict):
                section_name = item.get("section") or item.get("id") or item.get("name")
                if isinstance(section_name, str) and section_name.strip():
                    narrative_sections.add(section_name.strip())

    headline_positions: List[Tuple[str, float, float]] = []
    font_families: set = set()
    card_radii: set = set()
    archetype_sequence: List[Tuple[str, str]] = []
    density_sequence: List[Tuple[str, str]] = []
    section_counts: Counter = Counter()
    measurement_tiers: Counter = Counter()

    neutral_color_tokens = {
        "bg",
        "surface",
        "fg",
        "text",
        "muted",
        "muted_text",
        "border",
        "gridline",
        "axis",
        "annotation",
    }

    for idx, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        sid = str(slide.get("id") or f"slide[{idx}]")
        hard: List[Dict[str, Any]] = []
        warn: List[Dict[str, Any]] = []
        elems = list(iter_elements(slide))
        archetype = str(slide.get("archetype") or "")
        archetype_sequence.append((sid, archetype))

        section = slide.get("section")
        if isinstance(section, str) and section.strip():
            section_counts[section.strip()] += 1

        parent_slide = slide.get("parent_slide")
        if isinstance(parent_slide, str) and parent_slide.strip():
            p = parent_slide.strip()
            if p == sid:
                _append_finding(hard, "D12_PARENT_SLIDE_SELF", "slide.parent_slide points to itself", "Use another slide id or remove parent_slide.", sid)
            elif p not in slide_index:
                _append_finding(hard, "D13_PARENT_SLIDE_MISSING", f"slide.parent_slide='{p}' not found", "Use an existing slide id as parent_slide.", sid)
            elif slide_index[p] > idx:
                _append_finding(warn, "D14_PARENT_SLIDE_AFTER_CHILD", f"parent_slide='{p}' appears after this slide", "Place parent before child for deterministic narrative flow.", sid)

        headline_el = next((e for e in elems if (e.get("semantic_type") or "").lower() == "headline" and get_bbox(e)), None)
        if headline_el:
            hb = get_bbox(headline_el)
            if hb:
                headline_positions.append((sid, hb["x"], hb["y"]))

        for e in elems:
            st = e.get("style_tokens") if isinstance(e.get("style_tokens"), dict) else {}
            f = st.get("font")
            if isinstance(f, str):
                font_families.add(f)
            r = st.get("radius")
            if r is not None:
                if isinstance(r, (int, float)):
                    card_radii.add(round(float(r), 2))
                elif isinstance(r, str):
                    card_radii.add(r)

        for i, e in enumerate(slide.get("elements", []) or []):
            bbox = get_bbox(e)
            if not bbox:
                continue
            if bbox["x"] < 0 or bbox["y"] < 0 or bbox["x"] + bbox["w"] > 13.333 + 1e-6 or bbox["y"] + bbox["h"] > 7.5 + 1e-6:
                _append_finding(
                    hard,
                    "G1_OOB",
                    f"bbox={bbox}",
                    "Keep elements within slide bounds (or mark as full-bleed background).",
                    str(e.get("semantic_type") or f"element[{i}]"),
                )

        tol = 0.06
        lefts = []
        for e in slide.get("elements", []) or []:
            bbox = get_bbox(e)
            if bbox:
                lefts.append((e.get("semantic_type", ""), bbox["x"]))
        lefts.sort(key=lambda t: t[1])
        for j in range(1, len(lefts)):
            delta = abs(lefts[j][1] - lefts[j - 1][1])
            if tol < delta <= 0.16:
                _append_finding(
                    warn,
                    "A1_ALIGNMENT_OFF",
                    f"left edges differ by {delta:.2f} in ({lefts[j-1][0]} vs {lefts[j][0]})",
                    "Snap elements to a common grid column / margin.",
                )

        slide_words = 0
        slide_bullets = 0
        total_area = 13.333 * 7.5
        used_area = 0.0
        dominant_image_ratios: List[float] = []
        max_image_ratio = 0.0
        for e in elems:
            stype = (e.get("semantic_type") or "").lower()
            content = (e.get("content") or "") if isinstance(e.get("content"), str) else ""
            if stype in ("headline", "text", "caption", "quote"):
                slide_words += len(re.findall(r"\w+", content))
                slide_bullets += content.count("•") + content.count("- ")
            b = get_bbox(e)
            if b:
                used_area += bbox_area(b)
                if stype in ("image", "picture"):
                    ratio = bbox_area(b) / total_area
                    max_image_ratio = max(max_image_ratio, ratio)
                    if _is_dominant_image_intent(e):
                        dominant_image_ratios.append(ratio)
        whitespace_ratio = clamp(1.0 - (used_area / total_area), 0.0, 1.0)

        if whitespace_ratio < 0.22:
            _append_finding(
                hard,
                "A2_WHITESPACE_TOO_LOW",
                f"whitespace_ratio={whitespace_ratio:.3f} (< 0.22)",
                "Reduce content density or split this slide.",
            )

        for ratio in dominant_image_ratios:
            if ratio < 0.30:
                _append_finding(
                    hard,
                    "I2_IMAGE_DOMINANT_TOO_SMALL",
                    f"dominant image area ratio={ratio:.3f} (< 0.30 fail floor)",
                    "Increase dominant image area to at least 35% of slide area.",
                )
            elif ratio < 0.35:
                _append_finding(
                    warn,
                    "I3_IMAGE_DOMINANT_UNDERSIZED",
                    f"dominant image area ratio={ratio:.3f} (< 0.35 target)",
                    "Grow the image area to meet the >=35% dominance rule.",
                )

        density_profile = slide.get("density_profile") or deck.get("density_profile") or "comfortable"
        elem_count = len([e for e in elems if get_bbox(e)])
        if density_profile == "sparse":
            if elem_count > 10:
                _append_finding(warn, "D1_DENSE_FOR_SPARSE", f"{elem_count} elements", "Split slide or use a denser profile.")
        elif density_profile == "dense":
            if elem_count > 22:
                _append_finding(warn, "D2_TOO_MANY_ELEMENTS", f"{elem_count} elements", "Split slide; dense still has limits.")
        else:
            if elem_count > 18:
                _append_finding(warn, "D3_MANY_ELEMENTS", f"{elem_count} elements", "Consider simplifying or switching archetype.")

        backgrounds: List[Tuple[Dict[str, float], Optional[str], Optional[Dict[str, Any]]]] = []
        for e in elems:
            stype = (e.get("semantic_type") or "").lower()
            if stype in ("card", "panel", "shape"):
                b = get_bbox(e)
                if not b:
                    continue
                st = e.get("style_tokens") if isinstance(e.get("style_tokens"), dict) else {}
                fill_val = st.get("fill")
                solid, grad = resolve_fill(fill_val, color_tokens)
                if solid or grad:
                    backgrounds.append((b, solid, grad))
        slide_bg = resolve_color("bg", color_tokens) or "#FFFFFF"

        slide_font_sizes = set()
        slide_accent_tokens = set()
        for e in elems:
            stype = (e.get("semantic_type") or "").lower()
            content = e.get("content")
            if stype not in ("headline", "text", "caption", "quote"):
                continue
            if not isinstance(content, str) or not content.strip():
                continue
            b = get_bbox(e)
            if not b:
                continue

            st = e.get("style_tokens") if isinstance(e.get("style_tokens"), dict) else {}
            size_pt = resolve_font_size_pt(st, size_tokens, theme_sizes)
            explicit_lh = st.get("line_height", st.get("lineHeight"))
            lh = explicit_lh
            if not isinstance(lh, (int, float)):
                lh = 1.05 if stype == "headline" else 1.2
            lh = float(lh)
            bold = is_bold(st)
            font_family = st.get("font") if isinstance(st.get("font"), str) else None
            measurement = measure_text_height(
                content,
                b["w"],
                size_pt,
                line_height=lh,
                font_family=font_family,
                bold=bold,
            )
            tier = str(measurement.get("tier") or "A_HEURISTIC")
            measurement_tiers[tier] += 1
            est_h_pt = float(measurement.get("height_pt") or 0.0)
            box_h_pt = b["h"] * 72.0

            if est_h_pt > box_h_pt * 1.20:
                _append_finding(
                    hard,
                    "T1_TEXT_OVERFLOW_EST",
                    f"estimated {est_h_pt:.0f}pt > box {box_h_pt:.0f}pt (tier={tier})",
                    "Shorten copy, increase bbox height, or switch archetype/density.",
                    str(e.get("id") or stype),
                )
            elif est_h_pt > box_h_pt * 1.05:
                _append_finding(
                    warn,
                    "T2_TEXT_TIGHT_EST",
                    f"estimated {est_h_pt:.0f}pt vs box {box_h_pt:.0f}pt (tier={tier})",
                    "Slightly shorten copy or give the text more space.",
                    str(e.get("id") or stype),
                )

            role = str(e.get("role") or "").lower()
            if size_pt < 14 and role not in ("citation", "footnote"):
                _append_finding(
                    hard,
                    "A3_FONT_TOO_SMALL",
                    f"font size {size_pt:.1f}pt (< 14pt)",
                    "Use 14pt+ for readability (except citations/footnotes).",
                    str(e.get("id") or stype),
                )

            align = str(st.get("align") or "").lower()
            if stype in ("text", "caption") and align == "center" and len(re.findall(r"\w+", content)) >= 8:
                _append_finding(
                    warn,
                    "TY1_CENTER_BODY_TEXT",
                    "body/caption block is center-aligned",
                    "Use left alignment for longer body text.",
                    str(e.get("id") or stype),
                )

            if stype in ("text", "caption", "quote") and isinstance(explicit_lh, (int, float)) and lh < 1.1:
                _append_finding(
                    warn,
                    "TY2_LOW_LINE_SPACING",
                    f"line_height={lh:.2f}",
                    "Increase line height to >= 1.1 for readability.",
                    str(e.get("id") or stype),
                )

            est_chars_per_line = (b["w"] * 72.0) / max(1.0, size_pt * 0.52)
            if est_chars_per_line > 70 and len(re.sub(r"\s+", " ", content.strip())) > 70:
                _append_finding(
                    warn,
                    "TY4_LONG_LINE_EST",
                    f"estimated line length capacity {est_chars_per_line:.0f} chars (>70)",
                    "Narrow the text box or increase text size to shorten line length.",
                    str(e.get("id") or stype),
                )

            slide_font_sizes.add(round(size_pt, 1))
            color_ref = _token_ref_name(st.get("color"))
            fill_ref = _token_ref_name(st.get("fill"))
            if color_ref and color_ref not in neutral_color_tokens:
                slide_accent_tokens.add(color_ref)
            if fill_ref and fill_ref not in neutral_color_tokens:
                slide_accent_tokens.add(fill_ref)

            fg = resolve_color(st.get("color"), color_tokens) if isinstance(st, dict) else None
            fg = fg or resolve_color("fg", color_tokens) or "#111111"

            bg_solid = None
            bg_grad = None
            containing = []
            for bb, solid, grad in backgrounds:
                if bbox_contains(bb, b, pad=0.08):
                    containing.append((bbox_area(bb), solid, grad))
            containing.sort(key=lambda t: t[0])
            if containing:
                _, bg_solid, bg_grad = containing[0]
            else:
                bg_solid = slide_bg

            large = (size_pt >= 24.0) or (bold and size_pt >= 18.0)
            thresh = 3.0 if large else 4.5
            ratio = min_contrast_against_gradient(fg, bg_grad) if bg_grad is not None else contrast_ratio(fg, bg_solid) if bg_solid else None
            if ratio is not None and ratio < thresh:
                _append_finding(
                    hard,
                    "C1_CONTRAST_LOW",
                    f"contrast {ratio:.2f}:1 (< {thresh}:1)",
                    "Use fg/muted appropriately; adjust fill or choose a different theme/palette.",
                    str(e.get("id") or stype),
                )

        if len(slide_font_sizes) > 3:
            _append_finding(
                warn,
                "TY3_TOO_MANY_FONT_SIZES",
                f"{len(slide_font_sizes)} sizes: {sorted(slide_font_sizes)}",
                "Use up to three font sizes per slide.",
            )

        if len(slide_accent_tokens) > 1:
            _append_finding(
                warn,
                "C2_MULTI_ACCENT",
                f"accent tokens used: {sorted(slide_accent_tokens)}",
                "Keep one dominant accent color per slide.",
            )

        headline_text = slide.get("headline")
        if isinstance(headline_text, str):
            headline_words = len(re.findall(r"\w+", headline_text))
            if headline_words > 12:
                _append_finding(
                    warn,
                    "A4_HEADLINE_TOO_LONG",
                    f"{headline_words} words in headline",
                    "Trim headline to 12 words or fewer.",
                    sid,
                )

        for e in elems:
            st = e.get("style_tokens") if isinstance(e.get("style_tokens"), dict) else {}
            fill = st.get("fill")
            if isinstance(fill, dict) and fill.get("type") in ("linear", "radial"):
                stops = fill.get("stops")
                if not isinstance(stops, list) or len(stops) < 2:
                    _append_finding(
                        hard,
                        "G2_GRADIENT_INVALID",
                        "gradient must have >=2 stops",
                        "Provide at least two stops with pos and color.",
                        str(e.get("id") or e.get("semantic_type") or ""),
                    )
                else:
                    for stop in stops:
                        if not isinstance(stop, dict) or "pos" not in stop or "color" not in stop:
                            _append_finding(
                                hard,
                                "G2_GRADIENT_INVALID",
                                "stop missing pos/color",
                                "Stops must be objects {pos,color[,alpha]}.",
                                str(e.get("id") or e.get("semantic_type") or ""),
                            )
                            break
            if (e.get("semantic_type") or "").lower() == "icon":
                icon_ref = e.get("iconRef")
                if not isinstance(icon_ref, dict) or not icon_ref.get("set") or not icon_ref.get("name"):
                    _append_finding(
                        hard,
                        "I1_ICON_REF_MISSING",
                        "iconRef.set and iconRef.name required",
                        "Provide iconRef {set,name}.",
                        str(e.get("id") or "icon"),
                    )

        anim = slide.get("animations")
        if isinstance(anim, dict):
            steps = anim.get("steps")
            if steps is not None and not isinstance(steps, list):
                _append_finding(hard, "M1_ANIM_INVALID", "animations.steps must be a list", "Fix slide.animations schema.")
            elif isinstance(steps, list):
                for step in steps:
                    if not isinstance(step, dict):
                        _append_finding(hard, "M1_ANIM_INVALID", "animation step must be object", "Fix slide.animations.steps entries.")
                        break
                    if not step.get("targets"):
                        _append_finding(hard, "M1_ANIM_INVALID", "animation step missing targets", "Provide at least one target.")
                        break

        dominant_image_present = any(r >= 0.35 for r in dominant_image_ratios)
        density_sequence.append((sid, _density_class(slide_words, whitespace_ratio, dominant_image_present)))
        slide_rep = {
            "slide_id": sid,
            "section": slide.get("section"),
            "parent_slide": slide.get("parent_slide"),
            "archetype": slide.get("archetype"),
            "metrics": {
                "words": slide_words,
                "bullets": slide_bullets,
                "elements": elem_count,
                "whitespace_ratio": round(whitespace_ratio, 3),
                "max_image_area_ratio": round(max_image_ratio, 3),
            },
            "hard_fail": hard,
            "warnings": warn,
        }
        report["slides"].append(slide_rep)

    if len(headline_positions) >= 3:
        xs = [x for _, x, _ in headline_positions]
        ys = [y for _, _, y in headline_positions]
        if (max(xs) - min(xs)) > 0.12:
            _append_finding(
                report["deck_warnings"],
                "D4_HEADLINE_X_DRIFT",
                f"headline x range {min(xs):.2f}–{max(xs):.2f} in",
                "Align headlines to the same left margin across slides.",
            )
        if (max(ys) - min(ys)) > 0.12:
            _append_finding(
                report["deck_warnings"],
                "D5_HEADLINE_Y_DRIFT",
                f"headline y range {min(ys):.2f}–{max(ys):.2f} in",
                "Align headlines to the same top offset across slides.",
            )

    if len(font_families) > 2:
        _append_finding(
            report["deck_hard_fail"],
            "A5_TOO_MANY_FONTS",
            f"{len(font_families)} fonts: {sorted(font_families)}",
            "Use at most two font families (headline + body) per deck.",
        )

    if len(card_radii) > 2:
        _append_finding(
            report["deck_warnings"],
            "D7_INCONSISTENT_RADII",
            f"card radii variants: {sorted(card_radii)}",
            "Standardize card radius via theme tokens.",
        )

    if narrative_sections:
        used_sections = set(section_counts.keys())
        missing_sections = sorted(narrative_sections - used_sections)
        extra_sections = sorted(used_sections - narrative_sections)
        if missing_sections:
            _append_finding(
                report["deck_warnings"],
                "D15_NARRATIVE_SECTION_MISSING",
                f"narrative arc sections without slides: {missing_sections}",
                "Assign slide.section values to cover all narrative_arc sections.",
            )
        if extra_sections:
            _append_finding(
                report["deck_warnings"],
                "D16_SECTION_NOT_IN_NARRATIVE_ARC",
                f"slide sections not in narrative_arc: {extra_sections}",
                "Align slide.section tags with deck.narrative_arc.",
            )

    run_start = 0
    while run_start < len(archetype_sequence):
        sid0, arche0 = archetype_sequence[run_start]
        run_end = run_start + 1
        while run_end < len(archetype_sequence) and archetype_sequence[run_end][1] == arche0:
            run_end += 1
        run_len = run_end - run_start
        if arche0 and run_len > 2:
            span = [sid for sid, _ in archetype_sequence[run_start:run_end]]
            _append_finding(
                report["deck_warnings"],
                "D17_ARCHETYPE_REPEAT_RUN",
                f"archetype '{arche0}' repeated {run_len}x across {span}",
                "Limit identical archetype runs to at most 2 slides.",
            )
        run_start = run_end

    if len(archetype_sequence) >= 6:
        arche_counts = Counter(a for _, a in archetype_sequence if a)
        if arche_counts:
            top_arche, top_count = arche_counts.most_common(1)[0]
            if top_count / len(archetype_sequence) > 0.5:
                _append_finding(
                    report["deck_warnings"],
                    "D18_ARCHETYPE_DISTRIBUTION_SKEW",
                    f"'{top_arche}' appears on {top_count}/{len(archetype_sequence)} slides",
                    "Increase archetype variety across the deck.",
                )

    if len(density_sequence) >= 4:
        density_only = [d for _, d in density_sequence]
        density_counts = Counter(density_only)
        if density_counts:
            common_density, common_count = density_counts.most_common(1)[0]
            if common_count == len(density_only):
                _append_finding(
                    report["deck_warnings"],
                    "D19_DENSITY_DISTRIBUTION_FLAT",
                    f"all slides classified as '{common_density}'",
                    "Mix light/medium/heavy slide densities to improve deck rhythm.",
                )
        heavy_run = 0
        for _, density in density_sequence:
            heavy_run = heavy_run + 1 if density == "heavy" else 0
            if heavy_run >= 4:
                _append_finding(
                    report["deck_warnings"],
                    "D20_HEAVY_DENSITY_RUN",
                    "4+ heavy slides in a row",
                    "Insert lighter/breather slides to reset visual rhythm.",
                )
                break

    report["summary"]["deck_hard_fail"] = len(report["deck_hard_fail"])
    report["summary"]["deck_warnings"] = len(report["deck_warnings"])
    report["summary"]["hard_fail"] = len(report["deck_hard_fail"]) + sum(len(s["hard_fail"]) for s in report["slides"])
    report["summary"]["warnings"] = sum(len(s["warnings"]) for s in report["slides"])
    report["summary"]["text_measure_tiers"] = dict(measurement_tiers)
    return report


def to_markdown(report: Dict[str, Any]) -> str:
    s = report["summary"]
    verdict = "PASS" if s["hard_fail"] == 0 else "FAIL"
    lines: List[str] = []
    lines.append(f"# QA report — {verdict}")
    lines.append("")
    lines.append(f"Slides: {s['slides']}  ")
    lines.append(f"Hard fails: {s['hard_fail']}  ")
    lines.append(f"Deck hard fails: {s.get('deck_hard_fail', 0)}  ")
    lines.append(f"Warnings: {s['warnings']}  ")
    lines.append(f"Deck warnings: {s.get('deck_warnings', 0)}  ")
    lines.append(f"Schema engine: {s.get('schema_engine', 'unknown')}  ")
    if s.get("text_measure_tiers"):
        lines.append(f"Text measure tiers: {s.get('text_measure_tiers')}")
    lines.append("")

    if report.get("deck_hard_fail"):
        lines.append("## Deck hard fails")
        for w in report["deck_hard_fail"]:
            lines.append(f"- **{w['code']}**: {w.get('evidence','')}")
            if w.get("fix"):
                lines.append(f"  - Fix: {w['fix']}")
        lines.append("")

    if report.get("deck_warnings"):
        lines.append("## Deck warnings")
        for w in report["deck_warnings"]:
            lines.append(f"- {w['code']}: {w.get('evidence','')}")
            if w.get("fix"):
                lines.append(f"  - Fix: {w['fix']}")
        lines.append("")

    for slide in report["slides"]:
        sid = slide["slide_id"]
        lines.append(f"## {sid} — {slide.get('archetype')}")
        m = slide["metrics"]
        lines.append(f"- Elements: {m.get('elements')} | Words: {m.get('words')} | Bullets: {m.get('bullets')} | Whitespace: {m.get('whitespace_ratio')}")
        if slide["hard_fail"]:
            lines.append("### Hard fails")
            for v in slide["hard_fail"]:
                tgt = v.get("target", "")
                lines.append(f"- **{v['code']}** {('(' + tgt + ')') if tgt else ''}: {v.get('evidence','')}")
                if v.get("fix"):
                    lines.append(f"  - Fix: {v['fix']}")
        if slide["warnings"]:
            lines.append("### Warnings")
            for v in slide["warnings"]:
                tgt = v.get("target", "")
                lines.append(f"- {v['code']} {('(' + tgt + ')') if tgt else ''}: {v.get('evidence','')}")
                if v.get("fix"):
                    lines.append(f"  - Fix: {v['fix']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ir", type=Path, help="Path to deck.ir.json")
    ap.add_argument("--out", type=Path, default=None, help="Write JSON report to this path")
    ap.add_argument("--md", type=Path, default=None, help="Write Markdown report to this path")
    ap.add_argument("--themes", type=Path, default=None, help="Path to assets/themes.json (optional)")
    ap.add_argument("--palettes", type=Path, default=None, help="Path to assets/palettes.json (optional)")
    args = ap.parse_args()

    themes_path = args.themes or (repo_root() / "assets" / "themes.json")
    palettes_path = args.palettes or (repo_root() / "assets" / "palettes.json")

    ir = load_ir(args.ir)
    report = preflight(ir, themes_path=themes_path, palettes_path=palettes_path)

    if args.out:
        args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if args.md:
        args.md.write_text(to_markdown(report), encoding="utf-8")

    summary = report["summary"]
    print(
        f"Slides={summary['slides']} hard_fail={summary['hard_fail']} "
        f"deck_hard_fail={summary.get('deck_hard_fail',0)} warnings={summary['warnings']} "
        f"deck_warnings={summary.get('deck_warnings',0)}"
    )
    return 0 if summary["hard_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
