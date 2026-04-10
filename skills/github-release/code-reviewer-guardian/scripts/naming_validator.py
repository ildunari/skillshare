#!/usr/bin/env python3
"""
naming_validator.py
-------------------
Validate common Swift naming conventions:
- Types: UpperCamelCase (allow URL/ID suffixes)
- Functions/vars: lowerCamelCase
- Bool predicates start with is/has/should
- Acronym handling: URL, ID, JSON

Usage:
  python naming_validator.py --path . --out names.json
"""
import argparse, os, re, json
from typing import List, Dict

TYPE_DEF = re.compile(r"\b(class|struct|enum|protocol)\s+(\w+)\b")
FUNC_DEF = re.compile(r"\bfunc\s+(\w+)\s*\(")
VAR_DEF = re.compile(r"\b(?:var|let)\s+(\w+)\s*[:=]")
BOOL_DEF = re.compile(r"\b(?:var|let)\s+(\w+)\s*:\s*Bool\b")

UPPER_CAMEL = re.compile(r"^[A-Z][A-Za-z0-9]*$" )
LOWER_CAMEL = re.compile(r"^[a-z][A-Za-z0-9]*$" )

def list_swift(root: str) -> List[str]:
    out=[]
    for r,_,fs in os.walk(root):
        if any(p in r for p in ("Pods/", ".build/", "DerivedData/", "Carthage/", "vendor/", "Generated/")):
            continue
        for f in fs:
            if f.endswith('.swift'):
                out.append(os.path.join(r,f))
    return out

def analyze_file(path: str) -> List[Dict]:
    findings=[]
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            content=f.read()
    except Exception as e:
        return [{"file": path, "line": 0, "severity":"P1","rule":"read_error","message":str(e)}]

    for m in TYPE_DEF.finditer(content):
        name = m.group(2)
        if not UPPER_CAMEL.match(name):
            findings.append({"file": path, "line": 1, "severity":"P3","rule":"type_naming","message": f"Type '{name}' should be UpperCamelCase."})

    for m in FUNC_DEF.finditer(content):
        name = m.group(1)
        if not LOWER_CAMEL.match(name):
            findings.append({"file": path, "line": 1, "severity":"P3","rule":"func_naming","message": f"Function '{name}' should be lowerCamelCase."})

    for m in VAR_DEF.finditer(content):
        name = m.group(1)
        if not LOWER_CAMEL.match(name):
            findings.append({"file": path, "line": 1, "severity":"P3","rule":"var_naming","message": f"Variable '{name}' should be lowerCamelCase."})

    for m in BOOL_DEF.finditer(content):
        name = m.group(1)
        if not (name.startswith('is') or name.startswith('has') or name.startswith('should')):
            findings.append({"file": path, "line": 1, "severity":"P3","rule":"bool_prefix","message": f"Boolean '{name}' should start with is/has/should."})

    return findings

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default='.')
    ap.add_argument('--out', default='names.json')
    args=ap.parse_args()

    results=[]
    for fp in list_swift(args.path):
        results.extend(analyze_file(fp))

    with open(args.out,'w',encoding='utf-8') as f:
        json.dump({"naming": results}, f, indent=2)
    print(f"Wrote {len(results)} naming findings to {args.out}")

if __name__=='__main__':
    main()
