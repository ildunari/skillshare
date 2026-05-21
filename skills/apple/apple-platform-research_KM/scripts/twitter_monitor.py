#!/usr/bin/env python3
"""
Monitor Twitter/X for iOS development keywords.

- Uses Twitter API v2 (bearer token) to search recent tweets.
- Deduplicates, filters by language, and exports JSON/CSV.

Usage:
    export TWITTER_BEARER_TOKEN=xxxxx
    python scripts/twitter_monitor.py --query "SwiftUI OR Xcode OR SwiftData" --lang en --max 100 --out ./out/twitter.json
"""
import argparse
import os
import json
from typing import List, Dict, Any
from tools.utils import session_with_retries, getenv, json_dump, ensure_out, polite_sleep

API = "https://api.twitter.com/2"

def search_recent(session, bearer: str, query: str, max_results: int = 50, lang: str = "en") -> List[Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {bearer}"}
    params = {
        "query": f"({query}) lang:{lang} -is:retweet",
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,lang,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "name,username,verified"
    }
    r = session.get(f"{API}/tweets/search/recent", params=params, headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()
    users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
    tweets = data.get("data", [])
    for t in tweets:
        t["user"] = users.get(t.get("author_id"))
    return tweets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="SwiftUI OR Xcode OR SwiftData OR #iOSDev")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--max", type=int, default=50)
    ap.add_argument("--out", default="./out/twitter.json")
    args = ap.parse_args()

    bearer = getenv("TWITTER_BEARER_TOKEN", required=True)
    session = session_with_retries()
    tweets = search_recent(session, bearer, args.query, args.max, args.lang)
    ensure_out()
    json_dump(tweets, args.out)
    print(f"Wrote {len(tweets)} tweets -> {args.out}")

if __name__ == "__main__":
    main()
