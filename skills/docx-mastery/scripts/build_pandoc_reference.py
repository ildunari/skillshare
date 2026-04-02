#!/usr/bin/env python3
"""scripts/build_pandoc_reference.py

Generate Pandoc reference DOCX files from this skill's style-spec JSON profiles.

Why this exists:
- docx-js creation path is the default (max control).
- For *simple* docs written in Markdown, Pandoc + --reference-doc is a fast path.

Pandoc uses style *names* in the reference document to style elements.
This script starts from Pandoc's own default reference.docx, then rewrites:
- document section geometry (page size, margins)
- key paragraph styles (Title, Heading 1, Body Text, etc.)
- key character styles (Verbatim Char for inline code)
- the default table style (Table) for padding/borders/header shading

It outputs ready-to-use reference docs under assets/pandoc/.

Usage:
  # Build all bundled profiles
  python scripts/build_pandoc_reference.py

  # Build one profile
  python scripts/build_pandoc_reference.py --spec assets/style-specs/business_report_modern.json --out assets/pandoc/reference_business_report_modern.docx

Notes:
- Requires `pandoc` in PATH.
- Does not need Microsoft Word.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import zipfile
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

try:
    from lxml import etree
except Exception as e:  # pragma: no cover
    raise SystemExit("lxml is required (should be pre-installed in this sandbox)") from e


# ---------------------------
# Spec helpers
# ---------------------------


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = deepcopy(v)
    return out


def resolve_based_on(spec: Dict[str, Any], kind: str, style_id: str) -> Dict[str, Any]:
    """Resolve a paragraph/character/table style definition with `based_on` inheritance."""
    styles = spec.get(kind) or {}
    if style_id not in styles:
        return {}

    visited = set()
    cur = style_id
    merged: Dict[str, Any] = {}

    while cur:
        if cur in visited:
            break
        visited.add(cur)
        d = styles.get(cur) or {}
        parent = d.get("based_on")
        merged = _deep_merge(d, merged)  # parent first, then child overrides
        cur = parent

    # Remove based_on to avoid re-processing
    merged.pop("based_on", None)
    return merged


def resolve_color(spec: Dict[str, Any], name_or_hex: Optional[str]) -> Optional[str]:
    if not name_or_hex:
        return None
    if not isinstance(name_or_hex, str):
        return None

    colors = spec.get("colors") or {}
    if name_or_hex in colors:
        raw = str(colors[name_or_hex])
    else:
        raw = name_or_hex

    raw = raw.strip().lstrip("#")
    if len(raw) == 6 and all(c in "0123456789abcdefABCDEF" for c in raw):
        return raw.upper()
    return None


def resolve_font_family(spec: Dict[str, Any], family_or_key: Optional[str], fallback_key: str = "body") -> Optional[str]:
    fonts = spec.get("fonts") or {}

    key = family_or_key or fallback_key
    if key in fonts and isinstance(fonts[key], dict):
        fam = fonts[key].get("family")
        if fam:
            return str(fam)
    # Allow explicit font names
    if family_or_key and family_or_key not in fonts:
        return str(family_or_key)

    # Final fallback to body family if present
    body = fonts.get("body") or {}
    if isinstance(body, dict) and body.get("family"):
        return str(body["family"])
    return None


def resolve_font_size_pt(spec: Dict[str, Any], family_key: str, default_pt: Optional[float] = None) -> Optional[float]:
    fonts = spec.get("fonts") or {}
    d = fonts.get(family_key)
    if isinstance(d, dict) and isinstance(d.get("size_pt"), (int, float)):
        return float(d["size_pt"])
    return default_pt


# ---------------------------
# Pandoc style mapping
# ---------------------------


@dataclass
class PandocStyleMap:
    # paragraph styles
    title: str = "Title"
    subtitle: str = "Subtitle"
    heading1: str = "Heading 1"
    heading2: str = "Heading 2"
    heading3: str = "Heading 3"
    body_text: str = "Body Text"
    first_paragraph: str = "First Paragraph"
    normal: str = "Normal"
    compact: str = "Compact"
    block_text: str = "Block Text"
    table_caption: str = "Table Caption"
    image_caption: str = "Image Caption"
    caption: str = "Caption"
    captioned_figure: str = "Captioned Figure"
    bibliography: str = "Bibliography"
    source_code: str = "Source Code"  # Pandoc uses this for fenced code blocks

    # character styles
    verbatim_char: str = "Verbatim Char"  # Pandoc uses this for inline code

    # table style
    table: str = "Table"  # default table style in Pandoc reference doc


PANDOC_MAP = PandocStyleMap()


def _pick_quote_style_id(spec: Dict[str, Any]) -> Optional[str]:
    ps = spec.get("paragraphStyles") or {}
    if "BlockQuote" in ps:
        return "BlockQuote"
    if "Quote" in ps:
        return "Quote"
    return None


def build_pandoc_to_spec_map(spec: Dict[str, Any]) -> Dict[str, str]:
    ps = spec.get("paragraphStyles") or {}

    def has(sid: str) -> bool:
        return sid in ps

    quote = _pick_quote_style_id(spec) or ("Body" if has("Body") else "Normal")

    out: Dict[str, str] = {
        PANDOC_MAP.title: "Title" if has("Title") else ("Heading1" if has("Heading1") else "Body"),
        PANDOC_MAP.subtitle: "Subtitle" if has("Subtitle") else ("Body" if has("Body") else "Normal"),
        PANDOC_MAP.heading1: "Heading1" if has("Heading1") else "Body",
        PANDOC_MAP.heading2: "Heading2" if has("Heading2") else "Heading1" if has("Heading1") else "Body",
        PANDOC_MAP.heading3: "Heading3" if has("Heading3") else "Heading2" if has("Heading2") else "Body",
        PANDOC_MAP.body_text: "Body" if has("Body") else "Normal",
        PANDOC_MAP.first_paragraph: "Body" if has("Body") else "Normal",
        PANDOC_MAP.normal: "Body" if has("Body") else "Normal",
        PANDOC_MAP.compact: "BodyCompact" if has("BodyCompact") else ("Body" if has("Body") else "Normal"),
        PANDOC_MAP.block_text: quote,
        PANDOC_MAP.table_caption: "TableCaption" if has("TableCaption") else ("BodyCompact" if has("BodyCompact") else "Body"),
        PANDOC_MAP.image_caption: "FigureCaption" if has("FigureCaption") else ("BodyCompact" if has("BodyCompact") else "Body"),
        PANDOC_MAP.caption: "FigureCaption" if has("FigureCaption") else ("BodyCompact" if has("BodyCompact") else "Body"),
        # Captioned Figure is the paragraph that *contains* the image run.
        # No direct equivalent in our specs; style it like body but keep-with-next.
        PANDOC_MAP.captioned_figure: "Body" if has("Body") else "Normal",
        PANDOC_MAP.bibliography: "Body" if has("Body") else "Normal",
        # Source Code may not exist in the Pandoc reference doc; we'll create it.
        PANDOC_MAP.source_code: "CodeBlock" if has("CodeBlock") else ("Body" if has("Body") else "Normal"),
    }

    return out


# ---------------------------
# python-docx style editing
# ---------------------------


def _ensure_rpr(style) -> Any:
    # style._element is a CT_Style; get_or_add_rPr exists.
    return style._element.get_or_add_rPr()


def _ensure_ppr(style) -> Any:
    return style._element.get_or_add_pPr()


def set_style_font(
    spec: Dict[str, Any],
    style,
    font_def: Dict[str, Any],
    default_family_key: str,
    default_size_pt: Optional[float],
    color_hex: Optional[str] = None,
) -> None:
    fam_key = font_def.get("family") if isinstance(font_def, dict) else None
    family = resolve_font_family(spec, fam_key, fallback_key=default_family_key)
    size_pt = None
    if isinstance(font_def, dict) and isinstance(font_def.get("size_pt"), (int, float)):
        size_pt = float(font_def["size_pt"])
    if size_pt is None:
        size_pt = default_size_pt

    bold = None
    italic = None
    if isinstance(font_def, dict):
        if "bold" in font_def:
            bold = bool(font_def.get("bold"))
        if "italic" in font_def:
            italic = bool(font_def.get("italic"))

    font = style.font
    if family:
        font.name = family
        rpr = _ensure_rpr(style)
        rfonts = rpr.get_or_add_rFonts()
        rfonts.set(qn("w:ascii"), family)
        rfonts.set(qn("w:hAnsi"), family)
        rfonts.set(qn("w:eastAsia"), family)
        rfonts.set(qn("w:cs"), family)

    if size_pt is not None:
        font.size = Pt(size_pt)

    if bold is not None:
        font.bold = bold
    if italic is not None:
        font.italic = italic

    if color_hex:
        try:
            font.color.rgb = RGBColor.from_string(color_hex)
        except Exception:
            pass


def set_paragraph_format(style, defn: Dict[str, Any]) -> None:
    pf = style.paragraph_format

    # Alignment
    align = defn.get("alignment")
    if isinstance(align, str):
        a = align.strip().lower()
        if a == "center":
            pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif a == "right":
            pf.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif a == "justify":
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Spacing
    if isinstance(defn.get("space_before_pt"), (int, float)):
        pf.space_before = Pt(float(defn["space_before_pt"]))
    if isinstance(defn.get("space_after_pt"), (int, float)):
        pf.space_after = Pt(float(defn["space_after_pt"]))

    # Line spacing
    if isinstance(defn.get("line_spacing_multiple"), (int, float)):
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = float(defn["line_spacing_multiple"])

    # Indents
    if isinstance(defn.get("left_indent_in"), (int, float)):
        pf.left_indent = Inches(float(defn["left_indent_in"]))
    if isinstance(defn.get("right_indent_in"), (int, float)):
        pf.right_indent = Inches(float(defn["right_indent_in"]))
    if isinstance(defn.get("first_line_indent_in"), (int, float)):
        pf.first_line_indent = Inches(float(defn["first_line_indent_in"]))
    if isinstance(defn.get("hanging_indent_in"), (int, float)):
        h = float(defn["hanging_indent_in"])
        pf.left_indent = Inches(h)
        pf.first_line_indent = Inches(-h)

    # Pagination controls
    if "keep_with_next" in defn:
        try:
            pf.keep_with_next = bool(defn.get("keep_with_next"))
        except Exception:
            pass
    if "keep_together" in defn:
        try:
            pf.keep_together = bool(defn.get("keep_together"))
        except Exception:
            pass
    if "widow_control" in defn:
        try:
            pf.widow_control = bool(defn.get("widow_control"))
        except Exception:
            pass


def set_shading_on_style(style, fill_hex: str, for_paragraph: bool) -> None:
    fill_hex = fill_hex.upper()
    if not (len(fill_hex) == 6 and all(c in "0123456789ABCDEF" for c in fill_hex)):
        return

    if for_paragraph:
        ppr = _ensure_ppr(style)
        shd = ppr.find(qn("w:shd"))
        if shd is None:
            shd = OxmlElement("w:shd")
            ppr.append(shd)
    else:
        rpr = _ensure_rpr(style)
        shd = rpr.find(qn("w:shd"))
        if shd is None:
            shd = OxmlElement("w:shd")
            rpr.append(shd)

    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)


def apply_paragraph_style(doc: Document, spec: Dict[str, Any], pandoc_style_name: str, spec_style_id: str) -> None:
    # Ensure style exists (pandoc reference doc contains most, but not Source Code)
    try:
        style = doc.styles[pandoc_style_name]
    except KeyError:
        style = doc.styles.add_style(pandoc_style_name, WD_STYLE_TYPE.PARAGRAPH)

    defn = resolve_based_on(spec, "paragraphStyles", spec_style_id)

    fonts = spec.get("fonts") or {}
    body_family = resolve_font_family(spec, "body", fallback_key="body")
    body_size = resolve_font_size_pt(spec, "body", default_pt=11)

    # Determine default font family key: headings use 'heading' if present
    default_family_key = "body"
    if spec_style_id.lower().startswith("heading") and isinstance(fonts.get("heading"), dict):
        default_family_key = "heading"

    font_def = defn.get("font") if isinstance(defn.get("font"), dict) else {}

    # Colors can be given as a key (e.g., 'accent') or hex.
    color_hex = resolve_color(spec, defn.get("color"))

    set_style_font(spec, style, font_def, default_family_key=default_family_key, default_size_pt=body_size, color_hex=color_hex)
    set_paragraph_format(style, defn)

    # Paragraph shading
    shd = defn.get("shading")
    shd_hex = resolve_color(spec, shd) if isinstance(shd, str) else None
    if shd_hex:
        set_shading_on_style(style, shd_hex, for_paragraph=True)

    # Special-case: Captioned Figure should keep-with-next to keep image with caption
    if pandoc_style_name == PANDOC_MAP.captioned_figure:
        try:
            style.paragraph_format.keep_with_next = True
        except Exception:
            pass


def apply_character_style(doc: Document, spec: Dict[str, Any], pandoc_style_name: str, spec_style_id: str) -> None:
    try:
        style = doc.styles[pandoc_style_name]
    except KeyError:
        style = doc.styles.add_style(pandoc_style_name, WD_STYLE_TYPE.CHARACTER)

    defn = resolve_based_on(spec, "characterStyles", spec_style_id)

    fonts = spec.get("fonts") or {}
    body_size = resolve_font_size_pt(spec, "body", default_pt=11)

    font_def = defn.get("font") if isinstance(defn.get("font"), dict) else {}
    default_family_key = "body"
    if font_def.get("family") == "mono" or pandoc_style_name == PANDOC_MAP.verbatim_char:
        default_family_key = "mono" if isinstance(fonts.get("mono"), dict) else "body"

    color_hex = resolve_color(spec, defn.get("color"))

    set_style_font(spec, style, font_def, default_family_key=default_family_key, default_size_pt=body_size, color_hex=color_hex)

    # Bold/italic flags at the top level (Emphasis, Strong)
    if "bold" in defn:
        style.font.bold = bool(defn.get("bold"))
    if "italic" in defn:
        style.font.italic = bool(defn.get("italic"))

    # Shading
    shd = defn.get("shading")
    shd_hex = resolve_color(spec, shd) if isinstance(shd, str) else None
    if shd_hex:
        set_shading_on_style(style, shd_hex, for_paragraph=False)


# ---------------------------
# Table style patching (OOXML)
# ---------------------------


def _twips_from_pt(pt: float) -> int:
    return int(round(float(pt) * 20))


def _border_attrs(val: str, sz: Optional[int] = None, color: Optional[str] = None) -> Dict[str, str]:
    d: Dict[str, str] = {qn("w:val"): val}
    if sz is not None:
        d[qn("w:sz")] = str(int(sz))
        d[qn("w:space")] = "0"
    if color:
        d[qn("w:color")] = color
    return d


def _apply_tbl_borders(tbl_borders, preset: str, line_color: str = "C7C7C7", strong_color: str = "7F7F7F") -> Dict[str, Dict[str, str]]:
    """Return border element attribute dicts for top/bottom/left/right/insideH/insideV."""
    p = (preset or "").strip().lower()

    # Sizes are 1/8pt.
    HAIR = 1
    LIGHT = 2
    STRONG = 4

    def none():
        return _border_attrs("nil")

    def hair():
        return _border_attrs("single", sz=HAIR, color=line_color)

    def light():
        return _border_attrs("single", sz=LIGHT, color=line_color)

    def strong():
        return _border_attrs("single", sz=STRONG, color=strong_color)

    if p in ("full_grid", "grid"):
        return {
            "top": light(),
            "bottom": light(),
            "left": light(),
            "right": light(),
            "insideH": light(),
            "insideV": light(),
            "headerBottom": light(),
        }

    if p == "light_horizontal":
        return {
            "top": none(),
            "bottom": strong(),
            "left": none(),
            "right": none(),
            "insideH": hair(),
            "insideV": none(),
            "headerBottom": strong(),
        }

    # Default: minimal_horizontal
    return {
        "top": strong(),
        "bottom": strong(),
        "left": none(),
        "right": none(),
        "insideH": hair(),
        "insideV": none(),
        "headerBottom": strong(),
    }


def patch_table_style(docx_path: Path, spec: Dict[str, Any]) -> None:
    """Patch word/styles.xml to make the default Pandoc table style match the profile."""
    # Choose first table style def in spec
    table_styles = spec.get("tableStyles") or {}
    if not isinstance(table_styles, dict) or not table_styles:
        return
    t_key = next(iter(table_styles.keys()))
    t_def = table_styles[t_key] or {}

    # Table-level font defaults (applies to all cells unless overridden)
    t_font = t_def.get("font") or {}
    t_font_family = resolve_font_family(spec, t_font.get("family") if isinstance(t_font, dict) else None, fallback_key="body")
    t_font_size_pt = None
    if isinstance(t_font, dict) and isinstance(t_font.get("size_pt"), (int, float)):
        t_font_size_pt = float(t_font.get("size_pt"))
    if t_font_size_pt is None:
        t_font_size_pt = resolve_font_size_pt(spec, "body", default_pt=11) or 11

    padding = t_def.get("cell_padding_pt") or {}
    borders_preset = t_def.get("borders") or "minimal_horizontal"
    header_row = t_def.get("header_row") or {}

    header_fill = resolve_color(spec, header_row.get("shading")) or resolve_color(spec, "tableHeaderFill") or "EDEDED"
    header_bold = header_row.get("bold") is not False

    # Default padding fallback
    pad_top = float(padding.get("top", 5))
    pad_bottom = float(padding.get("bottom", 5))
    pad_left = float(padding.get("left", 6))
    pad_right = float(padding.get("right", 6))

    border_defs = _apply_tbl_borders(None, borders_preset)

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        # unzip
        with zipfile.ZipFile(docx_path, "r") as zf:
            zf.extractall(td_path)

        styles_xml = td_path / "word" / "styles.xml"
        if not styles_xml.exists():
            return

        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(str(styles_xml), parser)
        root = tree.getroot()
        ns = {
            "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        }

        # Find the table style named "Table" (styleId Table)
        style = root.xpath(".//w:style[@w:type='table' and @w:styleId='Table']", namespaces=ns)
        if not style:
            return
        style_el = style[0]

        # Ensure table style has an rPr with font + size (Pandoc doesn't set table fonts explicitly).
        rPr = style_el.find("w:rPr", namespaces=ns)
        if rPr is None:
            # Insert after <w:name> if present for nicer ordering.
            name_el = style_el.find("w:name", namespaces=ns)
            rPr = etree.Element(qn("w:rPr"))
            if name_el is not None:
                style_el.insert(style_el.index(name_el) + 1, rPr)
            else:
                style_el.insert(0, rPr)

        if t_font_family:
            rFonts = rPr.find("w:rFonts", namespaces=ns)
            if rFonts is None:
                rFonts = etree.Element(qn("w:rFonts"))
                rPr.append(rFonts)
            rFonts.set(qn("w:ascii"), t_font_family)
            rFonts.set(qn("w:hAnsi"), t_font_family)
            rFonts.set(qn("w:eastAsia"), t_font_family)
            rFonts.set(qn("w:cs"), t_font_family)

        # Size in half-points
        sz_val = str(int(round(t_font_size_pt * 2)))
        sz = rPr.find("w:sz", namespaces=ns)
        if sz is None:
            sz = etree.Element(qn("w:sz"))
            rPr.append(sz)
        sz.set(qn("w:val"), sz_val)
        szCs = rPr.find("w:szCs", namespaces=ns)
        if szCs is None:
            szCs = etree.Element(qn("w:szCs"))
            rPr.append(szCs)
        szCs.set(qn("w:val"), sz_val)

        # Optional muted text color
        muted = resolve_color(spec, "mutedText")
        if muted:
            color = rPr.find("w:color", namespaces=ns)
            if color is None:
                color = etree.Element(qn("w:color"))
                rPr.append(color)
            color.set(qn("w:val"), muted)

        tblPr = style_el.find("w:tblPr", namespaces=ns)
        if tblPr is None:
            tblPr = etree.Element(qn("w:tblPr"))
            style_el.append(tblPr)

        # cell margins
        tblCellMar = tblPr.find("w:tblCellMar", namespaces=ns)
        if tblCellMar is None:
            tblCellMar = etree.Element(qn("w:tblCellMar"))
            tblPr.append(tblCellMar)

        def set_mar(side: str, pt_val: float) -> None:
            el = tblCellMar.find(f"w:{side}", namespaces=ns)
            if el is None:
                el = etree.Element(qn(f"w:{side}"))
                tblCellMar.append(el)
            el.set(qn("w:w"), str(_twips_from_pt(pt_val)))
            el.set(qn("w:type"), "dxa")

        set_mar("top", pad_top)
        set_mar("bottom", pad_bottom)
        set_mar("left", pad_left)
        set_mar("right", pad_right)

        # Borders for the whole table
        tblBorders = tblPr.find("w:tblBorders", namespaces=ns)
        if tblBorders is None:
            tblBorders = etree.Element(qn("w:tblBorders"))
            tblPr.append(tblBorders)

        def set_border(name: str, attrs: Dict[str, str]) -> None:
            el = tblBorders.find(f"w:{name}", namespaces=ns)
            if el is None:
                el = etree.Element(qn(f"w:{name}"))
                tblBorders.append(el)
            # Clear existing attrs then set
            for k in list(el.attrib.keys()):
                el.attrib.pop(k, None)
            for k, v in attrs.items():
                el.set(k, v)

        set_border("top", border_defs["top"])
        set_border("bottom", border_defs["bottom"])
        set_border("left", border_defs["left"])
        set_border("right", border_defs["right"])
        set_border("insideH", border_defs["insideH"])
        set_border("insideV", border_defs["insideV"])

        # First row overrides: shading + stronger bottom border + bold
        # Find/create tblStylePr type="firstRow"
        first_row = style_el.xpath("./w:tblStylePr[@w:type='firstRow']", namespaces=ns)
        if first_row:
            first_el = first_row[0]
        else:
            first_el = etree.Element(qn("w:tblStylePr"))
            first_el.set(qn("w:type"), "firstRow")
            style_el.append(first_el)

        tcPr = first_el.find("w:tcPr", namespaces=ns)
        if tcPr is None:
            tcPr = etree.Element(qn("w:tcPr"))
            first_el.append(tcPr)

        # shading
        shd = tcPr.find("w:shd", namespaces=ns)
        if shd is None:
            shd = etree.Element(qn("w:shd"))
            tcPr.append(shd)
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), header_fill)

        # header bottom border
        tcBorders = tcPr.find("w:tcBorders", namespaces=ns)
        if tcBorders is None:
            tcBorders = etree.Element(qn("w:tcBorders"))
            tcPr.append(tcBorders)
        bottom = tcBorders.find("w:bottom", namespaces=ns)
        if bottom is None:
            bottom = etree.Element(qn("w:bottom"))
            tcBorders.append(bottom)
        # Replace attrs
        for k in list(bottom.attrib.keys()):
            bottom.attrib.pop(k, None)
        for k, v in border_defs["headerBottom"].items():
            bottom.set(k, v)

        if header_bold:
            rPr = first_el.find("w:rPr", namespaces=ns)
            if rPr is None:
                rPr = etree.Element(qn("w:rPr"))
                first_el.append(rPr)
            b = rPr.find("w:b", namespaces=ns)
            if b is None:
                b = etree.Element(qn("w:b"))
                rPr.append(b)

        # Write back
        tree.write(str(styles_xml), encoding="UTF-8", xml_declaration=True)

        # Repack (preserve original ordering? zipfile writes new)
        tmp_out = docx_path.with_suffix(".tmp.docx")
        with zipfile.ZipFile(tmp_out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file in sorted(td_path.rglob("*")):
                if file.is_dir():
                    continue
                arc = str(file.relative_to(td_path)).replace("\\", "/")
                zf.write(file, arc)

        shutil.move(str(tmp_out), str(docx_path))


# ---------------------------
# Build pipeline
# ---------------------------


def get_pandoc_reference_base(tmp_dir: Path) -> Path:
    """Write Pandoc's default reference.docx into tmp_dir and return its path."""
    out = tmp_dir / "pandoc_reference_default.docx"
    proc = subprocess.run(
        ["pandoc", "--print-default-data-file", "reference.docx"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout:
        raise RuntimeError(
            "Failed to obtain Pandoc default reference.docx. "
            f"pandoc exit={proc.returncode} stderr={proc.stderr.decode('utf-8','ignore')[:500]}"
        )
    out.write_bytes(proc.stdout)
    return out


def apply_section_geometry(doc: Document, spec: Dict[str, Any]) -> None:
    page = spec.get("page") or {}
    margins = (page.get("margins_in") or {}) if isinstance(page, dict) else {}

    for section in doc.sections:
        # Page size
        size = page.get("size")
        if isinstance(size, str) and size.strip().lower() == "letter":
            section.page_width = Inches(8.5)
            section.page_height = Inches(11)

        # Margins
        if isinstance(margins.get("top"), (int, float)):
            section.top_margin = Inches(float(margins["top"]))
        if isinstance(margins.get("bottom"), (int, float)):
            section.bottom_margin = Inches(float(margins["bottom"]))
        if isinstance(margins.get("left"), (int, float)):
            section.left_margin = Inches(float(margins["left"]))
        if isinstance(margins.get("right"), (int, float)):
            section.right_margin = Inches(float(margins["right"]))


def build_one_reference(spec_path: Path, out_path: Path) -> None:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        base_docx = get_pandoc_reference_base(td_path)

        # Copy base docx to a working path to preserve base doc for multiple builds
        work_docx = td_path / f"work_{spec.get('name','reference')}.docx"
        shutil.copy2(base_docx, work_docx)

        doc = Document(str(work_docx))
        apply_section_geometry(doc, spec)

        # Map Pandoc style names to spec style ids
        p2s = build_pandoc_to_spec_map(spec)

        # Apply paragraph styles
        for pandoc_name, spec_style_id in p2s.items():
            apply_paragraph_style(doc, spec, pandoc_name, spec_style_id)

        # Apply inline code style (Verbatim Char)
        if (spec.get("characterStyles") or {}).get("InlineCode"):
            apply_character_style(doc, spec, PANDOC_MAP.verbatim_char, "InlineCode")
        else:
            # Fallback: set mono font anyway
            try:
                vs = doc.styles[PANDOC_MAP.verbatim_char]
                mono = resolve_font_family(spec, "mono", fallback_key="mono") or "Courier New"
                vs.font.name = mono
                vs.font.size = Pt(resolve_font_size_pt(spec, "mono", default_pt=10) or 10)
            except Exception:
                pass

        # Source Code paragraph style (fenced code blocks)
        # Pandoc uses a paragraph style named "Source Code" in output.
        apply_paragraph_style(doc, spec, PANDOC_MAP.source_code, p2s.get(PANDOC_MAP.source_code, "CodeBlock"))

        # Ensure Normal style uses body font defaults
        try:
            normal = doc.styles[PANDOC_MAP.normal]
            body_family = resolve_font_family(spec, "body", fallback_key="body")
            body_size = resolve_font_size_pt(spec, "body", default_pt=11)
            set_style_font(spec, normal, {"family": "body", "size_pt": body_size}, default_family_key="body", default_size_pt=body_size)
            # Match Body paragraph spacing if specified
            body_def = resolve_based_on(spec, "paragraphStyles", "Body")
            if body_def:
                set_paragraph_format(normal, body_def)
        except Exception:
            pass

        # Save
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(out_path))

        # Patch table style via styles.xml
        patch_table_style(out_path, spec)


def default_profiles(root: Path) -> List[Tuple[Path, Path]]:
    specs_dir = root / "assets" / "style-specs"
    out_dir = root / "assets" / "pandoc"

    names = [
        "business_report_modern",
        "technical_report_engineering",
        "academic_manuscript_generic",
        "nih_grant_basic",
    ]

    pairs: List[Tuple[Path, Path]] = []
    for name in names:
        spec_path = specs_dir / f"{name}.json"
        out_path = out_dir / f"reference_{name}.docx"
        pairs.append((spec_path, out_path))
    return pairs


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Pandoc reference DOCX files from style-spec JSON.")
    parser.add_argument("--spec", type=str, help="Path to a style-spec JSON file.")
    parser.add_argument("--out", type=str, help="Output .docx path (used with --spec).")
    parser.add_argument("--all", action="store_true", help="Build all bundled profiles (default if no --spec).")

    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]

    jobs: List[Tuple[Path, Path]]
    if args.spec:
        if not args.out:
            raise SystemExit("--out is required when --spec is provided")
        jobs = [(Path(args.spec), Path(args.out))]
    else:
        jobs = default_profiles(root)

    for spec_path, out_path in jobs:
        if not spec_path.exists():
            raise SystemExit(f"Missing spec: {spec_path}")
        build_one_reference(spec_path, out_path)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
