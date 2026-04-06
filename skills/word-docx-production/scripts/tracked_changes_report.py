#!/usr/bin/env python3
"""scripts/tracked_changes_report.py

Produce a structured JSON report of *existing* tracked changes and comments in a .docx.

Why:
- The core Document library can *author* new tracked changes in a clean doc.
- This script is for the opposite direction: understand what's already in a doc before you touch it.

Output:
- JSON with lists of tracked changes and comment threads, including author/date and text context.

Notes:
- This is OOXML-level inspection (zip parts + XML). python-docx does not fully surface tracked revisions.
- We scan the main story plus common story parts (headers/footers/footnotes/endnotes).

Usage:
  python scripts/tracked_changes_report.py input.docx -o report.json --pretty

"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from lxml import etree


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16du": "http://schemas.microsoft.com/office/word/2018/wordml",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}

# OOXML tags we treat as "tracked changes".
TRACKED_TAGS = {
    "ins": "ins",
    "del": "del",
    "moveTo": "moveTo",
    "moveFrom": "moveFrom",
    "rPrChange": "rPrChange",
    "pPrChange": "pPrChange",
    "sectPrChange": "sectPrChange",
    "tblPrChange": "tblPrChange",
    "trPrChange": "trPrChange",
    "tcPrChange": "tcPrChange",
}


def qn(prefix: str, local: str) -> str:
    return f"{{{NS[prefix]}}}{local}"


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_dt(s: Optional[str]) -> Optional[str]:
    """Normalize an ISO-ish Word timestamp to RFC3339 (string) if parseable."""
    if not s:
        return None
    try:
        # Word commonly uses '...Z'
        if s.endswith("Z"):
            dt = datetime.fromisoformat(s[:-1] + "+00:00")
        else:
            dt = datetime.fromisoformat(s)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()
    except Exception:
        return s


def get_attr(elem: etree._Element, prefix: str, local: str) -> Optional[str]:
    return elem.get(qn(prefix, local))


def get_attr_any(elem: etree._Element, ns_uri: str, local: str) -> Optional[str]:
    return elem.get(f"{{{ns_uri}}}{local}")


def extract_text_plain(elem: etree._Element) -> str:
    """Extract visible-ish text from an element (ignores tracked-change semantics)."""
    out: List[str] = []
    for node in elem.iter():
        if node.tag == qn("w", "t"):
            if node.text:
                out.append(node.text)
        elif node.tag == qn("w", "tab"):
            out.append("\t")
        elif node.tag == qn("w", "br"):
            out.append("\n")
    return "".join(out)


def extract_text_inserted(ins: etree._Element) -> str:
    out: List[str] = []
    for node in ins.iter():
        if node.tag == qn("w", "t"):
            if node.text:
                out.append(node.text)
        elif node.tag == qn("w", "instrText"):
            if node.text:
                out.append(node.text)
        elif node.tag == qn("w", "tab"):
            out.append("\t")
        elif node.tag == qn("w", "br"):
            out.append("\n")
    return "".join(out)


def extract_text_deleted(del_: etree._Element) -> str:
    out: List[str] = []
    for node in del_.iter():
        if node.tag == qn("w", "delText"):
            if node.text:
                out.append(node.text)
        elif node.tag == qn("w", "delInstrText"):
            if node.text:
                out.append(node.text)
        elif node.tag == qn("w", "tab"):
            out.append("\t")
        elif node.tag == qn("w", "br"):
            out.append("\n")
    return "".join(out)


def render_with_revision_markers(node: etree._Element) -> str:
    """Render a node to text with [+...+] and [-...-] markers for ins/del."""
    # If node is an insertion/deletion wrapper, special-case.
    local = etree.QName(node).localname
    if local == "ins" or local == "moveTo":
        t = extract_text_inserted(node)
        return f"[+{t}+]" if t else "[+ +]"
    if local == "del" or local == "moveFrom":
        t = extract_text_deleted(node)
        return f"[-{t}-]" if t else "[- -]"

    out: List[str] = []
    # Only emit text for allowed leaf elements; recurse through containers.
    if node.tag == qn("w", "t"):
        return node.text or ""
    if node.tag == qn("w", "delText"):
        return node.text or ""
    if node.tag == qn("w", "tab"):
        return "\t"
    if node.tag == qn("w", "br"):
        return "\n"

    for child in node:
        out.append(render_with_revision_markers(child))
    return "".join(out)


def paragraph_context(p: etree._Element) -> str:
    return render_with_revision_markers(p).replace("\n", " ").strip()


def find_story_parts(zf: zipfile.ZipFile) -> List[str]:
    names = set(zf.namelist())
    parts: List[str] = []
    # Main story
    if "word/document.xml" in names:
        parts.append("word/document.xml")
    # Common story parts
    for pat in ("word/header", "word/footer"):
        for n in sorted(names):
            if n.startswith(pat) and n.endswith(".xml"):
                parts.append(n)
    for n in ("word/footnotes.xml", "word/endnotes.xml"):
        if n in names:
            parts.append(n)
    # De-dup while preserving order
    seen: Set[str] = set()
    ordered: List[str] = []
    for p in parts:
        if p not in seen:
            ordered.append(p)
            seen.add(p)
    return ordered


def parse_xml_bytes(data: bytes) -> etree._Element:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=True)
    return etree.fromstring(data, parser=parser)


def collect_tracked_changes(root: etree._Element, part: str) -> List[Dict[str, Any]]:
    # Map paragraphs to indices for context
    paras = root.xpath(".//w:p", namespaces=NS)
    para_index = {p: i for i, p in enumerate(paras)}

    changes: List[Dict[str, Any]] = []

    # Build a single XPath that catches all revision markup we support
    xpath_union = " | ".join(f".//w:{t}" for t in TRACKED_TAGS.keys())
    for elem in root.xpath(xpath_union, namespaces=NS):
        local = etree.QName(elem).localname
        ctype = TRACKED_TAGS.get(local, local)

        cid = get_attr(elem, "w", "id")
        author = get_attr(elem, "w", "author")
        date = parse_dt(get_attr(elem, "w", "date"))
        date_utc = parse_dt(get_attr_any(elem, NS["w16du"], "dateUtc"))

        text = ""
        if ctype in ("ins", "moveTo"):
            text = extract_text_inserted(elem)
        elif ctype in ("del", "moveFrom"):
            text = extract_text_deleted(elem)
        else:
            # Property change: provide a short textual hint (not a full diff)
            text = ""

        # Context paragraph
        p_anc = elem.xpath("ancestor::w:p[1]", namespaces=NS)
        p_el = p_anc[0] if p_anc else None
        if p_el is None:
            # e.g. a paragraph-level deletion wrapper; find first descendant paragraph
            p_desc = elem.xpath(".//w:p[1]", namespaces=NS)
            p_el = p_desc[0] if p_desc else None

        context = paragraph_context(p_el) if p_el is not None else ""
        p_idx = para_index.get(p_el) if p_el is not None else None

        try:
            xpath = elem.getroottree().getpath(elem)
        except Exception:
            xpath = None

        changes.append(
            {
                "type": ctype,
                "id": cid,
                "author": author,
                "date": date,
                "dateUtc": date_utc,
                "text": text,
                "part": part,
                "paragraph_index": p_idx,
                "paragraph_context": context,
                "xpath": xpath,
            }
        )

    return changes


def extract_comment_body(comment_el: etree._Element) -> str:
    # Keep paragraph breaks
    paras: List[str] = []
    for p in comment_el.xpath(".//w:p", namespaces=NS):
        t = extract_text_plain(p).strip()
        if t:
            paras.append(t)
    return "\n".join(paras)


def collect_comments(zf: zipfile.ZipFile) -> List[Dict[str, Any]]:
    names = set(zf.namelist())
    if "word/comments.xml" not in names:
        return []

    comments_root = parse_xml_bytes(zf.read("word/comments.xml"))

    # Optional: modern comments metadata
    done_by_para: Dict[str, bool] = {}
    parent_by_para: Dict[str, str] = {}
    if "word/commentsExtended.xml" in names:
        ext_root = parse_xml_bytes(zf.read("word/commentsExtended.xml"))
        for ce in ext_root.xpath(".//w15:commentEx", namespaces=NS):
            para_id = ce.get(qn("w15", "paraId"))
            if not para_id:
                continue
            done = ce.get(qn("w15", "done"))
            done_by_para[para_id] = done == "1"
            parent = ce.get(qn("w15", "paraIdParent"))
            if parent:
                parent_by_para[para_id] = parent

    # Map comment id -> paraId (first paragraph)
    comments: List[Dict[str, Any]] = []
    comment_id_to_para: Dict[str, str] = {}
    for c in comments_root.xpath(".//w:comment", namespaces=NS):
        cid = get_attr(c, "w", "id")
        author = get_attr(c, "w", "author")
        initials = get_attr(c, "w", "initials")
        date = parse_dt(get_attr(c, "w", "date"))

        first_p = c.xpath(".//w:p[1]", namespaces=NS)
        para_id = None
        if first_p:
            para_id = first_p[0].get(qn("w14", "paraId"))

        if cid is not None and para_id:
            comment_id_to_para[cid] = para_id

        text = extract_comment_body(c)
        comments.append(
            {
                "id": cid,
                "author": author,
                "initials": initials,
                "date": date,
                "paraId": para_id,
                "parentParaId": parent_by_para.get(para_id) if para_id else None,
                "done": done_by_para.get(para_id, False) if para_id else False,
                "text": text,
                "range_text": None,  # filled later from main document
            }
        )

    # Fill range_text from main document, if available
    if "word/document.xml" in names:
        doc_root = parse_xml_bytes(zf.read("word/document.xml"))
        ranges = extract_comment_ranges(doc_root)
        for c in comments:
            cid = c.get("id")
            if cid is None:
                continue
            if cid in ranges:
                c["range_text"] = ranges[cid]

    return comments


def extract_comment_ranges(doc_root: etree._Element, limit: int = 800) -> Dict[str, str]:
    """Return comment-id -> text contained in its comment range (best effort)."""
    active: Set[str] = set()
    chunks: Dict[str, List[str]] = defaultdict(list)

    # Iterate document order
    for elem in doc_root.iter():
        local = etree.QName(elem).localname
        if elem.tag == qn("w", "commentRangeStart"):
            cid = get_attr(elem, "w", "id")
            if cid is not None:
                active.add(cid)
            continue
        if elem.tag == qn("w", "commentRangeEnd"):
            cid = get_attr(elem, "w", "id")
            if cid is not None:
                active.discard(cid)
            continue

        if not active:
            continue

        # Text nodes inside the range
        if elem.tag in (qn("w", "t"), qn("w", "delText")):
            t = elem.text or ""
            if not t:
                continue
            for cid in list(active):
                # Hard cap to avoid exploding output
                if sum(len(x) for x in chunks[cid]) >= limit:
                    continue
                chunks[cid].append(t)

    out: Dict[str, str] = {}
    for cid, parts in chunks.items():
        s = "".join(parts)
        s = " ".join(s.split())
        out[cid] = s[:limit]
    return out


def build_report(docx_path: Path) -> Dict[str, Any]:
    with zipfile.ZipFile(docx_path, "r") as zf:
        parts = find_story_parts(zf)

        tracked: List[Dict[str, Any]] = []
        for part in parts:
            try:
                root = parse_xml_bytes(zf.read(part))
            except KeyError:
                continue
            tracked.extend(collect_tracked_changes(root, part=part))

        comments = collect_comments(zf)

    # Summaries
    counts = defaultdict(int)
    for c in tracked:
        counts[c.get("type") or "unknown"] += 1

    report = {
        "source": str(docx_path),
        "generated_at": iso_now(),
        "summary": {
            "tracked_changes_total": len(tracked),
            "tracked_changes_by_type": dict(sorted(counts.items())),
            "comments_total": len(comments),
        },
        "tracked_changes": tracked,
        "comments": comments,
    }
    return report


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Report existing tracked changes and comments in a .docx")
    ap.add_argument("input", type=Path, help="Input .docx")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Write JSON to this file (default: stdout)")
    ap.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = ap.parse_args(argv)

    if not args.input.exists():
        print(f"error: file not found: {args.input}", file=sys.stderr)
        return 2

    report = build_report(args.input)
    data = json.dumps(report, indent=2 if args.pretty else None, ensure_ascii=False)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
