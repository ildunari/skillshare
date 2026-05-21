#!/usr/bin/env python3
"""
Aggregate Reddit discussions relevant to iOS/macOS development.

- Uses PRAW (Reddit API) to fetch posts from target subreddits.
- Filters by score, comments, and keywords.
- Outputs JSON with useful fields.

Usage:
    export REDDIT_CLIENT_ID=xxx
    export REDDIT_CLIENT_SECRET=yyy
    export REDDIT_USER_AGENT="apple-platform-research"
    python scripts/reddit_aggregator.py --subs swift iOSProgramming SwiftUI --limit 50 --out ./out/reddit.json
"""
import argparse
import os
import json
from typing import List, Dict, Any
import praw
from tools.utils import json_dump, ensure_out

def collect(reddit, subs: List[str], limit: int, keywords: List[str]) -> List[Dict[str, Any]]:
    items = []
    for s in subs:
        subreddit = reddit.subreddit(s)
        for post in subreddit.hot(limit=limit):
            text = (post.title or "") + " " + (post.selftext or "")
            if keywords and not any(k.lower() in text.lower() for k in keywords):
                continue
            items.append({
                "subreddit": s,
                "title": post.title,
                "score": post.score,
                "num_comments": post.num_comments,
                "url": post.url,
                "permalink": f"https://reddit.com{post.permalink}",
                "created_utc": post.created_utc
            })
    return items

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subs", nargs="+", default=["swift", "iOSProgramming", "SwiftUI"])
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--keywords", nargs="*", default=[])
    ap.add_argument("--out", default="./out/reddit.json")
    args = ap.parse_args()

    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent=os.environ.get("REDDIT_USER_AGENT", "apple-platform-research")
    )

    data = collect(reddit, args.subs, args.limit, args.keywords)
    ensure_out()
    json_dump(data, args.out)
    print(f"Wrote {len(data)} posts -> {args.out}")

if __name__ == "__main__":
    main()
