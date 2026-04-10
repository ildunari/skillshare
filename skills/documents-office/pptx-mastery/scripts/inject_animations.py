#!/usr/bin/env python3

"""
inject_animations.py

Post-processes a rendered PPTX to inject PowerPoint (OOXML) build animations into slide XML.

Why a post-pass?
- PptxGenJS (and most PPT generators) do not expose a stable, high-level animation API.
- OOXML animations live under <p:timing> in each slide XML part.

This script:
1) Unpacks the PPTX using the skill's ooxml/scripts/unpack.py
2) Locates slideN.xml parts and identifies shapes (spid/name/bbox/text)
3) Writes/merges <p:timing> for specified slides
4) Repacks + validates via ooxml/scripts/pack.py (LibreOffice roundtrip)

Supported entrance effects:
- appear  (implemented as 1ms fade-in so the shape starts hidden)
- fade
- wipe (left/right/up/down)
- zoom  (fade-in + animScale 0%->100%)

Usage:
  python scripts/inject_animations.py in.pptx --spec animations.json --out out.pptx
  python scripts/inject_animations.py in.pptx --ir deck.ir.json --out out.pptx

Notes:
- For reliable targeting, the renderer should stamp stable shape names
  (recommended: name="el:{slide_id}:{element_id}"). This is part of Phase 3.
- Fallback matching by bbox/text is best-effort and may be ambiguous.

"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from lxml import etree


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
EMU_PER_IN = 914400.0


# -------------------------
# Data model
# -------------------------

@dataclass(frozen=True)
class BBox:
    x: float
    y: float
    w: float
    h: float

    def contains(self, other: "BBox", pad: float = 0.0) -> bool:
        return (
            (self.x - pad) <= other.x
            and (self.y - pad) <= other.y
            and (self.x + self.w + pad) >= (other.x + other.w)
            and (self.y + self.h + pad) >= (other.y + other.h)
        )

    def l1_distance(self, other: "BBox") -> float:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.w - other.w) + abs(self.h - other.h)


@dataclass
class ShapeRef:
    spid: int
    name: str
    bbox: Optional[BBox]
    text: str
    kind: str  # sp/pic/graphicFrame


@dataclass
class TargetSelector:
    spid: Optional[int] = None
    name: Optional[str] = None
    name_regex: Optional[str] = None
    bbox: Optional[BBox] = None
    text_contains: Optional[str] = None

    @staticmethod
    def from_obj(obj: Any) -> "TargetSelector":
        # Allow shorthand strings:
        # - "spid:7"
        # - "name:el:S03:card:0"
        if isinstance(obj, str):
            if obj.startswith("spid:"):
                return TargetSelector(spid=int(obj.split(":", 1)[1]))
            if obj.startswith("name:"):
                return TargetSelector(name=obj.split(":", 1)[1])
            return TargetSelector(name=obj)  # default: treat as name
        if isinstance(obj, int):
            return TargetSelector(spid=obj)
        if not isinstance(obj, dict):
            raise ValueError(f"Invalid target selector: {obj!r}")

        bbox_obj = obj.get("bbox")
        bbox = None
        if isinstance(bbox_obj, dict):
            bbox = BBox(float(bbox_obj["x"]), float(bbox_obj["y"]), float(bbox_obj["w"]), float(bbox_obj["h"]))
        return TargetSelector(
            spid=obj.get("spid"),
            name=obj.get("name"),
            name_regex=obj.get("name_regex"),
            bbox=bbox,
            text_contains=obj.get("text_contains"),
        )


@dataclass
class AnimStep:
    targets: List[TargetSelector]
    effect: str  # appear|fade|wipe|zoom
    direction: Optional[str] = None  # for wipe: left|right|up|down
    duration_ms: int = 320
    stagger_ms: int = 0


@dataclass
class SlideAnimSpec:
    slide_number: int  # 1-based slideN.xml
    steps: List[AnimStep]


# -------------------------
# Helpers: filesystem + subprocess
# -------------------------

def _repo_root() -> Path:
    # scripts/ is in the repo root for this skill
    return Path(__file__).resolve().parents[1]


def _run(cmd: Sequence[str], cwd: Optional[Path] = None) -> None:
    proc = subprocess.run(list(cmd), cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            f"  {' '.join(cmd)}\n\n"
            f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
        )


def unpack_pptx(pptx_path: Path, out_dir: Path) -> None:
    root = _repo_root()
    script = root / "ooxml" / "scripts" / "unpack.py"
    _run([sys.executable, str(script), str(pptx_path), str(out_dir)])


def pack_pptx(unpacked_dir: Path, out_pptx: Path, validate: bool = True) -> None:
    root = _repo_root()
    script = root / "ooxml" / "scripts" / "pack.py"
    cmd = [sys.executable, str(script), str(unpacked_dir), str(out_pptx)]
    if not validate:
        cmd.append("--force")
    _run(cmd)


# -------------------------
# Helpers: PPTX parsing
# -------------------------

def emu_to_in(v: int) -> float:
    return float(v) / EMU_PER_IN


def extract_shape_bbox(node: etree._Element) -> Optional[BBox]:
    xfrm = node.find(".//a:xfrm", namespaces=NS)
    if xfrm is None:
        return None
    off = xfrm.find("a:off", namespaces=NS)
    ext = xfrm.find("a:ext", namespaces=NS)
    if off is None or ext is None:
        return None
    try:
        x = emu_to_in(int(off.get("x")))
        y = emu_to_in(int(off.get("y")))
        w = emu_to_in(int(ext.get("cx")))
        h = emu_to_in(int(ext.get("cy")))
        return BBox(x, y, w, h)
    except Exception:
        return None


def extract_shape_text(node: etree._Element) -> str:
    texts = node.findall(".//a:t", namespaces=NS)
    t = "".join([tx.text or "" for tx in texts]).strip()
    # normalize whitespace
    return re.sub(r"\s+", " ", t)


def list_shapes(slide_root: etree._Element) -> List[ShapeRef]:
    out: List[ShapeRef] = []
    for kind_tag in ("p:sp", "p:pic", "p:graphicFrame"):
        for node in slide_root.findall(f".//{kind_tag}", namespaces=NS):
            cNvPr = node.find(".//p:cNvPr", namespaces=NS)
            if cNvPr is None:
                continue
            spid_s = cNvPr.get("id")
            if not spid_s:
                continue
            try:
                spid = int(spid_s)
            except ValueError:
                continue
            name = cNvPr.get("name") or ""
            bbox = extract_shape_bbox(node)
            text = extract_shape_text(node)
            out.append(ShapeRef(spid=spid, name=name, bbox=bbox, text=text, kind=kind_tag.split(":")[1]))
    return out


# -------------------------
# Target resolution
# -------------------------

def resolve_target(sel: TargetSelector, shapes: List[ShapeRef], bbox_tol_in: float = 0.12) -> int:
    # 1) spid exact
    if sel.spid is not None:
        for s in shapes:
            if s.spid == sel.spid:
                return s.spid
        raise ValueError(f"Target spid={sel.spid} not found on slide")

    # 2) name exact
    if sel.name is not None:
        matches = [s for s in shapes if s.name == sel.name]
        if len(matches) == 1:
            return matches[0].spid
        if len(matches) > 1:
            raise ValueError(f"Ambiguous name selector {sel.name!r} matched {len(matches)} shapes")
        # allow substring match as fallback
        matches = [s for s in shapes if sel.name in s.name]
        if len(matches) == 1:
            return matches[0].spid

    # 3) name regex
    if sel.name_regex is not None:
        rgx = re.compile(sel.name_regex)
        matches = [s for s in shapes if rgx.search(s.name)]
        if len(matches) == 1:
            return matches[0].spid
        if len(matches) > 1:
            raise ValueError(f"Ambiguous name_regex {sel.name_regex!r} matched {len(matches)} shapes")

    # 4) bbox + (optional) text_contains
    if sel.bbox is not None:
        candidates: List[Tuple[float, ShapeRef]] = []
        for s in shapes:
            if s.bbox is None:
                continue
            if sel.text_contains and sel.text_contains.lower() not in (s.text or "").lower():
                continue
            dist = s.bbox.l1_distance(sel.bbox)
            candidates.append((dist, s))
        candidates.sort(key=lambda x: x[0])
        if not candidates:
            raise ValueError(f"No bbox candidates found for selector bbox={sel.bbox}")

        best_dist, best = candidates[0]
        # accept if close enough
        if best_dist <= bbox_tol_in * 4:  # L1 over 4 dims
            # ensure not a tie
            ties = [c for c in candidates if abs(c[0] - best_dist) < 1e-6]
            if len(ties) > 1:
                raise ValueError(f"Ambiguous bbox selector: {len(ties)} shapes tied at distance {best_dist:.3f} in")
            return best.spid

        raise ValueError(
            f"No close bbox match (best distance {best_dist:.3f} in) for selector bbox={sel.bbox}. "
            "Consider adding text_contains or using spid/name selectors."
        )

    raise ValueError(f"Could not resolve target selector: {sel}")


# -------------------------
# OOXML construction
# -------------------------

def qn(prefix: str, tag: str) -> str:
    return f"{{{NS[prefix]}}}{tag}"


def _new_id_generator(start: int = 1):
    i = start
    while True:
        yield i
        i += 1


def _find_max_tn_id(slide_root: etree._Element) -> int:
    # find max id attribute among p:cTn in existing timing, if any
    max_id = 0
    for ctn in slide_root.findall(".//p:cTn", namespaces=NS):
        sid = ctn.get("id")
        if not sid:
            continue
        try:
            max_id = max(max_id, int(sid))
        except ValueError:
            continue
    return max_id


def _anim_effect_filter(effect: str, direction: Optional[str]) -> Tuple[str, Dict[str, str]]:
    """
    Returns (tag, attributes) for the behavior element under p:childTnLst.
    """
    if effect in ("fade", "appear"):
        return "animEffect", {"transition": "in", "filter": "fade"}
    if effect == "wipe":
        d = (direction or "right").lower()
        if d not in ("left", "right", "up", "down"):
            raise ValueError(f"Invalid wipe direction: {direction!r}")
        return "animEffect", {"transition": "in", "filter": f"wipe({d})"}
    if effect == "zoom":
        # handled separately (fade + animScale)
        return "animScale", {}
    raise ValueError(f"Unsupported effect: {effect!r}")


def _add_common_behavior(parent: etree._Element, id_gen, spid: int, dur_ms: int, delay_ms: int) -> etree._Element:
    """
    Adds <p:cBhvr> with <p:cTn>, <p:tgtEl>.
    Returns the created <p:cBhvr>.
    """
    cbhvr = etree.SubElement(parent, qn("p", "cBhvr"))
    ctn = etree.SubElement(
        cbhvr,
        qn("p", "cTn"),
        id=str(next(id_gen)),
        dur=str(max(1, int(dur_ms))),
        fill="hold",
    )
    st = etree.SubElement(ctn, qn("p", "stCondLst"))
    etree.SubElement(st, qn("p", "cond"), delay=str(max(0, int(delay_ms))))
    tgt = etree.SubElement(cbhvr, qn("p", "tgtEl"))
    etree.SubElement(tgt, qn("p", "spTgt"), spid=str(int(spid)))
    return cbhvr


def _add_fade_or_wipe(child_tn_lst: etree._Element, id_gen, spid: int, dur_ms: int, delay_ms: int, effect: str, direction: Optional[str]) -> None:
    tag, attrs = _anim_effect_filter(effect, direction)
    anim = etree.SubElement(child_tn_lst, qn("p", tag), **attrs)
    _add_common_behavior(anim, id_gen, spid=spid, dur_ms=dur_ms, delay_ms=delay_ms)


def _add_zoom(child_tn_lst: etree._Element, id_gen, spid: int, dur_ms: int, delay_ms: int) -> None:
    """
    Zoom entrance implemented as:
      - 1ms fade-in (ensures hidden-at-start semantics)
      - animScale from 0% -> 100%

    NOTE: PowerPoint can be strict about animScale; we include attrNameLst with two placeholders.
    """
    # 1) 1ms fade-in
    anim_fade = etree.SubElement(child_tn_lst, qn("p", "animEffect"), transition="in", filter="fade")
    _add_common_behavior(anim_fade, id_gen, spid=spid, dur_ms=1, delay_ms=delay_ms)

    # 2) animScale
    anim_scale = etree.SubElement(child_tn_lst, qn("p", "animScale"))
    cbhvr = _add_common_behavior(anim_scale, id_gen, spid=spid, dur_ms=dur_ms, delay_ms=delay_ms)

    # PowerPoint requires at least two attrName entries for animScale in some cases (MS-OE376 note).
    attr_lst = etree.SubElement(cbhvr, qn("p", "attrNameLst"))
    etree.SubElement(attr_lst, qn("p", "attrName")).text = "ppt_x"
    etree.SubElement(attr_lst, qn("p", "attrName")).text = "ppt_y"

    # from 0% -> to 100000 (100%)
    frm = etree.SubElement(anim_scale, qn("p", "from"))
    xfrm = etree.SubElement(frm, qn("p", "xfrm"))
    etree.SubElement(xfrm, qn("p", "off"), x="0", y="0")
    etree.SubElement(xfrm, qn("p", "ext"), cx="0", cy="0")

    to = etree.SubElement(anim_scale, qn("p", "to"))
    xfrm2 = etree.SubElement(to, qn("p", "xfrm"))
    etree.SubElement(xfrm2, qn("p", "off"), x="0", y="0")
    etree.SubElement(xfrm2, qn("p", "ext"), cx="100000", cy="100000")


def build_timing(slide_root: etree._Element, steps: List[AnimStep], replace_existing: bool = False) -> etree._Element:
    """
    Returns a <p:timing> element for the slide (or merges into existing).
    """
    existing = slide_root.find("p:timing", namespaces=NS)
    if existing is not None and not replace_existing:
        # Merge: append a new <p:seq> under the tmRoot <p:cTn>.
        # If we can't locate a tmRoot, fall back to replacing.
        try:
            tnLst = existing.find("p:tnLst", namespaces=NS)
            if tnLst is None:
                raise ValueError("missing tnLst")
            par = tnLst.find("p:par", namespaces=NS)
            if par is None:
                raise ValueError("missing par")
            cTn_root = par.find("p:cTn", namespaces=NS)
            if cTn_root is None:
                raise ValueError("missing cTn root")
            childTnLst = cTn_root.find("p:childTnLst", namespaces=NS)
            if childTnLst is None:
                childTnLst = etree.SubElement(cTn_root, qn("p", "childTnLst"))
            # We'll append a new seq that is click-advanced.
            start_id = _find_max_tn_id(slide_root) + 1
            id_gen = _new_id_generator(start_id)
            seq = _build_seq(id_gen, steps)
            childTnLst.append(seq)
            return existing
        except Exception:
            replace_existing = True

    # Replace (or create) full timing
    start_id = _find_max_tn_id(slide_root) + 1 if existing is not None else 1
    id_gen = _new_id_generator(start_id)

    timing = etree.Element(qn("p", "timing"))
    tnLst = etree.SubElement(timing, qn("p", "tnLst"))
    par = etree.SubElement(tnLst, qn("p", "par"))
    cTn_root = etree.SubElement(
        par,
        qn("p", "cTn"),
        id=str(next(id_gen)),
        dur="indefinite",
        restart="never",
        nodeType="tmRoot",
    )
    childTnLst = etree.SubElement(cTn_root, qn("p", "childTnLst"))
    seq = _build_seq(id_gen, steps)
    childTnLst.append(seq)
    return timing


def _build_seq(id_gen, steps: List[AnimStep]) -> etree._Element:
    """
    Build a click-advanced main sequence with one <p:par> per step.
    """
    seq = etree.Element(qn("p", "seq"), concurrent="1", nextAc="seek")
    cTn_main = etree.SubElement(
        seq,
        qn("p", "cTn"),
        id=str(next(id_gen)),
        dur="indefinite",
        restart="whenNotActive",
        fill="hold",
        nodeType="mainSeq",
    )
    st = etree.SubElement(cTn_main, qn("p", "stCondLst"))
    etree.SubElement(st, qn("p", "cond"), evt="onBegin", delay="0")
    child = etree.SubElement(cTn_main, qn("p", "childTnLst"))

    for step in steps:
        par_step = etree.SubElement(child, qn("p", "par"))
        cTn_step = etree.SubElement(
            par_step,
            qn("p", "cTn"),
            id=str(next(id_gen)),
            dur=str(max(1, int(step.duration_ms))),
            fill="hold",
        )
        st2 = etree.SubElement(cTn_step, qn("p", "stCondLst"))
        etree.SubElement(st2, qn("p", "cond"), delay="0")
        child2 = etree.SubElement(cTn_step, qn("p", "childTnLst"))

        # Each target animates inside the step, optionally staggered
        for idx, tgt in enumerate(step.targets):
            delay = idx * int(step.stagger_ms or 0)
            # appear implemented as 1ms fade
            eff = step.effect.lower()
            if eff == "zoom":
                _add_zoom(child2, id_gen, spid=tgt.spid, dur_ms=step.duration_ms, delay_ms=delay)
            else:
                _add_fade_or_wipe(child2, id_gen, spid=tgt.spid, dur_ms=(1 if eff=="appear" else step.duration_ms), delay_ms=delay, effect=eff, direction=step.direction)

    # Click advances to the next child in the sequence
    next_cond = etree.SubElement(seq, qn("p", "nextCondLst"))
    etree.SubElement(next_cond, qn("p", "cond"), evt="onClick", delay="0")
    return seq


# -------------------------
# Spec loading
# -------------------------

def load_spec_from_json(path: Path) -> List[SlideAnimSpec]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    slides_obj = obj.get("slides") if isinstance(obj, dict) else None
    if slides_obj is None:
        raise ValueError("Animation spec JSON must be an object with a 'slides' list")

    out: List[SlideAnimSpec] = []
    for s in slides_obj:
        if not isinstance(s, dict):
            raise ValueError("Each slide spec must be an object")
        slide_number = int(s["slide_number"])
        defaults = s.get("defaults", {})
        def_eff = defaults.get("effect", "fade")
        def_dur = int(defaults.get("duration_ms", 320))
        def_stagger = int(defaults.get("stagger_ms", 0))
        steps: List[AnimStep] = []
        for step_obj in s.get("steps", []):
            effect = (step_obj.get("effect") or def_eff)
            duration_ms = int(step_obj.get("duration_ms") or def_dur)
            stagger_ms = int(step_obj.get("stagger_ms") or def_stagger)
            direction = step_obj.get("direction")
            targets = [TargetSelector.from_obj(t) for t in step_obj.get("targets", [])]
            steps.append(AnimStep(targets=targets, effect=effect, direction=direction, duration_ms=duration_ms, stagger_ms=stagger_ms))
        out.append(SlideAnimSpec(slide_number=slide_number, steps=steps))
    return out


def load_spec_from_ir(path: Path, auto: bool = False) -> List[SlideAnimSpec]:
    """
    Reads pptx-master IR and returns SlideAnimSpec objects.

    Expected IR additions (Phase 2 schema):
      slide.animations: optional object with 'preset' or explicit 'steps'

    If auto=True, slides without explicit animations may receive a generic reading-order build.
    """
    ir = json.loads(path.read_text(encoding="utf-8"))
    deck = ir.get("deck") or {}
    slides = deck.get("slides") or []
    out: List[SlideAnimSpec] = []

    for idx, s in enumerate(slides):
        slide_number = idx + 1
        anim = s.get("animations")
        if anim is None and not auto:
            continue

        # Build steps
        steps: List[Dict[str, Any]] = []
        defaults = {"effect": "fade", "duration_ms": 320, "stagger_ms": 0}
        archetype = s.get("archetype")

        if isinstance(anim, dict):
            defaults.update(anim.get("defaults") or {})
            preset = (anim.get("preset") or "").lower()
            if preset == "auto":
                steps = auto_steps_from_slide(s, archetype=archetype, defaults=defaults)
            else:
                steps = anim.get("steps") or []
        else:
            steps = auto_steps_from_slide(s, archetype=archetype, defaults=defaults)

        # If still no steps (e.g., empty), skip
        if not steps:
            continue

        anim_steps: List[AnimStep] = []
        for st in steps:
            effect = (st.get("effect") or defaults["effect"])
            duration_ms = int(st.get("duration_ms") or defaults["duration_ms"])
            stagger_ms = int(st.get("stagger_ms") or defaults.get("stagger_ms", 0))
            direction = st.get("direction")
            targets = [TargetSelector.from_obj(t) for t in st.get("targets", [])]
            anim_steps.append(AnimStep(targets=targets, effect=effect, direction=direction, duration_ms=duration_ms, stagger_ms=stagger_ms))

        out.append(SlideAnimSpec(slide_number=slide_number, steps=anim_steps))

    return out


def auto_steps_from_slide(slide_obj: Dict[str, Any], archetype: Optional[str], defaults: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Best-effort smart defaults based on archetype + element ordering.
    This is intentionally conservative: prefer a small number of meaningful builds.

    Strategy:
      - exclude headline/footer-like elements by semantic_type
      - sort remaining elements by reading order (y, then x)
      - one build per element (or per clustered group for known archetypes)

    Targets are expressed as bbox selectors so they can be resolved post-render.
    """
    elems = slide_obj.get("elements") or []
    if not elems:
        return []

    def is_animatable(e: Dict[str, Any]) -> bool:
        st = (e.get("semantic_type") or "").lower()
        return st not in ("headline", "title", "footer", "background", "bg", "logo")

    anim_elems = [e for e in elems if is_animatable(e) and isinstance(e.get("bbox"), dict)]
    if not anim_elems:
        return []

    # reading order
    anim_elems.sort(key=lambda e: (e["bbox"]["y"], e["bbox"]["x"]))

    # archetype-tuned effect defaults
    eff = defaults.get("effect", "fade")
    direction = None
    if archetype:
        a = archetype.upper()
        if a in ("A12", "A14"):
            eff = "wipe"
            direction = "right"

    steps: List[Dict[str, Any]] = []
    for e in anim_elems:
        steps.append({
            "effect": eff,
            "direction": direction,
            "targets": [{"bbox": e["bbox"], "text_contains": (e.get("text") or "")[:40] or None}],
        })
    return steps


