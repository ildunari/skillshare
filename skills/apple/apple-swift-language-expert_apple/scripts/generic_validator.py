#!/usr/bin/env python3
"""
generic_validator.py — Lints for generics/existentials/opaque types.
"""
import re, os, sys, json, argparse
from pathlib import Path

PROTO_ASSOC = re.compile(r'protocol\s+([A-Z]\w+)\s*\{[^}]*\bassociatedtype\b', re.S)
SELF_REQ = re.compile(r'protocol\s+([A-Z]\w+)\s*\{[^}]*\bSelf\b', re.S)
ANY_USE = re.compile(r':\s*any\s+([A-Z]\w+)')
SOME_RETURN = re.compile(r'->\s*some\s+([A-Z]\w+)')

def parse_protocols(text: str):
    s = set()
    for m in PROTO_ASSOC.finditer(text): s.add(m.group(1))
    for m in SELF_REQ.finditer(text): s.add(m.group(1))
    return s

def validate(text: str):
    assoc = parse_protocols(text)
    out = []
    for m in ANY_USE.finditer(text):
        if m.group(1) in assoc:
            out.append({"kind": "existential_with_associatedtype",
                        "line": text.count("\\n", 0, m.start()) + 1,
                        "message": f"'any {m.group(1)}' used where associated types/Self likely prevent existential use."})
    for m in SOME_RETURN.finditer(text):
        out.append({"kind": "opaque_return_detected",
                    "line": text.count("\\n", 0, m.start()) + 1,
                    "message": f"Function returns 'some {m.group(1)}' (opaque)."})
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
            findings = validate(f.read_text(encoding='utf-8', errors='ignore'))
            if findings:
                results.append({"file": str(f), "findings": findings})

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if not results: print("No generic/existential issues detected.")
        for entry in results:
            print(f"\\n== {entry['file']} ==")
            for f in entry["findings"]:
                print(f"  L{f['line']}: {f['kind']}: {f['message']}")

if __name__ == "__main__":
    main()
