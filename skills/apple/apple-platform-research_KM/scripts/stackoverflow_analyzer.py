#!/usr/bin/env python3
"""
Analyze Stack Overflow questions for pain points.

- Uses Stack Exchange API to fetch questions by tags and date range.
- Ranks by views, unanswered, and score.
- Optionally clusters titles with TF-IDF + KMeans.

Usage:
    export STACKEXCHANGE_KEY=xxx  # optional
    python scripts/stackoverflow_analyzer.py --tags swift,swiftui,ios --days 90 --cluster 8 --out ./out/so.json
"""
import argparse
import os
import time
import json
import math
from typing import List, Dict, Any
from datetime import datetime, timedelta
from tools.utils import session_with_retries, json_dump, ensure_out, polite_sleep
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

API = "https://api.stackexchange.com/2.3"

def fetch_questions(tags: List[str], fromdate: int, todate: int, key: str = "") -> List[Dict[str, Any]]:
    session = session_with_retries()
    has_more = True
    page = 1
    items = []
    while has_more and page < 20:
        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": ";".join(tags),
            "site": "stackoverflow",
            "fromdate": fromdate,
            "todate": todate,
            "pagesize": 100,
            "page": page,
        }
        if key:
            params["key"] = key
        r = session.get(f"{API}/questions", params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("items", []))
        has_more = data.get("has_more", False)
        page += 1
        polite_sleep(0.4, 0.9)
    return items

def cluster_titles(items: List[Dict[str, Any]], k: int) -> Dict[int, List[Dict[str, Any]]]:
    titles = [it.get("title", "") for it in items]
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(titles)
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X)
    buckets: Dict[int, List[Dict[str, Any]]] = {}
    for it, label in zip(items, labels):
        buckets.setdefault(int(label), []).append(it)
    return buckets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", default="swift,ios,swiftui")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--cluster", type=int, default=0)
    ap.add_argument("--out", default="./out/so.json")
    args = ap.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    todate = int(time.time())
    fromdate = int((datetime.utcnow() - timedelta(days=args.days)).timestamp())
    key = os.environ.get("STACKEXCHANGE_KEY", "")

    items = fetch_questions(tags, fromdate, todate, key)
    items = sorted(items, key=lambda x: (x.get("is_answered") == False, x.get("view_count", 0)), reverse=True)
    result = {"summary": {"count": len(items)}, "items": items}

    if args.cluster and len(items) >= args.cluster:
        buckets = cluster_titles(items, args.cluster)
        result["clusters"] = {str(k): [{"title": it["title"], "link": it["link"]} for it in v] for k, v in buckets.items()}

    ensure_out()
    json_dump(result, args.out)
    print(f"Wrote {len(items)} questions -> {args.out}")

if __name__ == "__main__":
    main()