# -------------------------
# Slide XML patching
# -------------------------

def insert_or_replace_timing(slide_root: etree._Element, timing: etree._Element, replace_existing: bool) -> None:
    existing = slide_root.find("p:timing", namespaces=NS)
    if existing is not None:
        if replace_existing:
            slide_root.remove(existing)
            slide_root.append(timing)
        else:
            # build_timing already merged into existing
            return
    else:
        # place timing after clrMapOvr if present
        clr = slide_root.find("p:clrMapOvr", namespaces=NS)
        if clr is not None:
            idx = list(slide_root).index(clr)
            slide_root.insert(idx + 1, timing)
        else:
            slide_root.append(timing)


def apply_animations_to_slide(slide_path: Path, spec: SlideAnimSpec, replace_existing: bool) -> None:
    parser = etree.XMLParser(remove_blank_text=False)
    slide_root = etree.fromstring(slide_path.read_bytes(), parser=parser)

    shapes = list_shapes(slide_root)
    if not shapes:
        raise ValueError(f"No shapes found in {slide_path}")

    # Resolve selectors to spids
    resolved_steps: List[AnimStep] = []
    for step in spec.steps:
        resolved_targets: List[TargetSelector] = []
        for sel in step.targets:
            spid = resolve_target(sel, shapes)
            resolved_targets.append(TargetSelector(spid=spid))
        resolved_steps.append(AnimStep(targets=resolved_targets, effect=step.effect, direction=step.direction, duration_ms=step.duration_ms, stagger_ms=step.stagger_ms))

    timing = build_timing(slide_root, resolved_steps, replace_existing=replace_existing)
    insert_or_replace_timing(slide_root, timing, replace_existing=replace_existing)

    slide_path.write_bytes(etree.tostring(slide_root, xml_declaration=True, encoding="UTF-8", standalone="yes"))


