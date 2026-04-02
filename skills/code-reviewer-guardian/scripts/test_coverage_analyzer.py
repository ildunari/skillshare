#!/usr/bin/env python3
"""
test_coverage_analyzer.py
-------------------------
Analyze Xcode coverage JSON (from `xcrun xccov view --report --json`)
and suggest gaps prioritized by file risk (complexity, smells optional).

Usage:
  python test_coverage_analyzer.py --coverage coverage.json --out coverage_findings.json
"""
import argparse, json, os
from typing import Dict, List

def load_coverage(path: str) -> Dict:
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def analyze_coverage(data: Dict, min_target: float = 75.0) -> Dict:
    files = data.get('files') or data  # support flat list
    findings = []
    overall_cov = 0.0; n=0
    for f in files:
        # Many xccov formats have {name, lineCoverage}
        path = f.get('name') or f.get('path') or '<unknown>'
        cov = f.get('lineCoverage') or f.get('coverage') or 0.0
        if isinstance(cov, float):
            cov_pct = cov * 100.0 if cov <= 1.0 else cov
        else:
            cov_pct = float(cov)
        overall_cov += cov_pct; n += 1
        if cov_pct < min_target and path.endswith('.swift') and '/Tests/' not in path:
            findings.append({
                'file': path, 'severity':'P2' if cov_pct<50 else 'P3',
                'message': f'Coverage {cov_pct:.1f}% below target {min_target:.0f}%. Add unit tests for core logic.'
            })
    avg = (overall_cov/n) if n else 100.0
    return {'overall': round(avg,2), 'findings': findings}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--coverage', required=True)
    ap.add_argument('--out', default='coverage_findings.json')
    ap.add_argument('--target', type=float, default=75.0)
    args = ap.parse_args()

    data = load_coverage(args.coverage)
    result = analyze_coverage(data, args.target)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print(f"Overall coverage {result['overall']}% -> {args.out}; {len(result['findings'])} low-coverage files.")

if __name__ == '__main__':
    main()
