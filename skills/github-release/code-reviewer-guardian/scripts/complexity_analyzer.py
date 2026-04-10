#!/usr/bin/env python3
"""
complexity_analyzer.py
----------------------
Computes a naive cyclomatic complexity for Swift functions based on
keywords (if, guard, for, while, repeat, case, catch, throw, defer).
Also suggests simplifications when thresholds are exceeded.

Usage:
  python complexity_analyzer.py --path . --out complexity.json
"""
import argparse, os, re, json
from typing import List, Tuple, Dict

FUNC_DEF = re.compile(r"^\s*(?:@\w+\s+)*func\s+(\w+)\s*\([^)]*\).*?\{\s*$")
TOKENS = re.compile(r"\b(if|guard|for|while|repeat|case|catch|throw|defer|where|\?\:|&&|\|\|)\b")

def list_swift(root: str) -> List[str]:
    files = []
    for r,_,fs in os.walk(root):
        if any(p in r for p in ("Pods/", ".build/", "DerivedData/", "Carthage/", "vendor/", "Generated/")):
            continue
        for f in fs:
            if f.endswith('.swift'):
                files.append(os.path.join(r,f))
    return files

def parse_functions(lines: List[str]) -> List[Tuple[int,int,str]]:
    spans = []
    i=0; n=len(lines)
    while i<n:
        m = FUNC_DEF.match(lines[i])
        if m:
            name = m.group(1)
            opened=0; closed=0
            start=i; j=i
            while j<n:
                opened += lines[j].count('{')
                closed += lines[j].count('}')
                if opened>0 and opened==closed:
                    spans.append((start, j, name))
                    i=j
                    break
                j+=1
        i+=1
    return spans

def complexity_for(body: str) -> int:
    # Base complexity 1 + branches
    return 1 + len(TOKENS.findall(body))

def analyze_file(path: str) -> List[Dict]:
    out=[]
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            lines=f.read().splitlines()
    except Exception as e:
        return [{"file": path, "line": 0, "severity":"P1","rule":"read_error","message":str(e)}]

    for (start, end, name) in parse_functions(lines):
        body = "\n".join(lines[start:end+1])
        c = complexity_for(body)
        sev = "P3"
        if c >= 20: sev = "P1"
        elif c >= 10: sev = "P2"
        out.append({
            "file": path, "line": start+1, "severity": sev, "rule": "cyclomatic_complexity",
            "message": f"Function '{name}' complexity={c}. Consider early returns, guard clauses, or strategy pattern."
        })
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default='.')
    ap.add_argument('--out', default='complexity.json')
    args=ap.parse_args()

    results=[]
    for fp in list_swift(args.path):
        results.extend(analyze_file(fp))

    with open(args.out,'w',encoding='utf-8') as f:
        json.dump({"complexity": results}, f, indent=2)
    print(f"Wrote {len(results)} records to {args.out}")

if __name__=='__main__':
    main()
