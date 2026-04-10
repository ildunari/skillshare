#!/usr/bin/env python3
"""
concurrency_analyzer.py — Swift concurrency heuristic scanner.
"""
import re, os, sys, json, argparse
from pathlib import Path

TASK_PATTERN = re.compile(r'\bTask\s*\{|\bDetachedTask\s*\{')
CANCEL_CHECK_PATTERN = re.compile(r'\bTask\.(isCancelled|checkCancellation)\b|\btry\s+await\s+Task\.sleep')
MAINACTOR_ANNOT = re.compile(r'@MainActor\b')
UI_KNOWN_TYPES = re.compile(r'\b(UIViewController|NSViewController|View\b|App\b|UIApplication|NSApplication)\b')
GLOBAL_VAR = re.compile(r'^\s*(public|internal|fileprivate|private)?\s*var\s+\w+\s*[:=]', re.M)
NON_SENDABLE_CAPTURE = re.compile(r'@Sendable\s*\([^\)]*self[^\)]*\)')
GCD_PATTERN = re.compile(r'DispatchQueue\.(main|global|label)')

def analyze_file(p: Path):
    text = p.read_text(encoding='utf-8', errors='ignore')
    findings = []

    for m in TASK_PATTERN.finditer(text):
        window = text[max(0, m.start()-200):m.end()+300]
        if not CANCEL_CHECK_PATTERN.search(window):
            findings.append({"kind": "unstructured_task_no_cancellation",
                             "line": text.count("\\n", 0, m.start()) + 1,
                             "message": "Unstructured Task/DetachedTask without nearby cancellation checks."})

    if UI_KNOWN_TYPES.search(text) and not MAINACTOR_ANNOT.search(text):
        findings.append({"kind": "ui_without_mainactor", "line": 1,
                         "message": "UI types present without @MainActor annotation."})

    for m in GLOBAL_VAR.finditer(text):
        findings.append({"kind": "global_var_mutable",
                         "line": text.count("\\n", 0, m.start()) + 1,
                         "message": "Top-level mutable global detected; prefer actor/value isolation."})

    for m in NON_SENDABLE_CAPTURE.finditer(text):
        findings.append({"kind": "sendable_captures_self",
                         "line": text.count("\\n", 0, m.start()) + 1,
                         "message": "@Sendable closure appears to capture 'self'."})

    for m in GCD_PATTERN.finditer(text):
        findings.append({"kind": "gcd_usage",
                         "line": text.count("\\n", 0, m.start()) + 1,
                         "message": "GCD usage detected; prefer structured concurrency."})
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="Swift file(s) or directories")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    all_findings = []
    for raw in args.paths:
        p = Path(raw)
        files = [p] if p.is_file() else list(p.rglob("*.swift"))
        for f in files:
            res = analyze_file(f)
            if res:
                all_findings.append({"file": str(f), "findings": res})

    if args.json:
        print(json.dumps(all_findings, indent=2))
    else:
        if not all_findings:
            print("No findings.")
        for entry in all_findings:
            print(f"\\n== {entry['file']} ==")
            for f in entry["findings"]:
                print(f"  L{f['line']}: {f['kind']}: {f['message']}")

if __name__ == "__main__":
    main()
