#!/usr/bin/env python3
"""
component_inventory.py

Creates a lightweight inventory of UI components by scanning common patterns in:
- React (.jsx/.tsx)
- Vue (.vue)
- Svelte (.svelte)

It won't be perfect (no AST), but it's fast and helpful during audits.

Usage:
  python scripts/component_inventory.py --root src --out inventory.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple


EXTS = {".tsx", ".jsx", ".vue", ".svelte"}


REACT_EXPORT_FN = re.compile(r"export\s+function\s+([A-Z][A-Za-z0-9_]*)\s*\(")
REACT_EXPORT_DEFAULT_FN = re.compile(r"export\s+default\s+function\s+([A-Z][A-Za-z0-9_]*)\s*\(")
REACT_CONST_COMP = re.compile(r"(?:export\s+)?const\s+([A-Z][A-Za-z0-9_]*)\s*=\s*\(")

VUE_NAME = re.compile(r"name:\s*['\"]([^'\"]+)['\"]")
SVELTE_NAME = re.compile(r"<svelte:options\s+tag=['\"]([^'\"]+)['\"]")


def iter_files(root: Path, max_files: int) -> List[Path]:
    out: List[Path] = []
    for p in root.rglob("*"):
        if len(out) >= max_files:
            break
        if p.is_file() and p.suffix.lower() in EXTS:
            out.append(p)
    return out


def scan_file(fp: Path) -> List[str]:
    names: List[str] = []
    text = fp.read_text(encoding="utf-8", errors="ignore")

    if fp.suffix.lower() in {".tsx", ".jsx"}:
        names += REACT_EXPORT_DEFAULT_FN.findall(text)
        names += REACT_EXPORT_FN.findall(text)
        names += REACT_CONST_COMP.findall(text)

    elif fp.suffix.lower() == ".vue":
        m = VUE_NAME.search(text)
        if m:
            names.append(m.group(1))
        else:
            names.append(fp.stem)

    elif fp.suffix.lower() == ".svelte":
        m = SVELTE_NAME.search(text)
        names.append(m.group(1) if m else fp.stem)

    # Deduplicate while preserving order
    seen = set()
    uniq: List[str] = []
    for n in names:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Directory to scan")
    ap.add_argument("--max-files", type=int, default=1200)
    ap.add_argument("--out", default="", help="Optional output markdown file")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    files = iter_files(root, args.max_files)

    rows: List[Tuple[str, str]] = []
    for fp in files:
        names = scan_file(fp)
        for n in names:
            rows.append((n, str(fp.relative_to(root))))

    rows.sort(key=lambda x: (x[0].lower(), x[1].lower()))

    md = []
    md.append("# UI Component Inventory\n")
    md.append(f"- Root: `{root}`")
    md.append(f"- Files scanned (max): {args.max_files}")
    md.append(f"- Components found: {len(rows)}\n")
    md.append("| Component | File |")
    md.append("|---|---|")
    for name, rel in rows:
        md.append(f"| `{name}` | `{rel}` |")
    md.append("")

    out_md = "\n".join(md)

    if args.out:
        Path(args.out).write_text(out_md, encoding="utf-8")
        print(f"Wrote: {args.out}")
    else:
        print(out_md)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
