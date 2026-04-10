#!/usr/bin/env python3
"""
Search WWDC session transcripts for topics.

- Queries developer.apple.com WWDC pages and parses transcript text if available.
- Outputs matches with timecodes and URLs.

Usage:
    python scripts/wwdc_session_searcher.py --query "SwiftData" --years 2023 2024 2025 --out ./out/wwdc_swiftdata.json
"""
import argparse
import re
import json
from typing import List, Dict, Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tools.utils import get_html, json_dump, ensure_out, polite_sleep

BASE = "https://developer.apple.com"

def find_sessions(year: int, query: str) -> List[Dict[str, Any]]:
    url = f"{BASE}/videos/wwdc{year}/"
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a[href*='/videos/play/']")
    results = []
    for a in cards:
        href = urljoin(BASE, a.get("href"))
        title = a.get_text(strip=True)
        if query.lower() in title.lower():
            results.append({"year": year, "title": title, "url": href})
    return results

def fetch_transcript(url: str) -> List[Dict[str, str]]:
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    transcript = []
    for row in soup.select("[data-timecode]"):
        t = row.get("data-timecode")
        text = row.get_text(strip=True)
        transcript.append({"time": t, "text": text})
    return transcript

def search_in_transcript(transcript: List[Dict[str, str]], query: str) -> List[Dict[str, str]]:
    q = query.lower()
    hits = []
    for seg in transcript:
        if q in seg["text"].lower():
            hits.append(seg)
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--years", nargs="+", type=int, default=[])
    ap.add_argument("--out", default="./out/wwdc_hits.json")
    args = ap.parse_args()
    years = args.years or [2025, 2024, 2023]

    all_hits = []
    for y in years:
        sessions = find_sessions(y, args.query)
        for s in sessions:
            try:
                transcript = fetch_transcript(s["url"])
                matches = search_in_transcript(transcript, args.query)
                if matches:
                    all_hits.append({"year": y, "session": s["title"], "url": s["url"], "matches": matches})
            except Exception:
                continue
            polite_sleep(0.4, 0.9)

    ensure_out()
    json_dump(all_hits, args.out)
    print(f"Wrote {len(all_hits)} session hits -> {args.out}")

if __name__ == "__main__":
    main()
