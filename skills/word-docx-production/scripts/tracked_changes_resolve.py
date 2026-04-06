#!/usr/bin/env python3
"""scripts/tracked_changes_resolve.py

Accept/reject *existing* tracked changes in a .docx and resolve/delete comments.

Why:
- python-docx does not expose full revision operations.
- This script works at the OOXML level (unzip → edit XML → rezip).

Core operations:
- Accept all / reject all
- Accept/reject subset by author, date range, change id, and change type
- Mark comments as resolved (modern comments) or delete comments + markers

Usage examples:
  # Accept everything
  python scripts/tracked_changes_resolve.py in.docx --accept-all -o out.docx

  # Reject all changes by an author
  python scripts/tracked_changes_resolve.py in.docx --reject --author "Bob" -o out.docx

  # Accept a specific change id
  python scripts/tracked_changes_resolve.py in.docx --accept --id 42 -o out.docx

  # Resolve all comments (requires commentsExtended.xml)
  python scripts/tracked_changes_resolve.py in.docx --resolve-comments -o out.docx

"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
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


def qn(prefix: str, local: str) -> str:
    return f"{{{NS[prefix]}}}{local}"


def parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        if s.endswith("Z"):
            dt = datetime.fromisoformat(s[:-1] + "+00:00")
        else:
            dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def get_attr(elem: etree._Element, prefix: str, local: str) -> Optional[str]:
    return elem.get(qn(prefix, local))


def get_attr_any(elem: etree._Element, ns_uri: str, local: str) -> Optional[str]:
    return elem.get(f"{{{ns_uri}}}{local}")


CHANGE_TAGS = {
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


STORY_PART_PREFIXES = (
    "word/document.xml",
    "word/header",
    "word/footer",
    "word/footnotes.xml",
    "word/endnotes.xml",
)


def is_story_part(name: str) -> bool:
    if name == "word/document.xml":
        return True
    if name.startswith("word/header") and name.endswith(".xml"):
        return True
    if name.startswith("word/footer") and name.endswith(".xml"):
        return True
    if name in ("word/footnotes.xml", "word/endnotes.xml"):
        return True
    return False


def unzip_docx(docx_path: Path, dest_dir: Path) -> None:
    with zipfile.ZipFile(docx_path, "r") as zf:
        zf.extractall(dest_dir)


def zip_dir(src_dir: Path, out_docx: Path) -> None:
    out_docx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_docx, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(src_dir.rglob("*")):
            if p.is_dir():
                continue
            rel = p.relative_to(src_dir).as_posix()
            zf.write(p, rel)


def parse_xml(path: Path) -> etree._ElementTree:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=True)
    return etree.parse(str(path), parser)


def write_xml(tree: etree._ElementTree, path: Path) -> None:
    # Keep formatting as-is as much as possible
    tree.write(str(path), encoding="UTF-8", xml_declaration=True, standalone=None)


def element_depth(e: etree._Element) -> int:
    d = 0
    cur = e
    while cur is not None:
        cur = cur.getparent()
        if cur is not None:
            d += 1
    return d


def _unwrap_element(elem: etree._Element) -> None:
    parent = elem.getparent()
    if parent is None:
        return
    idx = parent.index(elem)
    for child in list(elem):
        parent.insert(idx, child)
        idx += 1
    parent.remove(elem)


def _remove_element(elem: etree._Element) -> None:
    parent = elem.getparent()
    if parent is None:
        return
    parent.remove(elem)


def _convert_deltext_to_text(del_elem: etree._Element) -> None:
    # Convert <w:delText> → <w:t> and <w:delInstrText> → <w:instrText>
    for dt in del_elem.xpath(".//w:delText", namespaces=NS):
        t = etree.Element(qn("w", "t"))
        # Preserve space handling if present
        xml_space = dt.get("{http://www.w3.org/XML/1998/namespace}space")
        if xml_space:
            t.set("{http://www.w3.org/XML/1998/namespace}space", xml_space)
        t.text = dt.text
        dt.getparent().replace(dt, t)
    for dit in del_elem.xpath(".//w:delInstrText", namespaces=NS):
        it = etree.Element(qn("w", "instrText"))
        xml_space = dit.get("{http://www.w3.org/XML/1998/namespace}space")
        if xml_space:
            it.set("{http://www.w3.org/XML/1998/namespace}space", xml_space)
        it.text = dit.text
        dit.getparent().replace(dit, it)


def _reject_del_or_movefrom(elem: etree._Element) -> None:
    _convert_deltext_to_text(elem)
    _unwrap_element(elem)


def _accept_ins_or_moveto(elem: etree._Element) -> None:
    _unwrap_element(elem)


def _reject_ins_or_moveto(elem: etree._Element) -> None:
    _remove_element(elem)


def _accept_del_or_movefrom(elem: etree._Element) -> None:
    _remove_element(elem)


def _accept_property_change(change_elem: etree._Element) -> None:
    # Accepting formatting/property change = keep current properties, remove *Change element.
    _remove_element(change_elem)


def _reject_property_change(change_elem: etree._Element) -> None:
    # Rejecting formatting/property change = restore old properties inside the *Change element.
    parent = change_elem.getparent()
    if parent is None:
        _remove_element(change_elem)
        return

    # Expected structures:
    #   <w:rPr><w:rPrChange> <w:rPr> ...old... </w:rPr> </w:rPrChange></w:rPr>
    #   <w:pPr><w:pPrChange> <w:pPr> ...old... </w:pPr> </w:pPrChange></w:pPr>
    #   <w:sectPr><w:sectPrChange> <w:sectPr> ...old... </w:sectPr> ...</w:sectPrChange></w:sectPr>
    old = None
    for child in change_elem:
        # take first child with matching localname of parent's expected props
        old = child
        break
    if old is None:
        _remove_element(change_elem)
        return

    # Replace parent's children with old's children (deep copy)
    for c in list(parent):
        parent.remove(c)
    for c in list(old):
        parent.append(etree.fromstring(etree.tostring(c)))


def should_match(value: Optional[str], patterns: Optional[List[str]]) -> bool:
    if not patterns:
        return True
    if value is None:
        return False
    v = value.strip().lower()
    return any(v == p.strip().lower() for p in patterns)


def parse_types(types: Optional[List[str]]) -> Optional[Set[str]]:
    if not types:
        return None
    out: Set[str] = set()
    for t in types:
        if not t:
            continue
        t_norm = t.strip()
        # Allow short aliases
        aliases = {
            "rpr": "rPrChange",
            "ppr": "pPrChange",
            "sectpr": "sectPrChange",
            "tblpr": "tblPrChange",
            "trpr": "trPrChange",
            "tcpr": "tcPrChange",
        }
        t_norm = aliases.get(t_norm.lower(), t_norm)
        out.add(t_norm)
    return out


def change_matches(
    elem: etree._Element,
    ctype: str,
    ids: Optional[Set[str]],
    authors: Optional[List[str]],
    since: Optional[datetime],
    until: Optional[datetime],
    types: Optional[Set[str]],
) -> bool:
    if types is not None and ctype not in types:
        return False

    cid = get_attr(elem, "w", "id")
    if ids is not None and (cid is None or cid not in ids):
        return False

    author = get_attr(elem, "w", "author")
    if authors and not should_match(author, authors):
        return False

    # Date filters
    if since or until:
        dt = parse_dt(get_attr(elem, "w", "date"))
        if dt is None:
            dt = parse_dt(get_attr_any(elem, NS["w16du"], "dateUtc"))
        if dt is None:
            return False
        if since and dt < since:
            return False
        if until and dt > until:
            return False

    return True


def process_tracked_changes_in_part(
    xml_path: Path,
    action: Optional[str],
    ids: Optional[Set[str]],
    authors: Optional[List[str]],
    since: Optional[datetime],
    until: Optional[datetime],
    types: Optional[Set[str]],
    stats: Dict[str, int],
) -> None:
    if action not in (None, "accept", "reject"):
        raise ValueError("action must be accept/reject/None")

    tree = parse_xml(xml_path)
    root = tree.getroot()

    xpath_union = " | ".join(f".//w:{t}" for t in CHANGE_TAGS.keys())
    elems: List[Tuple[int, etree._Element, str]] = []
    for e in root.xpath(xpath_union, namespaces=NS):
        local = etree.QName(e).localname
        ctype = CHANGE_TAGS.get(local, local)
        elems.append((element_depth(e), e, ctype))

    # Process inner changes first so nested unwrapping behaves.
    elems.sort(key=lambda x: x[0], reverse=True)

    for _, e, ctype in elems:
        if action is None:
            continue
        if not change_matches(e, ctype, ids=ids, authors=authors, since=since, until=until, types=types):
            continue

        if ctype in ("ins", "moveTo"):
            if action == "accept":
                _accept_ins_or_moveto(e)
            else:
                _reject_ins_or_moveto(e)
            stats[f"{action}_{ctype}"] += 1
            continue

        if ctype in ("del", "moveFrom"):
            if action == "accept":
                _accept_del_or_movefrom(e)
            else:
                _reject_del_or_movefrom(e)
            stats[f"{action}_{ctype}"] += 1
            continue

        # Property changes
        if action == "accept":
            _accept_property_change(e)
        else:
            _reject_property_change(e)
        stats[f"{action}_{ctype}"] += 1

    write_xml(tree, xml_path)


def build_comment_index(parts_dir: Path) -> Tuple[Dict[str, etree._Element], Dict[str, Dict[str, Any]]]:
    """Return (comments_by_id, meta_by_id).

    meta contains: id, author, date(dt), initials, paraId
    """
    comments_path = parts_dir / "word" / "comments.xml"
    if not comments_path.exists():
        return {}, {}

    tree = parse_xml(comments_path)
    root = tree.getroot()

    by_id: Dict[str, etree._Element] = {}
    meta: Dict[str, Dict[str, Any]] = {}
    for c in root.xpath(".//w:comment", namespaces=NS):
        cid = get_attr(c, "w", "id")
        if cid is None:
            continue
        by_id[cid] = c
        author = get_attr(c, "w", "author")
        initials = get_attr(c, "w", "initials")
        date = parse_dt(get_attr(c, "w", "date"))
        para_id = None
        first_p = c.xpath(".//w:p[1]", namespaces=NS)
        if first_p:
            para_id = first_p[0].get(qn("w14", "paraId"))
        meta[cid] = {
            "id": cid,
            "author": author,
            "initials": initials,
            "date": date,
            "paraId": para_id,
        }

    # keep tree alive by attaching to meta
    meta["__tree__"] = {"tree": tree, "path": comments_path}
    return by_id, meta


def comment_matches(
    meta: Dict[str, Any],
    ids: Optional[Set[str]],
    authors: Optional[List[str]],
    since: Optional[datetime],
    until: Optional[datetime],
) -> bool:
    cid = meta.get("id")
    if ids is not None and (cid is None or cid not in ids):
        return False
    if authors and not should_match(meta.get("author"), authors):
        return False
    if since or until:
        dt = meta.get("date")
        if not isinstance(dt, datetime):
            return False
        if since and dt < since:
            return False
        if until and dt > until:
            return False
    return True


def resolve_comments(parts_dir: Path, comment_ids: Set[str], stats: Dict[str, int]) -> None:
    """Mark comments as done by setting w15:done="1" in commentsExtended.xml.

    If commentsExtended.xml doesn't exist, we leave comments untouched (best-effort).
    """
    ext_path = parts_dir / "word" / "commentsExtended.xml"
    if not ext_path.exists():
        stats["resolve_comments_missing_commentsExtended"] += len(comment_ids)
        return

    # Need mapping from comment id -> paraId
    _, meta = build_comment_index(parts_dir)
    meta_tree = meta.get("__tree__")
    if not meta_tree:
        return

    id_to_para = {cid: m.get("paraId") for cid, m in meta.items() if cid != "__tree__"}

    tree = parse_xml(ext_path)
    root = tree.getroot()
    changed = 0
    for cid in comment_ids:
        para_id = id_to_para.get(cid)
        if not para_id:
            continue
        for ce in root.xpath(".//w15:commentEx", namespaces=NS):
            if ce.get(qn("w15", "paraId")) == para_id:
                ce.set(qn("w15", "done"), "1")
                changed += 1
                break

    if changed:
        write_xml(tree, ext_path)
    stats["resolve_comments_marked_done"] += changed


def delete_comments(parts_dir: Path, comment_ids: Set[str], stats: Dict[str, int]) -> None:
    """Delete comments and strip their range markers from story parts."""
    comments_path = parts_dir / "word" / "comments.xml"
    if not comments_path.exists():
        return

    # Load comments.xml
    c_tree = parse_xml(comments_path)
    c_root = c_tree.getroot()

    removed = 0
    for c in list(c_root.xpath(".//w:comment", namespaces=NS)):
        cid = get_attr(c, "w", "id")
        if cid in comment_ids:
            c_root.remove(c)
            removed += 1

    if removed:
        write_xml(c_tree, comments_path)
    stats["delete_comments_removed"] += removed

    # Remove markers in story parts
    word_dir = parts_dir / "word"
    for xml in word_dir.rglob("*.xml"):
        rel = xml.relative_to(parts_dir).as_posix()
        if not is_story_part(rel):
            continue
        tree = parse_xml(xml)
        root = tree.getroot()
        removed_markers = 0
        # These are empty elements; removing them is safe.
        for tag in ("commentRangeStart", "commentRangeEnd", "commentReference"):
            for el in list(root.xpath(f".//w:{tag}", namespaces=NS)):
                cid = get_attr(el, "w", "id")
                if cid in comment_ids:
                    parent = el.getparent()
                    if parent is not None:
                        parent.remove(el)
                        removed_markers += 1
        if removed_markers:
            write_xml(tree, xml)
        stats["delete_comment_markers_removed"] += removed_markers

    # Best-effort cleanup of modern comment metadata parts (if present)
    for extra in ("commentsExtended.xml", "commentsIds.xml", "commentsExtensible.xml"):
        p = word_dir / extra
        if not p.exists():
            continue
        # Can't reliably map durableId without full thread model; keep the parts unless we can map.
        # For commentsExtended.xml and commentsIds.xml we *can* map via paraId.
        if extra in ("commentsExtended.xml", "commentsIds.xml"):
            _, meta = build_comment_index(parts_dir)
            id_to_para = {cid: m.get("paraId") for cid, m in meta.items() if cid != "__tree__"}
            para_ids = {id_to_para.get(cid) for cid in comment_ids if id_to_para.get(cid)}

            tree = parse_xml(p)
            root = tree.getroot()
            removed_extra = 0
            if extra == "commentsExtended.xml":
                for ce in list(root.xpath(".//w15:commentEx", namespaces=NS)):
                    if ce.get(qn("w15", "paraId")) in para_ids:
                        ce.getparent().remove(ce)
                        removed_extra += 1
            else:  # commentsIds.xml
                # structure: <w15:commentIds><w15:commentId w15:paraId=".." .../></...>
                for ci in list(root.xpath(".//w15:commentId", namespaces=NS)):
                    if ci.get(qn("w15", "paraId")) in para_ids:
                        ci.getparent().remove(ci)
                        removed_extra += 1
            if removed_extra:
                write_xml(tree, p)
            stats[f"delete_comments_{extra}_entries_removed"] += removed_extra


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Accept/reject tracked changes and resolve/delete comments in a DOCX")
    ap.add_argument("input", type=Path, help="Input .docx")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Output .docx (default: <input>_resolved.docx)")

    g = ap.add_mutually_exclusive_group()
    g.add_argument("--accept-all", action="store_true", help="Accept all tracked changes")
    g.add_argument("--reject-all", action="store_true", help="Reject all tracked changes")
    g.add_argument("--accept", action="store_true", help="Accept tracked changes matching filters")
    g.add_argument("--reject", action="store_true", help="Reject tracked changes matching filters")

    ap.add_argument("--id", action="append", default=None, help="Tracked change id (w:id); repeatable")
    ap.add_argument("--author", action="append", default=None, help="Tracked change author; repeatable")
    ap.add_argument("--since", default=None, help="Only changes/comments on/after this UTC timestamp (ISO 8601)")
    ap.add_argument("--until", default=None, help="Only changes/comments on/before this UTC timestamp (ISO 8601)")
    ap.add_argument(
        "--type",
        dest="types",
        action="append",
        default=None,
        help="Change type: ins, del, moveTo, moveFrom, rPrChange, pPrChange, sectPrChange, tblPrChange, trPrChange, tcPrChange (repeatable)",
    )

    cg = ap.add_mutually_exclusive_group()
    cg.add_argument("--resolve-comments", action="store_true", help="Mark comments as resolved (modern comments)")
    cg.add_argument("--delete-comments", action="store_true", help="Delete comments + range markers")

    ap.add_argument("--comment-id", action="append", default=None, help="Comment id; repeatable")
    ap.add_argument("--comment-author", action="append", default=None, help="Comment author; repeatable")
    ap.add_argument("--report", type=Path, default=None, help="Write a JSON summary report here")

    args = ap.parse_args(argv)

    if not args.input.exists():
        print(f"error: file not found: {args.input}", file=sys.stderr)
        return 2

    out_path = args.output
    if out_path is None:
        out_path = args.input.with_name(args.input.stem + "_resolved.docx")

    # Determine action
    action: Optional[str] = None
    if args.accept_all:
        action = "accept"
    elif args.reject_all:
        action = "reject"
    elif args.accept:
        action = "accept"
    elif args.reject:
        action = "reject"

    # Filters
    ids = set(args.id) if args.id else None
    types = parse_types(args.types)

    since = parse_dt(args.since) if args.since else None
    until = parse_dt(args.until) if args.until else None

    # Comment filters
    c_ids = set(args.comment_id) if args.comment_id else None
    c_authors = args.comment_author if args.comment_author else None

    stats: Dict[str, int] = defaultdict(int)

    with tempfile.TemporaryDirectory(prefix="docx_resolve_") as td:
        td_path = Path(td)
        unzip_docx(args.input, td_path)

        # Process tracked changes
        if action is not None:
            word_dir = td_path / "word"
            for xml_path in word_dir.rglob("*.xml"):
                rel = xml_path.relative_to(td_path).as_posix()
                if not is_story_part(rel):
                    continue
                process_tracked_changes_in_part(
                    xml_path,
                    action=action,
                    ids=None if (args.accept_all or args.reject_all) else ids,
                    authors=None if (args.accept_all or args.reject_all) else args.author,
                    since=None if (args.accept_all or args.reject_all) else since,
                    until=None if (args.accept_all or args.reject_all) else until,
                    types=None if (args.accept_all or args.reject_all) else types,
                    stats=stats,
                )

        # Process comments
        if args.resolve_comments or args.delete_comments:
            _, meta = build_comment_index(td_path)
            comment_ids: Set[str] = set()
            for cid, m in meta.items():
                if cid == "__tree__":
                    continue
                if comment_matches(m, ids=c_ids, authors=c_authors, since=since, until=until):
                    comment_ids.add(cid)

            if args.resolve_comments:
                resolve_comments(td_path, comment_ids, stats=stats)
            elif args.delete_comments:
                delete_comments(td_path, comment_ids, stats=stats)

        zip_dir(td_path, out_path)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        import json

        args.report.write_text(json.dumps({"input": str(args.input), "output": str(out_path), "stats": dict(stats)}, indent=2), encoding="utf-8")

    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
