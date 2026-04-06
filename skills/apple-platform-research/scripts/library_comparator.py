#!/usr/bin/env python3
"""
Compare libraries on multiple metrics (GitHub-based + heuristics).

Usage:
    python scripts/library_comparator.py --repos owner/a owner/b --weights stars=0.3,commits=0.3,responses=0.4 --out ./out/compare.json
"""
import argparse
import os
import json
from typing import Dict, Any, List
from tools.utils import session_with_retries, json_dump, ensure_out, polite_sleep, bounded

API = "https://api.github.com"

def headers():
    t = os.environ.get("GITHUB_TOKEN", "")
    h = {"Accept": "application/vnd.github+json"}
    if t:
        h["Authorization"] = f"Bearer {t}"
    return h

def fetch_meta(session, repo: str) -> Dict[str, Any]:
    r = session.get(f"{API}/repos/{repo}", headers=headers(), timeout=20)
    r.raise_for_status()
    return r.json()

def fetch_releases(session, repo: str) -> List[Dict[str, Any]]:
    r = session.get(f"{API}/repos/{repo}/releases", headers=headers(), timeout=20)
    r.raise_for_status()
    return r.json()

def score_repo(meta: Dict[str, Any], releases: List[Dict[str, Any]], weights: Dict[str, float]) -> float:
    stars = meta.get("stargazers_count", 0)
    forks = meta.get("forks_count", 0)
    open_issues = meta.get("open_issues_count", 0)
    # crude heuristics; values normalized
    score = 0.0
    score += weights.get("stars", 0.25) * min(stars/1000.0, 1.0)
    score += weights.get("forks", 0.15) * min(forks/200.0, 1.0)
    score += weights.get("releases", 0.2) * min(len(releases)/10.0, 1.0)
    score += weights.get("issues", 0.2) * (1.0 - min(open_issues/500.0, 1.0))
    # prefer recent activity
    score += weights.get("activity", 0.2) * (1.0 if meta.get("updated_at") else 0.5)
    return min(max(score, 0.0), 1.0)

def parse_weights(s: str) -> Dict[str, float]:
    pairs = [p for p in s.split(",") if p]
    w = {}
    for p in pairs:
        k, v = p.split("=")
        w[k.strip()] = float(v.strip())
    return w

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", nargs="+", required=True)
    ap.add_argument("--weights", default="stars=0.3,forks=0.1,releases=0.2,issues=0.2,activity=0.2")
    ap.add_argument("--out", default="./out/compare.json")
    args = ap.parse_args()

    weights = parse_weights(args.weights)
    session = session_with_retries()
    results: List[Dict[str, Any]] = []
    for repo in args.repos:
        meta = fetch_meta(session, repo)
        releases = fetch_releases(session, repo)
        sc = score_repo(meta, releases, weights)
        results.append({"repo": repo, "score": sc, "meta": {"stars": meta.get("stargazers_count"), "forks": meta.get("forks_count"), "open_issues": meta.get("open_issues_count")}})
        polite_sleep(0.4, 1.0)

    ensure_out()
    json_dump({"weights": weights, "results": results}, args.out)
    print(f"Wrote scores for {len(results)} repos -> {args.out}")

if __name__ == "__main__":
    main()
