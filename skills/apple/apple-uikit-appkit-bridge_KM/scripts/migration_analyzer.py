#!/usr/bin/env python3
"""
migration_analyzer.py
Scan a UIKit/AppKit codebase and suggest migration paths to SwiftUI.

Heuristics:
- Detect UIViewController/NSViewController-heavy modules → propose UI/NSHostingController embedding.
- Detect common controls (UITableView/NSTableView/WKWebView/MKMapView) → suggest Representable wrappers.
- Flag storyboards/xibs → recommend extraction of views into SwiftUI and layout simplification.
- Summarize delegate/data source usage that could move into Coordinator.
"""
import argparse
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

CONTROL_MAP = {
    "UITableView": "UIViewRepresentable wrapper + Coordinator as delegate/dataSource (diffable preferred)",
    "UICollectionView": "UIViewRepresentable or rewrite to SwiftUI/List/ScrollView if simple",
    "WKWebView": "UIViewRepresentable with navigation delegate and KVO progress",
    "MKMapView": "UIViewRepresentable with MKMapViewDelegate and region binding",
    "NSTableView": "NSViewRepresentable with dataSource/delegate, consider DiffableDataSource on macOS 11+",
    "NSCollectionView": "NSViewRepresentable or SwiftUI grid APIs if feasible",
}

VC_REGEX = re.compile(r'\b(UI|NS)ViewController\b')
SB_REGEX = re.compile(r'\.(storyboard|xib)\b', re.IGNORECASE)

def scan_files(paths: List[Path]) -> List[Path]:
    files = []
    for p in paths:
        if p.is_dir():
            for root, _, names in os.walk(p):
                for n in names:
                    if n.endswith((".swift", ".m", ".mm", ".xib", ".storyboard")):
                        files.append(Path(root) / n)
        else:
            files.append(p)
    return files

def analyze_file(path: Path) -> Dict[str, List[Tuple[str, int]]]:
    findings: Dict[str, List[Tuple[str, int]]] = {"controllers": [], "controls": [], "storyboards": []}
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    if VC_REGEX.search(text):
        findings["controllers"].append((str(path), len(VC_REGEX.findall(text))))
    for control in CONTROL_MAP.keys():
        count = len(re.findall(r'\b' + re.escape(control) + r'\b', text))
        if count:
            findings["controls"].append((f"{control} in {path}", count))
    if SB_REGEX.search(path.suffix):
        findings["storyboards"].append((str(path), 1))
    return findings

def summarize(findings_list: List[Dict[str, List[Tuple[str, int]]]]) -> Dict[str, List[Tuple[str, int]]]:
    summary: Dict[str, List[Tuple[str, int]]] = {"controllers": [], "controls": [], "storyboards": []}
    for f in findings_list:
        for k in summary:
            summary[k].extend(f[k])
    return summary

def suggestions(summary: Dict[str, List[Tuple[str, int]]]) -> str:
    lines: List[str] = []
    if summary["controllers"]:
        lines.append("• Consider embedding SwiftUI via UIHostingController / NSHostingController in these modules:")
        for path, _ in summary["controllers"][:10]:
            lines.append(f"  - {path}")
    if summary["controls"]:
        lines.append("• Detected legacy controls and suggested bridges:")
        for item, count in summary["controls"]:
            control = item.split()[0]
            lines.append(f"  - {item} (x{count}): {CONTROL_MAP.get(control, 'Representable wrapper')}")
    if summary["storyboards"]:
        lines.append("• Storyboards/XIBs present → opportunity to migrate layouts to SwiftUI where possible.")
    if not lines:
        lines.append("No obvious migration hotspots found. Consider starting with hosting controllers for leaf screens.")
    lines.append("\nNext steps:\n  1) Generate wrappers with scripts/bridge_generator.py\n  2) Move delegates/datasources into Coordinator\n  3) Add unit/UI tests using templates/testing")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="*", help="Files or directories to analyze", default=["."])
    args = parser.parse_args()
    paths = [Path(t) for t in args.targets]
    files = scan_files(paths)
    results = [analyze_file(f) for f in files]
    summary = summarize(results)
    print("=== Migration Analyzer Report ===\n")
    print(f"Scanned {len(files)} files.\n")
    print(suggestions(summary))

if __name__ == "__main__":
    main()
