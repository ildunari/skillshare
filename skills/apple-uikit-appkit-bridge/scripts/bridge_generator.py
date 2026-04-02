#!/usr/bin/env python3
"""
bridge_generator.py
Generate Swift boilerplate for UIKit/AppKit bridges using UIViewRepresentable / NSViewRepresentable.

Usage:
  python bridge_generator.py --platform ios --type UITableView --name MyTableBridge --output ./out
  python bridge_generator.py --platform macos --type NSTableView --name MyTableBridge --output ./out
  python bridge_generator.py --list-templates
"""
import argparse
import os
import sys
from pathlib import Path
from typing import Dict

TEMPLATE_MAP = {
    ("ios", "UITableView"): "templates/uikit/UITableViewBridge.swift.mustache",
    ("ios", "MKMapView"): "templates/uikit/MKMapViewBridge.swift.mustache",
    ("ios", "WKWebView"): "templates/uikit/WKWebViewBridge.swift.mustache",
    ("ios", "Custom"): "templates/uikit/CustomUIKitControl.swift.mustache",
    ("macos", "NSTableView"): "templates/appkit/NSTableViewBridge.swift.mustache",
    ("macos", "Custom"): "templates/appkit/CustomAppKitControl.swift.mustache",
}

def read_template(path: Path) -> str:
    if not path.exists():
        sys.exit(f"[bridge_generator] Template not found: {path}")
    return path.read_text(encoding="utf-8")

def render(template: str, name: str, module: str, extra: Dict[str, str]) -> str:
    # A very small mustache-ish renderer ({{var}} replacement)
    out = template.replace("{{Name}}", name).replace("{{Module}}", module)
    for k, v in extra.items():
        out = out.replace("{{" + k + "}}", v)
    return out

def list_templates():
    print("Available templates:")
    for (platform, typ), path in TEMPLATE_MAP.items():
        print(f" - {platform:5} | {typ:12} -> {path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", choices=["ios", "macos"], required=False, default="ios")
    parser.add_argument("--type", required=False, default="UITableView",
                        help="UIKit/AppKit control type (e.g., UITableView, MKMapView, WKWebView, NSTableView, Custom)")
    parser.add_argument("--name", required=False, default="GeneratedBridge")
    parser.add_argument("--module", required=False, default="SwiftUI")
    parser.add_argument("--output", required=False, default="./out")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list-templates", action="store_true")
    parser.add_argument("--extra", nargs="*", default=[], help="key=value pairs for template variables")
    args = parser.parse_args()

    if args.list_templates:
        list_templates()
        return

    key = (args.platform, args.type)
    if key not in TEMPLATE_MAP:
        print(f"[bridge_generator] Unknown combination {key}. Use --list-templates to inspect.", file=sys.stderr)
        sys.exit(2)

    template_path = Path(TEMPLATE_MAP[key])
    template = read_template(template_path)

    extras: Dict[str, str] = {}
    for pair in args.extra:
        if "=" not in pair:
            print(f"[bridge_generator] Ignoring malformed extra '{pair}', expected key=value.", file=sys.stderr)
            continue
        k, v = pair.split("=", 1)
        extras[k.strip()] = v.strip()

    content = render(template, args.name, args.module, extras)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.name}.swift"

    if args.dry_run:
        print(content)
        return

    out_file.write_text(content, encoding="utf-8")
    print(f"[bridge_generator] Wrote {out_file}")

if __name__ == "__main__":
    main()
