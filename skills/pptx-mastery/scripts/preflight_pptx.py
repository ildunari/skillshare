#!/usr/bin/env python3
"""
preflight_pptx.py

Post-render QA for pptx-master outputs (PPTX).

Checks:
- slide bounds / safe zone overflow
- minimum font size
- image/asset integrity and effective DPI
- font embedding warnings
- animation validity
- optional integration hooks for asset-planning and vision QA artifacts
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from lxml import etree
from PIL import Image


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
EMU_PER_IN = 914400.0
KNOWN_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".emf", ".wmf", ".svg"}
MAX_IMAGE_BYTES_WARN = 20 * 1024 * 1024


def unzip_pptx(pptx_path: Path, out_dir: Path) -> None:
    with zipfile.ZipFile(pptx_path, "r") as zf:
        zf.extractall(out_dir)


def emu_to_in(v: int) -> float:
    return float(v) / EMU_PER_IN


def normalize_severity(value: Any) -> str:
    raw = str(value or "").strip().upper()
    if raw in {"FAIL", "ERROR", "HARD_FAIL", "BLOCK"}:
        return "FAIL"
    if raw in {"WARN", "WARNING"}:
        return "WARN"
    return "INFO"


def make_finding(code: str, severity: str, evidence: str, fix: Optional[str] = None) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "code": code,
        "severity": normalize_severity(severity),
        "evidence": evidence,
    }
    if fix:
        item["fix"] = fix
    return item


@dataclass
class ShapeInfo:
    spid: int
    name: str
    kind: str
    x: float
    y: float
    w: float
    h: float
    text: str


def extract_bbox(node: etree._Element) -> Optional[Tuple[float, float, float, float]]:
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
        return x, y, w, h
    except Exception:
        return None


def extract_text(node: etree._Element) -> str:
    texts = node.findall(".//a:t", namespaces=NS)
    t = "".join([tx.text or "" for tx in texts]).strip()
    return re.sub(r"\s+", " ", t)


def list_shapes(slide_root: etree._Element) -> List[ShapeInfo]:
    out: List[ShapeInfo] = []
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
            bbox = extract_bbox(node)
            if bbox is None:
                continue
            x, y, w, h = bbox
            out.append(
                ShapeInfo(
                    spid=spid,
                    name=cNvPr.get("name") or "",
                    kind=kind_tag.split(":")[1],
                    x=x,
                    y=y,
                    w=w,
                    h=h,
                    text=extract_text(node),
                )
            )
    return out


def slide_rels_map(rels_path: Path) -> Dict[str, Dict[str, str]]:
    if not rels_path.exists():
        return {}
    root = etree.fromstring(rels_path.read_bytes())
    out: Dict[str, Dict[str, str]] = {}
    for rel in root.findall("rel:Relationship", namespaces=NS):
        rid = rel.get("Id")
        if not rid:
            continue
        out[rid] = {
            "target": rel.get("Target") or "",
            "type": rel.get("Type") or "",
            "target_mode": rel.get("TargetMode") or "",
        }
    return out


def resolve_rel_target(base_dir: Path, target: str) -> Path:
    target_clean = (target or "").split("?", 1)[0].split("#", 1)[0].strip()
    if target_clean.startswith("/"):
        return (base_dir.parents[2] / target_clean.lstrip("/")).resolve()
    return (base_dir / target_clean).resolve()


def safe_rel_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def find_images(slide_root: etree._Element) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for pic in slide_root.findall(".//p:pic", namespaces=NS):
        c_nv_pr = pic.find(".//p:cNvPr", namespaces=NS)
        if c_nv_pr is None or not c_nv_pr.get("id"):
            continue
        try:
            spid = int(c_nv_pr.get("id"))
        except ValueError:
            continue
        blip = pic.find(".//a:blip", namespaces=NS)
        if blip is None:
            continue
        out.append(
            {
                "spid": spid,
                "embed_rid": blip.get(f"{{{NS['r']}}}embed"),
                "link_rid": blip.get(f"{{{NS['r']}}}link"),
            }
        )
    return out


def read_image_size_px(path: Path) -> Optional[Tuple[int, int]]:
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def collect_fonts_in_slide(slide_root: etree._Element) -> List[str]:
    fonts = []
    for latin in slide_root.findall(".//a:rPr/a:latin", namespaces=NS):
        tf = latin.get("typeface")
        if tf:
            fonts.append(tf)
    for latin in slide_root.findall(".//a:defRPr/a:latin", namespaces=NS):
        tf = latin.get("typeface")
        if tf:
            fonts.append(tf)
    return fonts


def has_embedded_fonts(unz_dir: Path) -> bool:
    pres = unz_dir / "ppt" / "presentation.xml"
    if not pres.exists():
        return False
    root = etree.fromstring(pres.read_bytes())
    emb = root.find(".//p:embeddedFontLst", namespaces=NS)
    if emb is not None:
        return True
    fonts_dir = unz_dir / "ppt" / "fonts"
    return fonts_dir.exists() and any(fonts_dir.iterdir())


def is_full_bleed(shape: ShapeInfo, slide_w: float = 13.333, slide_h: float = 7.5, tol: float = 0.15) -> bool:
    return (
        abs(shape.x) <= tol
        and abs(shape.y) <= tol
        and abs((shape.x + shape.w) - slide_w) <= tol
        and abs((shape.y + shape.h) - slide_h) <= tol
    )


def validate_animation_targets(slide_root: etree._Element, shape_ids: Set[int]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    timing = slide_root.find("p:timing", namespaces=NS)
    if timing is None:
        return findings

    main_seq = timing.find(".//p:cTn[@nodeType='mainSeq']", namespaces=NS)
    if main_seq is None:
        findings.append(make_finding("M2_TIMING_NO_MAINSEQ", "WARN", "p:timing present but no mainSeq"))

    for sp_tgt in timing.findall(".//p:spTgt", namespaces=NS):
        spid_s = sp_tgt.get("spid")
        if not spid_s:
            continue
        try:
            spid = int(spid_s)
        except ValueError:
            continue
        if spid not in shape_ids:
            findings.append(make_finding("M3_TIMING_BAD_TARGET", "FAIL", f"animation targets missing spid={spid}"))

    for anim in timing.findall(".//p:animEffect", namespaces=NS):
        flt = anim.get("filter") or ""
        if flt.startswith("wipe(") and flt.endswith(")"):
            direction = flt[len("wipe(") : -1].lower()
            if direction not in ("left", "right", "up", "down"):
                findings.append(make_finding("M4_TIMING_BAD_FILTER", "WARN", f"unknown wipe direction '{direction}'"))

    return findings


def _extract_slide_id(value: Any) -> Optional[str]:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, int):
        return f"S{value:02d}"
    return None


def normalize_vision_entries(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []
    if isinstance(payload.get("slides"), list):
        return [x for x in payload["slides"] if isinstance(x, dict)]
    if payload.get("slide_id") or payload.get("slide"):
        return [payload]
    return []


def _count_unresolved_assets(payload: Any) -> int:
    if not isinstance(payload, dict):
        return 0
    value = payload.get("unresolved_assets")
    if isinstance(value, list):
        return len(value)
    if isinstance(value, int):
        return max(0, value)
    missing = payload.get("missing_assets")
    if isinstance(missing, list):
        return len(missing)
    if isinstance(missing, int):
        return max(0, missing)
    return 0


def evaluate_optional_integrations(
    report: Dict[str, Any],
    slide_count: int,
    deck_findings: List[Dict[str, Any]],
    vision_report_path: Optional[Path] = None,
    thumbnails_dir: Optional[Path] = None,
    asset_plan_report_path: Optional[Path] = None,
) -> None:
    integrations: Dict[str, Any] = {
        "vision_qa": {
            "requested": bool(vision_report_path or thumbnails_dir),
            "report_path": str(vision_report_path) if vision_report_path else None,
            "thumbnails_dir": str(thumbnails_dir) if thumbnails_dir else None,
            "report_loaded": False,
            "slide_entries": 0,
            "thumbnail_count": 0,
        },
        "asset_plan": {
            "requested": bool(asset_plan_report_path),
            "report_path": str(asset_plan_report_path) if asset_plan_report_path else None,
            "report_loaded": False,
            "unresolved_assets": 0,
        },
    }

    if thumbnails_dir:
        if not thumbnails_dir.exists() or not thumbnails_dir.is_dir():
            deck_findings.append(
                make_finding(
                    "V20_THUMBNAILS_MISSING",
                    "WARN",
                    f"thumbnails directory not found: {thumbnails_dir}",
                    "Generate thumbnails before running vision QA.",
                )
            )
        else:
            thumbs = sorted(
                [
                    p
                    for p in thumbnails_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
                ]
            )
            integrations["vision_qa"]["thumbnail_count"] = len(thumbs)
            if not thumbs:
                deck_findings.append(
                    make_finding(
                        "V21_THUMBNAILS_EMPTY",
                        "WARN",
                        f"thumbnails directory contains no images: {thumbnails_dir}",
                    )
                )
            elif len(thumbs) < slide_count:
                deck_findings.append(
                    make_finding(
                        "V22_THUMBNAILS_INCOMPLETE",
                        "WARN",
                        f"thumbnails={len(thumbs)} but slides={slide_count}",
                        "Re-render thumbnails and ensure all slides exported.",
                    )
                )

    if vision_report_path:
        if not vision_report_path.exists():
            deck_findings.append(
                make_finding(
                    "V10_VISION_REPORT_MISSING",
                    "WARN",
                    f"vision report not found: {vision_report_path}",
                    "Generate vision QA report or disable --vision-qa for this run.",
                )
            )
        else:
            try:
                payload = json.loads(vision_report_path.read_text(encoding="utf-8"))
                entries = normalize_vision_entries(payload)
                integrations["vision_qa"]["report_loaded"] = True
                integrations["vision_qa"]["slide_entries"] = len(entries)
            except Exception as exc:
                deck_findings.append(
                    make_finding(
                        "V11_VISION_REPORT_INVALID",
                        "WARN",
                        f"vision report parse error: {exc}",
                    )
                )
                entries = []

            for entry in entries:
                verdict = str(entry.get("verdict") or "").strip().lower()
                slide_id = _extract_slide_id(entry.get("slide_id") or entry.get("slide")) or "unknown"
                if verdict in {"fail", "reject", "blocked", "hard_fail"}:
                    deck_findings.append(
                        make_finding(
                            "V12_VISION_FAIL",
                            "WARN",
                            f"{slide_id}: verdict={verdict}",
                            "Apply deterministic IR fixes and re-run vision QA.",
                        )
                    )
                score = entry.get("overall_score")
                if isinstance(score, (int, float)) and score < 3.5:
                    deck_findings.append(
                        make_finding(
                            "V13_VISION_LOW_SCORE",
                            "WARN",
                            f"{slide_id}: overall_score={float(score):.2f}",
                            "Consider auto_fix_ir.py before shipping.",
                        )
                    )

    if asset_plan_report_path:
        if not asset_plan_report_path.exists():
            deck_findings.append(
                make_finding(
                    "A40_ASSET_PLAN_REPORT_MISSING",
                    "WARN",
                    f"asset planning report not found: {asset_plan_report_path}",
                )
            )
        else:
            try:
                payload = json.loads(asset_plan_report_path.read_text(encoding="utf-8"))
                unresolved = _count_unresolved_assets(payload)
                integrations["asset_plan"]["report_loaded"] = True
                integrations["asset_plan"]["unresolved_assets"] = unresolved
                if unresolved > 0:
                    deck_findings.append(
                        make_finding(
                            "A41_ASSET_PLAN_UNRESOLVED",
                            "WARN",
                            f"asset planner reported unresolved assets: {unresolved}",
                            "Resolve or replace missing assets before final export.",
                        )
                    )
            except Exception as exc:
                deck_findings.append(
                    make_finding(
                        "A42_ASSET_PLAN_REPORT_INVALID",
                        "WARN",
                        f"asset planning report parse error: {exc}",
                    )
                )

    report["integrations"] = integrations


def preflight(
    pptx_path: Path,
    safe_margin_in: float = 0.7,
    vision_report_path: Optional[Path] = None,
    thumbnails_dir: Optional[Path] = None,
    asset_plan_report_path: Optional[Path] = None,
) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="pptx_pf_") as tmp:
        unz = Path(tmp)
        unzip_pptx(pptx_path, unz)

        slide_dir = unz / "ppt" / "slides"
        if not slide_dir.exists():
            raise FileNotFoundError("ppt/slides missing")

        embedded = has_embedded_fonts(unz)
        used_fonts: Set[str] = set()
        referenced_media_paths: Set[str] = set()

        report: Dict[str, Any] = {"slides": [], "summary": {"hard_fail": 0, "warnings": 0}}
        hard = 0
        warn = 0

        slide_files = sorted(
            [p for p in slide_dir.glob("slide*.xml")],
            key=lambda p: int(re.findall(r"\d+", p.stem)[0]),
        )

        for sp in slide_files:
            snum = int(re.findall(r"\d+", sp.stem)[0])
            root = etree.fromstring(sp.read_bytes())
            shapes = list_shapes(root)
            shape_ids = {s.spid for s in shapes}

            findings: List[Dict[str, Any]] = []

            for shape in shapes:
                if is_full_bleed(shape):
                    continue
                if re.search(r"\b(bg|background|hero)\b", shape.name.lower()):
                    continue
                if (
                    shape.x < safe_margin_in - 1e-6
                    or shape.y < safe_margin_in - 1e-6
                    or (shape.x + shape.w) > (13.333 - safe_margin_in + 1e-6)
                    or (shape.y + shape.h) > (7.5 - safe_margin_in + 1e-6)
                ):
                    findings.append(
                        make_finding(
                            "G10_SAFEZONE_OVERFLOW",
                            "WARN",
                            f"{shape.kind} spid={shape.spid} name='{shape.name}' bbox=({shape.x:.2f},{shape.y:.2f},{shape.w:.2f},{shape.h:.2f})",
                        )
                    )

            min_font = 999.0
            for run_props in root.findall(".//a:rPr", namespaces=NS):
                value = run_props.get("sz")
                if not value:
                    continue
                try:
                    min_font = min(min_font, int(value) / 100.0)
                except Exception:
                    continue
            if min_font != 999.0 and min_font < 10:
                findings.append(make_finding("T10_FONT_TOO_SMALL", "WARN", f"min font ~{min_font:.1f}pt"))

            rels = slide_rels_map(unz / "ppt" / "slides" / "_rels" / f"slide{snum}.xml.rels")
            pics = find_images(root)
            for pic in pics:
                spid = pic["spid"]
                embed_rid = pic.get("embed_rid")
                link_rid = pic.get("link_rid")

                if link_rid and not embed_rid:
                    findings.append(
                        make_finding(
                            "I24_IMAGE_EXTERNAL_LINK",
                            "WARN",
                            f"spid={spid} uses external image link rid={link_rid}",
                            "Prefer embedded images for portable decks.",
                        )
                    )

                if not embed_rid:
                    continue

                rel = rels.get(embed_rid)
                if not rel:
                    findings.append(
                        make_finding(
                            "I20_IMAGE_REL_MISSING",
                            "FAIL",
                            f"spid={spid} rid={embed_rid} has no relationship target",
                        )
                    )
                    continue

                if str(rel.get("target_mode") or "").lower() == "external":
                    findings.append(
                        make_finding(
                            "I24_IMAGE_EXTERNAL_LINK",
                            "WARN",
                            f"spid={spid} rid={embed_rid} points to external target={rel.get('target')}",
                            "Prefer embedded images for portable decks.",
                        )
                    )
                    continue

                target = rel.get("target") or ""
                img_path = resolve_rel_target(unz / "ppt" / "slides", target)
                if not img_path.exists():
                    fallback = unz / "ppt" / "media" / Path(target).name
                    img_path = fallback if fallback.exists() else img_path

                if not img_path.exists():
                    findings.append(
                        make_finding(
                            "I21_IMAGE_FILE_MISSING",
                            "FAIL",
                            f"missing image file for rid={embed_rid} -> {target}",
                        )
                    )
                    continue

                media_rel = safe_rel_path(img_path, unz)
                referenced_media_paths.add(media_rel)

                ext = img_path.suffix.lower()
                if ext and ext not in KNOWN_IMAGE_EXTS:
                    findings.append(
                        make_finding(
                            "I26_IMAGE_UNKNOWN_EXT",
                            "WARN",
                            f"{img_path.name} uses nonstandard extension '{ext}'",
                        )
                    )

                try:
                    byte_size = img_path.stat().st_size
                except Exception:
                    byte_size = 0
                if byte_size <= 0:
                    findings.append(make_finding("I27_IMAGE_EMPTY_FILE", "FAIL", f"{img_path.name} is empty"))
                    continue
                if byte_size > MAX_IMAGE_BYTES_WARN:
                    findings.append(
                        make_finding(
                            "I28_IMAGE_LARGE_FILE",
                            "WARN",
                            f"{img_path.name} size={byte_size / (1024 * 1024):.1f}MB",
                            "Consider compression to reduce deck size.",
                        )
                    )

                shape = next((s for s in shapes if s.spid == spid), None)
                if not shape:
                    continue

                px = read_image_size_px(img_path)
                if not px:
                    findings.append(make_finding("I22_IMAGE_UNREADABLE", "WARN", f"cannot read {img_path.name}"))
                    continue
                pw, ph = px
                dpi_x = pw / max(shape.w, 0.01)
                dpi_y = ph / max(shape.h, 0.01)
                eff = min(dpi_x, dpi_y)
                area = shape.w * shape.h
                thresh = 150 if area >= 12.0 else 100
                if eff < thresh:
                    findings.append(
                        make_finding(
                            "I23_IMAGE_LOW_DPI",
                            "WARN",
                            f"{img_path.name} effective ~{eff:.0f} DPI (< {thresh}); displayed {shape.w:.2f}x{shape.h:.2f} in; pixels {pw}x{ph}",
                        )
                    )

            for font_name in collect_fonts_in_slide(root):
                used_fonts.add(font_name)

            findings.extend(validate_animation_targets(root, shape_ids))

            sfail = sum(1 for f in findings if f.get("severity") == "FAIL")
            swarn = sum(1 for f in findings if f.get("severity") == "WARN")
            hard += sfail
            warn += swarn

            report["slides"].append(
                {
                    "slide_number": snum,
                    "fail": sfail,
                    "warn": swarn,
                    "findings": findings,
                }
            )

        deck_findings: List[Dict[str, Any]] = []
        safe_fonts = {"Calibri", "Arial", "Times New Roman", "Cambria", "Segoe UI"}
        nonstandard = sorted([f for f in used_fonts if f and f not in safe_fonts])
        if nonstandard and not embedded:
            deck_findings.append(
                make_finding(
                    "F30_FONTS_NOT_EMBEDDED",
                    "WARN",
                    f"nonstandard fonts used without embedding: {nonstandard}",
                    "Embed fonts (if licensing allows) or switch to standard fonts.",
                )
            )

        media_dir = unz / "ppt" / "media"
        if media_dir.exists():
            media_files = [p for p in media_dir.iterdir() if p.is_file()]
            for media_file in media_files:
                rel_path = media_file.relative_to(unz).as_posix()
                if rel_path not in referenced_media_paths:
                    deck_findings.append(
                        make_finding(
                            "A31_UNUSED_MEDIA",
                            "WARN",
                            f"unreferenced media asset: {rel_path}",
                            "Remove unused assets to keep package lean.",
                        )
                    )
                if media_file.stat().st_size <= 0:
                    deck_findings.append(make_finding("A32_EMPTY_MEDIA_FILE", "FAIL", f"media file is empty: {rel_path}"))

        evaluate_optional_integrations(
            report=report,
            slide_count=len(slide_files),
            deck_findings=deck_findings,
            vision_report_path=vision_report_path,
            thumbnails_dir=thumbnails_dir,
            asset_plan_report_path=asset_plan_report_path,
        )

        report["deck_findings"] = deck_findings
        hard += sum(1 for f in deck_findings if f.get("severity") == "FAIL")
        warn += sum(1 for f in deck_findings if f.get("severity") == "WARN")

        report["summary"]["hard_fail"] = hard
        report["summary"]["warnings"] = warn
        return report


def to_markdown(report: Dict[str, Any]) -> str:
    summary = report.get("summary") or {}
    slides = report.get("slides") or []
    verdict = "PASS" if int(summary.get("hard_fail") or 0) == 0 else "FAIL"
    lines: List[str] = []
    lines.append(f"# PPTX QA report — {verdict}")
    lines.append("")
    lines.append(f"Slides: {len(slides)}  ")
    lines.append(f"Hard fails: {summary.get('hard_fail', 0)}  ")
    lines.append(f"Warnings: {summary.get('warnings', 0)}")
    lines.append("")

    deck_findings = report.get("deck_findings") or []
    if deck_findings:
        lines.append("## Deck findings")
        for finding in deck_findings:
            sev = finding.get("severity", "WARN")
            lines.append(f"- [{sev}] {finding.get('code', 'UNKNOWN')}: {finding.get('evidence', '')}")
            if finding.get("fix"):
                lines.append(f"  - Fix: {finding['fix']}")
        lines.append("")

    for slide in slides:
        lines.append(f"## Slide {slide.get('slide_number')}")
        lines.append(f"- Hard fails: {slide.get('fail', 0)} | Warnings: {slide.get('warn', 0)}")
        for finding in slide.get("findings") or []:
            sev = finding.get("severity", "WARN")
            lines.append(f"- [{sev}] {finding.get('code', 'UNKNOWN')}: {finding.get('evidence', '')}")
            if finding.get("fix"):
                lines.append(f"  - Fix: {finding['fix']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", type=Path)
    ap.add_argument("--out", type=Path, default=None, help="Write JSON report to this file")
    ap.add_argument("--md", type=Path, default=None, help="Write Markdown report to this file")
    ap.add_argument("--safe-margin", type=float, default=0.7, help="Safe margin in inches (default 0.7)")
    ap.add_argument("--vision-report", type=Path, default=None, help="Optional vision QA JSON report path")
    ap.add_argument("--thumbnails-dir", type=Path, default=None, help="Optional directory of rendered slide thumbnails")
    ap.add_argument("--asset-plan-report", type=Path, default=None, help="Optional asset-planning JSON report path")
    args = ap.parse_args()

    rep = preflight(
        args.pptx,
        safe_margin_in=float(args.safe_margin),
        vision_report_path=args.vision_report,
        thumbnails_dir=args.thumbnails_dir,
        asset_plan_report_path=args.asset_plan_report,
    )
    if args.out:
        args.out.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    if args.md:
        args.md.write_text(to_markdown(rep), encoding="utf-8")

    summary = rep["summary"]
    print(f"PPTX preflight: hard_fail={summary['hard_fail']} warnings={summary['warnings']} slides={len(rep['slides'])}")
    return 0 if summary["hard_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
