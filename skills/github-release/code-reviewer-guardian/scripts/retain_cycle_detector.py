#!/usr/bin/env python3
"""
retain_cycle_detector.py
------------------------
Heuristics to flag likely retain cycles:
- Escaping closure capturing self without [weak self]
- Delegates declared as strong
- Combine/NotificationCenter observers not removed
- Timers retaining targets

Outputs JSON with findings.
"""
import argparse, os, re, json
from typing import List, Dict

ESCAPING_CLOSURE = re.compile(r"\b(@escaping)\b")
CLOSURE_START = re.compile(r"\{\s*\[([^\]]*)\]?")  # capture list
SELF_USE = re.compile(r"\bself\.")
DELEGATE_STRONG = re.compile(r"\bvar\s+\w+Delegate\s*:\s*(?:weak\s+)?[^=]+\{?")
WEAK_VAR = re.compile(r"\bweak\s+var\s+\w+Delegate\b")
DELEGATE_DECL = re.compile(r"\bvar\s+(\w+Delegate)\s*:\s*[^=]+\b")
TIMER_SCHEDULED = re.compile(r"Timer\.scheduledTimer|DispatchSourceTimer|CADisplayLink\("))
OBSERVER_ADD = re.compile(r"NotificationCenter\.default\.addObserver\("))
OBSERVER_REMOVE = re.compile(r"NotificationCenter\.default\.removeObserver\(")
SINK_ASSIGN = re.compile(r"\.sink\s*\{[^}]*self\.")
CANCEL_BAG = re.compile(r"AnyCancellable|cancel\(\)")

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
    res=[]
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            content=f.read()
    except Exception as e:
        return [{"file": path, "line":0, "severity":"P1","rule":"read_error","message":str(e)}]

    lines = content.splitlines()

    # Escaping closure capturing self
    for idx, ln in enumerate(lines, 1):
        if ESCAPING_CLOSURE.search(ln):
            # Look ahead a few lines for closure body using self without weak capture
            window = "\n".join(lines[idx-1: idx+10])
            if SELF_USE.search(window) and not re.search(r"\[\s*weak\s+self\s*\]", window):
                res.append({"file": path, "line": idx, "severity":"P1","rule":"retain_cycle_closure","message":"Escaping closure captures self without [weak self]."})

    # Delegates strong vs weak
    for idx, ln in enumerate(lines, 1):
        if DELEGATE_DECL.search(ln):
            if not re.search(r"\bweak\b", ln):
                res.append({"file": path, "line": idx, "severity":"P2","rule":"delegate_strong","message":"Delegate should typically be weak to avoid cycles."})

    # Notification observers without removal (heuristic)
    if OBSERVER_ADD.search(content) and not OBSERVER_REMOVE.search(content):
        res.append({"file": path, "line": 1, "severity":"P2","rule":"notification_leak","message":"Observer added but no corresponding removeObserver found."})

    # Combine sinks referencing self without cancellation
    if SINK_ASSIGN.search(content) and not CANCEL_BAG.search(content):
        res.append({"file": path, "line": 1, "severity":"P2","rule":"combine_leak","message":"Combine subscription referencing self without stored AnyCancellable or cancel()."})

    # Timers retaining target
    if TIMER_SCHEDULED.search(content) and not re.search(r"\[\s*weak\s+self\s*\]", content):
        res.append({"file": path, "line": 1, "severity":"P2","rule":"timer_retain","message":"Timer closure may retain self; add [weak self] and invalidate in deinit."})

    return res

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default='.')
    ap.add_argument('--out', default='retains.json')
    args=ap.parse_args()

    results=[]
    for fp in list_swift(args.path):
        results.extend(analyze_file(fp))

    with open(args.out,'w',encoding='utf-8') as f:
        json.dump({"retains": results}, f, indent=2)
    print(f"Wrote {len(results)} retain findings to {args.out}")

if __name__=='__main__':
    main()
