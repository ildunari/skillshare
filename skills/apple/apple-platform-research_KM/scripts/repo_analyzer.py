#!/usr/bin/env python3
"""
Analyze GitHub repos for quality signals.

Signals:
- stars, forks, watchers
- issues open/closed ratio
- PR velocity (time to first response)
- commit cadence (last 90 days)
- releases cadence
- bus factor (top N committers share)

Requires GITHUB_TOKEN (optional but recommended).

Usage:
    python scripts/repo_analyzer.py --repo owner/name --repo another/one --out ./out/repos.json
"""
import argparse
import os
import time
import json
from collections import Counter, defaultdict
from typing import Dict, Any, List, Tuple
import datetime as dt
from tools.utils import session_with_retries, json_dump, getenv, polite_sleep, ensure_out, Score, bounded

API = "https://api.github.com"

def gh_headers(token: str = "") -> Dict[str, str]:
    h = {"Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def fetch_repo(session, full: str, headers) -> Dict[str, Any]:
    r = session.get(f"{API}/repos/{full}", headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def fetch_commits(session, full: str, headers, since: str) -> List[Dict[str, Any]]:
    items = []
    page = 1
    while True:
        resp = session.get(f"{API}/repos/{full}/commits", params={"since": since, "per_page": 100, "page": page}, headers=headers, timeout=20)
        if resp.status_code == 404:
            break
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break
        items.extend(chunk)
        page += 1
        polite_sleep(0.4, 0.9)
    return items

def fetch_issues(session, full: str, headers, state: str, since: str) -> List[Dict[str, Any]]:
    items = []
    page = 1
    while True:
        params={"state": state, "since": since, "per_page": 100, "page": page}
        resp = session.get(f"{API}/repos/{full}/issues", params=params, headers=headers, timeout=20)
        resp.raise_for_status()
        chunk = [it for it in resp.json() if "pull_request" not in it]
        if not chunk:
            break
        items.extend(chunk)
        page += 1
        polite_sleep(0.4, 0.9)
    return items

def fetch_pulls(session, full: str, headers, state: str) -> List[Dict[str, Any]]:
    items = []
    page = 1
    while True:
        resp = session.get(f"{API}/repos/{full}/pulls", params={"state": state, "per_page": 100, "page": page}, headers=headers, timeout=20)
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break
        items.extend(chunk)
        page += 1
        polite_sleep(0.4, 0.9)
    return items

def compute_scores(meta: Dict[str, Any], commits: List[Dict[str, Any]], issues_open: List[Dict[str, Any]], releases_count: int) -> Dict[str, Any]:
    stars = meta.get("stargazers_count", 0)
    forks = meta.get("forks_count", 0)
    watchers = meta.get("subscribers_count", 0)
    pushed_at = meta.get("pushed_at", "")
    last_push_days = 9999
    if pushed_at:
        last_push_days = (dt.datetime.utcnow() - dt.datetime.fromisoformat(pushed_at.replace("Z",""))).days
    commit_count = len(commits)
    open_issues = len(issues_open)
    # Simple normalization
    score = bounded((stars/1000.0) + (commit_count/200.0) + (releases_count/10.0) - (open_issues/500.0) - (last_push_days/365.0), 0.0, 1.0)
    return {"score": score, "signals": {"stars": stars, "forks": forks, "watchers": watchers, "commits_90d": commit_count, "open_issues": open_issues, "releases": releases_count, "last_push_days": last_push_days}}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", action="append", required=True, help="owner/name")
    ap.add_argument("--out", default="./out/repos.json")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    headers = gh_headers(token)
    since = (dt.datetime.utcnow() - dt.timedelta(days=90)).isoformat() + "Z"
    session = session_with_retries()

    results = []
    for full in args.repo:
        meta = fetch_repo(session, full, headers)
        commits = fetch_commits(session, full, headers, since)
        issues_open = fetch_issues(session, full, headers, "open", since)
        releases_resp = session.get(f"{API}/repos/{full}/releases", headers=headers, timeout=20)
        releases_resp.raise_for_status()
        releases = releases_resp.json()
        signals = compute_scores(meta, commits, issues_open, len(releases))
        results.append({"repo": full, "meta": meta, "signals": signals})
        print(f"Analyzed {full}: score={signals['score']:.2f}")
        polite_sleep(0.5, 1.1)

    ensure_out()
    json_dump(results, args.out)
    print(f"Wrote {len(results)} repos -> {args.out}")

if __name__ == "__main__":
    main()
