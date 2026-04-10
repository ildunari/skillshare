#!/usr/bin/env python3
'''
Validate that all must-keep facts survived the rewrite.

This script expects a constraints JSON produced by extract_constraints.py (or edited
by hand/LLM) and checks that every string in:
- must_keep_flat
- manual_additions
appears verbatim in the rewritten text.

Usage:
  python scripts/validate_preservation.py --constraints constraints.json --in after.txt
  cat after.txt | python scripts/validate_preservation.py --constraints constraints.json --stdin
'''
from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List, Tuple


def read_text(path: str | None, stdin: bool) -> str:
    if stdin:
        import sys
        return sys.stdin.read()
    if not path:
        raise SystemExit("Provide --in <file> or --stdin")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_constraints(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dedupe(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate preservation of must-keep facts.")
    ap.add_argument("--constraints", required=True, help="Path to constraints JSON")
    ap.add_argument("--in", dest="in_path", help="Rewritten text file path")
    ap.add_argument("--stdin", action="store_true", help="Read rewritten text from stdin")
    args = ap.parse_args()

    constraints = load_constraints(args.constraints)
    after = read_text(args.in_path, args.stdin)

    must_keep_flat: List[str] = constraints.get("must_keep_flat", [])
    manual: List[str] = constraints.get("manual_additions", [])

    checks = dedupe([s for s in must_keep_flat + manual if isinstance(s, str) and s.strip()])

    missing: List[str] = [s for s in checks if s not in after]

    result = {
        "pass": len(missing) == 0,
        "checked_count": len(checks),
        "missing_count": len(missing),
        "missing": missing[:200],  # cap for sanity
    }

    import sys
    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
