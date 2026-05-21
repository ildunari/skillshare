#!/usr/bin/env python3
"""
memory_leak_detector.py — Heuristics for ARC retain cycles and lifetime hazards.
"""
import re, os, sys, json, argparse
from pathlib import Path

DELEGATE_STRONG = re.compile(r'(?<!weak\s)var\s+delegate\s*:\s*[A-Z]\w+\??')
CLOSURE_SELF = re.compile(r'\{[^\}]*\bself\b[^\}]*\}')
WEAK_CAPTURE = re.compile(r'\[\s*weak\s+self\s*\]')
NOTIF_ADD = re.compile(r'NotificationCenter\.default\.addObserver')
DEINIT = re.compile(r'\bdeinit\b')
TASK_UNSTRUCTURED = re.compile(r'\bTask\s*\{')

def analyze(text: str):
    out = []
    for m in DELEGATE_STRONG.finditer(text):
        out.append({"kind": "delegate_not_weak", "line": text.count("\\n", 0, m.start()) + 1,
                    "message": "Delegate is not weak; may retain cycles."})
    for m in CLOSURE_SELF.finditer(text):
        window = text[max(0, m.start()-40):m.start()+1]
        if not WEAK_CAPTURE.search(window):
            out.append({"kind": "closure_captures_self", "line": text.count("\\n", 0, m.start()) + 1,
                        "message": "Closure captures self without [weak self]."})
    if NOTIF_ADD.search(text) and not DEINIT.search(text):
        out.append({"kind": "notification_no_deinit", "line": 1,
                    "message": "Adds NotificationCenter observer with no deinit to remove."})
    if TASK_UNSTRUCTURED.search(text):
        out.append({"kind": "unstructured_task", "line": 1,
                    "message": "Unstructured Task present; ensure cancellation and lifetime are handled."})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    results = []
    from pathlib import Path
    for raw in args.paths:
        p = Path(raw)
        files = [p] if p.is_file() else list(p.rglob("*.swift"))
        for f in files:
            res = analyze(f.read_text(encoding='utf-8', errors='ignore'))
            if res:
                results.append({"file": str(f), "findings": res})

    if args.json:
        import json; print(json.dumps(results, indent=2))
    else:
        if not results: print("No memory issues detected.")
        for entry in results:
            print(f"\\n== {entry['file']} ==")
            for f in entry["findings"]:
                print(f"  L{f['line']}: {f['kind']}: {f['message']}")

if __name__ == "__main__":
    main()
