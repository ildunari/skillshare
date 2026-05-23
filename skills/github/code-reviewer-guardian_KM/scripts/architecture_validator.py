#!/usr/bin/env python3
"""
architecture_validator.py
-------------------------
Validate basic architectural boundaries by scanning imports, file paths, and
common anti-patterns (UI layer doing networking/persistence).

Convention expected (customize via args if desired):
- Presentation/UI: Sources/UI/, SwiftUI/, UIKit/
- Domain: Sources/Domain/
- Data/Infrastructure: Sources/Data/, Sources/Infrastructure/

Rules:
- UI files should not import CoreData/URLSession directly for business operations.
- Domain should not import UIKit/SwiftUI.
- Data layer should not import SwiftUI/UIKit.

Usage:
  python architecture_validator.py --path . --out arch.json
"""
import argparse, os, re, json
from typing import List, Dict

IMPORT_RX = re.compile(r"^\s*import\s+(\w+)\b")
FUNC_DEF = re.compile(r"\bfunc\s+\w+\s*\(")

UI_KITS = {"UIKit", "SwiftUI"}
DATA_KITS = {"CoreData"}
NET_APIS = {"URLSession"}

def list_swift(root: str) -> List[str]:
    out=[]
    for r,_,fs in os.walk(root):
        if any(p in r for p in ("Pods/", ".build/", "DerivedData/", "Carthage/", "vendor/", "Generated/")):
            continue
        for f in fs:
            if f.endswith('.swift'):
                out.append(os.path.join(r,f))
    return out

def layer_for(path: str) -> str:
    p = path.replace('\\','/')
    if any(seg in p for seg in ("/UI/", "SwiftUI/", "/Presentation/", "/Features/")):
        return "ui"
    if "/Domain/" in p:
        return "domain"
    if any(seg in p for seg in ("/Data/", "/Infrastructure/", "/Persistence/")):
        return "data"
    return "unknown"

def analyze_file(path: str) -> List[Dict]:
    out=[]
    layer = layer_for(path)
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            lines=f.read().splitlines()
    except Exception as e:
        return [{"file": path, "line":0, "severity":"P1","rule":"read_error","message":str(e)}]

    imports=set()
    for ln in lines:
        m = IMPORT_RX.match(ln)
        if m: imports.add(m.group(1))

    if layer == 'ui':
        if 'CoreData' in imports or 'Combine' in imports and 'ViewModel' not in path:
            out.append({"file": path, "line": 1, "severity":"P2","rule":"ui_data_coupling","message":"UI layer imports Data frameworks; move data access to ViewModel/Interactor."})
        # Naive URLSession usage in UI
        if any('URLSession' in ln for ln in lines):
            out.append({"file": path, "line": 1, "severity":"P2","rule":"ui_networking","message":"Networking in UI layer. Move to service and inject."})

    if layer == 'domain':
        if any(k in imports for k in UI_KITS):
            out.append({"file": path, "line": 1, "severity":"P1","rule":"domain_ui_dependency","message":"Domain depends on UI framework. Invert dependency through protocols."})

    if layer == 'data':
        if any(k in imports for k in UI_KITS):
            out.append({"file": path, "line": 1, "severity":"P2","rule":"data_ui_dependency","message":"Data layer importing UI framework. Remove coupling."})

    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default='.')
    ap.add_argument('--out', default='arch.json')
    args=ap.parse_args()

    results=[]
    for fp in list_swift(args.path):
        results.extend(analyze_file(fp))

    with open(args.out,'w',encoding='utf-8') as f:
        json.dump({"architecture": results}, f, indent=2)
    print(f"Wrote {len(results)} architecture findings to {args.out}")

if __name__=='__main__':
    main()