# -------------------------
# CLI
# -------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Inject build animations into a rendered PPTX (OOXML post-pass).")
    ap.add_argument("pptx", type=Path, help="Input PPTX (already rendered)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--spec", type=Path, help="Animation specification JSON file")
    src.add_argument("--ir", type=Path, help="pptx-master IR JSON file (uses slide.animations)")
    ap.add_argument("--out", type=Path, required=True, help="Output PPTX path")
    ap.add_argument("--replace-existing", action="store_true", help="Replace existing <p:timing> instead of merging")
    ap.add_argument("--no-validate", action="store_true", help="Skip LibreOffice validation during repack")
    ap.add_argument("--auto", action="store_true", help="When using --ir, auto-generate animations for slides without explicit slide.animations")
    args = ap.parse_args()

    if not args.pptx.exists():
        raise FileNotFoundError(args.pptx)

    with tempfile.TemporaryDirectory(prefix="pptx_anim_") as tmp:
        tmpdir = Path(tmp)
        unpack_pptx(args.pptx, tmpdir)

        if args.spec:
            slide_specs = load_spec_from_json(args.spec)
        else:
            slide_specs = load_spec_from_ir(args.ir, auto=args.auto)

        # Apply per slide
        for ss in slide_specs:
            slide_path = tmpdir / "ppt" / "slides" / f"slide{ss.slide_number}.xml"
            if not slide_path.exists():
                raise FileNotFoundError(f"Slide part not found: {slide_path}")
            apply_animations_to_slide(slide_path, ss, replace_existing=args.replace_existing)

        pack_pptx(tmpdir, args.out, validate=(not args.no_validate))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
