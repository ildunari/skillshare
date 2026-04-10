#!/usr/bin/env python3
"""
modernization_suggester.py — Suggests upgrades to modern Swift.
"""
import re, os, sys, json, argparse
from pathlib import Path

COMPLETION_FUNC = re.compile(r'func\s+\w+\s*\([^)]*completion:\s*@?escaping', re.S)
URLSESSION_COMPLETION = re.compile(r'URLSession\.shared\.dataTask\(.*completionHandler:', re.S)
DISPATCH_GROUP = re.compile(r'DispatchGroup\(')
DISPATCH_QUEUE = re.compile(r'DispatchQueue\.(main|global|label)')
ANY_EXISTENTIAL = re.compile(r':\s*any\s+[A-Z]\w+')

def suggest(text: str):
    out = []
    if COMPLETION_FUNC.search(text) or URLSESSION_COMPLETION.search(text):
        out.append({"kind": "callbacks_to_async",
                    "message": "Completion-handler APIs detected. Consider 'async throws' and 'await'."})
    if DISPATCH_GROUP.search(text):
        out.append({"kind": "dispatch_group",
                    "message": "DispatchGroup usage detected. Prefer 'with(Throwing)TaskGroup'."})
    if DISPATCH_QUEUE.search(text):
        out.append({"kind": "dispatch_queue",
                    "message": "DispatchQueue usage detected. Prefer actors/@MainActor + Task APIs."})
    if ANY_EXISTENTIAL.search(text):
        out.append({"kind": "existential_any",
                    "message": "Use of 'any Protocol' detected. Prefer generics or 'some' when specialization matters."})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    results = []
    for raw in args.paths:
        p = Path(raw)
        files = [p] if p.is_file() else list(p.rglob("*.swift"))
        for f in files:
            s = suggest(f.read_text(encoding='utf-8', errors='ignore'))
            if s:
                results.append({"file": str(f), "suggestions": s})

    if args.json:
        import json; print(json.dumps(results, indent=2))
    else:
        if not results: print("No modernization suggestions.")
        for entry in results:
            print(f"\\n== {entry['file']} ==")
            for s in entry["suggestions"]:
                print(f"- {s['kind']}: {s['message']}")

if __name__ == "__main__":
    main()
