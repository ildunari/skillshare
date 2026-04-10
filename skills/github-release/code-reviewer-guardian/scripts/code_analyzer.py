#!/usr/bin/env python3
"""
code_analyzer.py
-----------------
Custom static analysis for Swift projects beyond SwiftLint.

Features:
- Flags TODO/FIXME
- Detects debug prints in production code
- Detects force unwrap/try/cast
- Detects DispatchQueue.main.sync usage
- Finds large files and long functions (naive)
- Emits JSON with severity and suggested fixes

Usage:
  python code_analyzer.py --path . --out findings.json
"""

import argparse, json, os, re
from typing import List, Dict, Any, Tuple

FORCE_PATTERNS = [
    (re.compile(r"\btry!\b"), "Avoid try!; handle or propagate errors."),
    (re.compile(r"\bas!\b"), "Avoid force cast 'as!'; use safe cast or redesign API."),
    (re.compile(r"!\s*(?:\.|\)|,|\}|\]|$)"), "Avoid force unwrap '!' in production code."),
]

DEBUG_PATTERN = re.compile(r"\bprint\s*\(")
MAIN_SYNC_PATTERN = re.compile(r"DispatchQueue\.main\.sync\b")
TODO_PATTERN = re.compile(r"\b(?:TODO|FIXME|XXX)\b")
FUNC_DEF_PATTERN = re.compile(r"^\s*(?:@\w+\s+)*func\s+\w+\s*\(.*\)\s*(?:->\s*[^\{]+)?\{\s*$")


def list_swift_files(root: str) -> List[str]:
    files = []
    for r, _, fs in os.walk(root):
        if any(part in r for part in ("Pods/", ".build/", "DerivedData/", "Carthage/", "vendor/", "Generated/")):
            continue
        for f in fs:
            if f.endswith(".swift"):
                files.append(os.path.join(r, f))
    return files


def split_functions(lines: List[str]) -> List[Tuple[int, int]]:
    """Very naive function boundary detection by counting braces after 'func' lines."""
    spans = []
    i = 0
    n = len(lines)
    while i < n:
        if FUNC_DEF_PATTERN.match(lines[i]):
            depth = 0
            start = i
            # include this line and iterate until balanced
            j = i
            opened = 0
            closed = 0
            while j < n:
                opened += lines[j].count('{')
                closed += lines[j].count('}')
                if opened > 0 and opened == closed:
                    spans.append((start, j))
                    i = j
                    break
                j += 1
        i += 1
    return spans


def analyze_file(path: str) -> List[Dict[str, Any]]:
    findings = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return [{"file": path, "line": 0, "severity": "P1", "rule": "read_error", "message": str(e)}]

    lines = content.splitlines()
    # Size-related
    if len(lines) > 800:
        findings.append({"file": path, "line": 1, "severity": "P2", "rule": "file_length", "message": f"Large file ({len(lines)} lines). Consider splitting."})

    # Generic regex rules
    for i, line in enumerate(lines, 1):
        if DEBUG_PATTERN.search(line) and not ("TEST" in path or "/Tests/" in path):
            findings.append({"file": path, "line": i, "severity": "P2", "rule": "debug_print", "message": "Avoid print() in production code; use logging abstraction with levels."})
        if MAIN_SYNC_PATTERN.search(line):
            findings.append({"file": path, "line": i, "severity": "P1", "rule": "main_thread_sync", "message": "Avoid DispatchQueue.main.sync; may deadlock. Use async or MainActor."})
        if TODO_PATTERN.search(line):
            findings.append({"file": path, "line": i, "severity": "P3", "rule": "todo_comment", "message": "TODO/FIXME left in code; convert to tracked issue with owner/date."})
        for rx, tip in FORCE_PATTERNS:
            if rx.search(line):
                findings.append({"file": path, "line": i, "severity": "P1", "rule": "force_operation", "message": tip})

    # Naive long function detection
    spans = split_functions(lines)
    for (start, end) in spans:
        length = end - start + 1
        if length > 80:
            findings.append({"file": path, "line": start + 1, "severity": "P2", "rule": "long_function", "message": f"Function is {length} lines; consider Extract Method/Type."})

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".")
    ap.add_argument("--out", default="findings.json")
    args = ap.parse_args()

    files = list_swift_files(args.path)
    results: List[Dict[str, Any]] = []
    for fp in files:
        results.extend(analyze_file(fp))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"findings": results}, f, indent=2)
    print(f"Wrote {len(results)} findings to {args.out}")


if __name__ == "__main__":
    main()
