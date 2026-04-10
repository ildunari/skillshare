#!/usr/bin/env python3
"""
code_smell_detector.py
----------------------
Detect classic code smells in Swift with naive heuristics:
- Long Method
- God Class (type length & member count)
- Feature Envy (foreign type references)
- Data Clumps (repeated parameter tuples)
- Duplicate Code (hash-based near duplicates)

Outputs JSON with severity (P1/P2/P3) and suggested refactorings.
"""
import argparse, os, re, json, hashlib
from typing import List, Dict, Tuple

TYPE_DEF = re.compile(r"^\s*(?:public|internal|open|fileprivate|private)?\s*(?:final\s+)?(class|struct|enum)\s+(\w+)\b")
FUNC_DEF = re.compile(r"^\s*(?:@\w+\s+)*func\s+(\w+)\s*\(([^)]*)\)")
IMPORT_RX = re.compile(r"^\s*import\s+(\w+)")
SELF_RX = re.compile(r"\bself\.")
IDENT_RX = re.compile(r"\b[A-Z][A-Za-z0-9_]+\b")

PARAM_TUPLE_SPLIT = re.compile(r"\s*,\s*")

def list_swift_files(root: str) -> List[str]:
    files = []
    for r, _, fs in os.walk(root):
        if any(p in r for p in ("Pods/", ".build/", "DerivedData/", "Carthage/", "vendor/", "Generated/")):
            continue
        for f in fs:
            if f.endswith(".swift"):
                files.append(os.path.join(r, f))
    return files

def fingerprint_block(block: List[str]) -> str:
    text = "\n".join([re.sub(r"\s+", " ", ln.strip()) for ln in block if ln.strip()])
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def detect_duplicates(lines: List[str], window: int = 12) -> List[Tuple[int, int, str]]:
    seen = {}
    dups = []
    for i in range(0, max(0, len(lines)-window)):
        block = lines[i:i+window]
        fp = fingerprint_block(block)
        if fp in seen and abs(seen[fp] - i) > window:
            dups.append((seen[fp], i, fp))
        else:
            seen[fp] = i
    return dups

def parse_functions(lines: List[str]) -> List[Tuple[int,int,str,str]]:
    spans = []
    i=0
    n=len(lines)
    while i<n:
        m = FUNC_DEF.match(lines[i])
        if m:
            name = m.group(1)
            params = m.group(2)
            opened = 0; closed=0
            start=i
            j=i
            while j<n:
                opened += lines[j].count('{')
                closed += lines[j].count('}')
                if opened>0 and opened==closed:
                    spans.append((start, j, name, params))
                    i=j
                    break
                j+=1
        i+=1
    return spans

def detect_feature_envy(lines: List[str], start: int, end: int) -> bool:
    body = "\n".join(lines[start:end+1])
    # Feature envy if code references foreign types significantly more than self
    self_refs = len(SELF_RX.findall(body))
    foreign = 0
    # naive: count capitalized identifiers as types (excluding keywords)
    for tok in IDENT_RX.findall(body):
        if tok not in ("Self", "URL", "ID", "JSON", "Int", "String", "Bool", "Double"):
            foreign += 1
    return foreign > max(4, self_refs * 2)

def analyze_file(path: str) -> List[Dict]:
    out = []
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            lines = f.read().splitlines()
    except Exception as e:
        return [{"file": path, "line": 0, "severity": "P1", "rule": "read_error", "message": str(e)}]

    # God class heuristic
    type_lines = 0
    members = 0
    for i, ln in enumerate(lines):
        if TYPE_DEF.match(ln):
            type_lines = 0; members = 0
        if FUNC_DEF.match(ln):
            members += 1
        type_lines += 1
        if type_lines > 600 or members > 25:
            out.append({"file": path, "line": i+1, "severity": "P2", "rule": "god_object", "message": f"Type may be a God Object (lines~{type_lines}, funcs~{members}). Extract types."})
            break

    # Long method & feature envy
    for (start, end, name, params) in parse_functions(lines):
        length = end - start + 1
        if length > 60:
            out.append({"file": path, "line": start+1, "severity": "P2", "rule": "long_method", "message": f"Method '{name}' is {length} lines. Consider Extract Method/Type."})
        if detect_feature_envy(lines, start, end):
            out.append({"file": path, "line": start+1, "severity": "P2", "rule": "feature_envy", "message": f"Method '{name}' heavily references foreign types. Consider Move Method or redesign."})

        # Data clumps in parameter list
        params_list = [p.strip() for p in PARAM_TUPLE_SPLIT.split(params) if p.strip()]
        if len(params_list) >= 4:
            out.append({"file": path, "line": start+1, "severity": "P3", "rule": "data_clumps", "message": f"Method '{name}' has many parameters ({len(params_list)}). Consider Parameter Object."})

    # Duplicates
    for a, b, _ in detect_duplicates(lines):
        out.append({"file": path, "line": a+1, "severity": "P3", "rule": "duplicate_code", "message": f"Duplicate block near line {a+1} and {b+1}. Consider DRYing up."})
        break  # avoid flooding

    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', default='.')
    ap.add_argument('--out', default='smells.json')
    args = ap.parse_args()

    results = []
    for fp in list_swift_files(args.path):
        results.extend(analyze_file(fp))

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump({'smells': results}, f, indent=2)
    print(f"Wrote {len(results)} smells to {args.out}")

if __name__ == '__main__':
    main()
