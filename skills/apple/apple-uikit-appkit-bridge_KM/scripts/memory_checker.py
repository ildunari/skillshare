#!/usr/bin/env python3
"""
memory_checker.py
Detect potential retain cycles and lifecycle hazards in bridge code.
Heuristics (best effort):
- Coordinators should hold `weak var parent` or `owner`.
- Capture lists in closures should use [weak self] when self is referenced.
- Representables should clean up in dismantle*.
- Delegates should be nilled in teardown.
"""
import argparse
import re
from pathlib import Path
from typing import List, Tuple

WEAK_PARENT_REGEX = re.compile(r'weak\s+var\s+(parent|owner)\s*:\s*[\w<>\?]+')
COORDINATOR_CLASS_REGEX = re.compile(r'class\s+Coordinator\b')
SELF_CAPTURE_REGEX = re.compile(r'\{\s*\[([^\]]+)\]\s*in')
SELF_USAGE_REGEX = re.compile(r'(?<!\.)\bself\b')
DISMANTLE_REGEX = re.compile(r'static\s+func\s+dismantle(UI|NS)View')
DEINIT_REGEX = re.compile(r'\bdeinit\b')

def scan(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    warnings: List[str] = []

    if COORDINATOR_CLASS_REGEX.search(text):
        if not WEAK_PARENT_REGEX.search(text):
            warnings.append("Coordinator missing `weak var parent/owner` (risk of retain cycle).")

    # Look for closures that reference self without weak/unowned capture
    for m in re.finditer(r'\{[^\}]*\}', text, re.DOTALL):
        block = m.group(0)
        uses_self = bool(SELF_USAGE_REGEX.search(block))
        has_capture = bool(SELF_CAPTURE_REGEX.search(block))
        if uses_self and not has_capture:
            warnings.append("Closure references `self` without capture list (consider [weak self]).")
            break

    if not DISMANTLE_REGEX.search(text):
        warnings.append("No dismantleUIView/dismantleNSView found (remember to cleanup observers/delegates).")

    # Encourage deinit logging for views/coordinators during development
    if "Coordinator" in text and not DEINIT_REGEX.search(text):
        warnings.append("No `deinit` in Coordinator (useful for leak detection during development).")

    return warnings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="*", default=["."])
    args = ap.parse_args()
    files: List[Path] = []
    for t in args.targets:
        p = Path(t)
        if p.is_dir():
            for f in p.rglob("*.swift"):
                files.append(f)
        elif p.suffix == ".swift":
            files.append(p)

    total_warnings: List[Tuple[str, str]] = []
    for f in files:
        ws = scan(f)
        for w in ws:
            total_warnings.append((str(f), w))

    if not total_warnings:
        print("[memory_checker] No obvious issues found.")
        return

    print("=== Potential Memory/Lifecycle Issues ===")
    for path, msg in total_warnings:
        print(f"- {path}: {msg}")
    print("\nTips:\n • Use weak references in coordinators and gesture targets.\n • Cancel Combine subscriptions and remove observers in dismantle*.")

if __name__ == "__main__":
    main()
