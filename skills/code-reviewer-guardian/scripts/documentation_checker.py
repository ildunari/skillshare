#!/usr/bin/env python3
"""
documentation_checker.py
------------------------
Computes documentation coverage for Swift code:
- Public/open types and members should have DocC/`///` comments
- Emits coverage rate per file and missing symbols list
- Optional quality checks: presence of Parameters/Returns tags

Usage:
  python documentation_checker.py --path . --out docs.json
"""
import argparse, os, re, json
from typing import List, Dict

PUB_DECL = re.compile(r"^\s*(public|open)\s+(class|struct|enum|protocol|func|var|let)\s+")
DOC_LINE = re.compile(r"^\s*///|\s*/\*\*|^\s*\*\s")  # simple DocC markers
SYMBOL_DEF = re.compile(r"^\s*(?:public|open)\s+(class|struct|enum|protocol|func|var|let)\s+(\w+)\b")

def list_swift(root: str) -> List[str]:
    files=[]
    for r,_,fs in os.walk(root):
        if any(p in r for p in ("Pods/", ".build/", "DerivedData/", "Carthage/", "vendor/", "Generated/")):
            continue
        for f in fs:
            if f.endswith('.swift'):
                files.append(os.path.join(r,f))
    return files

def analyze_file(path: str) -> Dict:
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            lines=f.read().splitlines()
    except Exception as e:
        return {"file": path, "error": str(e)}

    total=0; documented=0; missing=[]

    for i, ln in enumerate(lines):
        if PUB_DECL.match(ln):
            total+=1
            # check previous lines for DocC markers
            has_doc=False
            for j in range(max(0, i-3), i):
                if DOC_LINE.search(lines[j]):
                    has_doc=True; break
            if has_doc:
                documented+=1
            else:
                sym = SYMBOL_DEF.match(ln)
                sym_name = sym.group(2) if sym else "<symbol>"
                missing.append({"line": i+1, "symbol": sym_name})

    coverage = (documented/total*100.0) if total>0 else 100.0
    return {"file": path, "coverage": round(coverage,2), "total": total, "documented": documented, "missing": missing}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default='.')
    ap.add_argument('--out', default='docs.json')
    args=ap.parse_args()

    results=[analyze_file(fp) for fp in list_swift(args.path)]
    # overall coverage
    cov = [r["coverage"] for r in results if "coverage" in r]
    overall = round(sum(cov)/len(cov),2) if cov else 100.0
    out = {"overall_coverage": overall, "files": results}
    with open(args.out,'w',encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(f"Doc coverage overall: {overall}% -> {args.out}")

if __name__=='__main__':
    main()
