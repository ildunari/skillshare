#!/usr/bin/env python3
"""
Track sources and generate citations.

- Stores citations in JSONL or CSV.
- De-duplicates by URL hash.
- Exports Markdown bibliography.

Usage:
    python scripts/citation_tracker.py add --title "..." --url "..." --author "..." --tags swift,ios
    python scripts/citation_tracker.py export --format md --out ./out/refs.md
"""
import argparse
import os
import json
import csv
import hashlib
from typing import Dict, Any, List
from datetime import datetime
from tools.utils import ensure_out

STORE = os.environ.get("RDA_CITATIONS", "./out/citations.jsonl")

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def add_entry(entry: Dict[str, Any]) -> None:
    ensure_out(os.path.dirname(STORE) or "./out")
    seen = set()
    if os.path.exists(STORE):
        with open(STORE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    seen.add(obj.get("id"))
                except Exception:
                    continue
    eid = sha1(entry["url"])
    if eid in seen:
        return
    entry["id"] = eid
    entry.setdefault("accessed_at", datetime.utcnow().isoformat() + "Z")
    with open(STORE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def export_markdown(out_path: str) -> None:
    items: List[Dict[str, Any]] = []
    if os.path.exists(STORE):
        with open(STORE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    items.append(json.loads(line))
                except Exception:
                    continue
    ensure_out(os.path.dirname(out_path) or "./out")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Bibliography\n\n")
        for it in items:
            f.write(f"- {it.get('title')} — {it.get('url')} ({it.get('accessed_at')})\n")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    addp = sub.add_parser("add")
    addp.add_argument("--title", required=True)
    addp.add_argument("--url", required=True)
    addp.add_argument("--author", default="")
    addp.add_argument("--tags", default="")
    addp.add_argument("--note", default="")
    exp = sub.add_parser("export")
    exp.add_argument("--format", choices=["md"], default="md")
    exp.add_argument("--out", default="./out/refs.md")
    args = ap.parse_args()

    if args.cmd == "add":
        add_entry({"title": args.title, "url": args.url, "author": args.author, "tags": args.tags.split(","), "note": args.note})
        print("Added.")
    elif args.cmd == "export":
        if args.format == "md":
            export_markdown(args.out)
            print(f"Wrote {args.out}")
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
