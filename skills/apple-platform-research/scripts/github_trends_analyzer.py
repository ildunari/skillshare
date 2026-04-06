#!/usr/bin/env python3
"""
Scrape and analyze GitHub trending for Swift/iOS.

- Scrapes https://github.com/trending for topic=swift or spoken_language etc.
- Computes basic metrics and writes CSV/JSON artifacts.
- Optionally uses GitHub API for enrichment if GITHUB_TOKEN provided.

Usage:
    python scripts/github_trends_analyzer.py --language Swift --since weekly --limit 50 --out ./out/trending_swift.json
"""
import argparse
import json
import re
import sys
from typing import List, Dict, Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tools.utils import get_html, polite_sleep, json_dump, ensure_out
from tools.scraping import get_links_with_text

BASE = "https://github.com"

def parse_trending(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    repos = []
    for article in soup.select("article.Box-row"):
        h = article.select_one("h2 a")
        if not h:
            continue
        href = h.get("href", "").strip("/")
        full = urljoin(BASE, href)
        owner, name = href.split("/")[:2]
        desc_el = article.select_one("p")
        desc = desc_el.get_text(strip=True) if desc_el else ""
        star_el = article.select_one("a[href$='/stargazers']")
        stars = star_el.get_text(strip=True).replace(",", "") if star_el else "0"
        lang_el = article.select_one("[itemprop='programmingLanguage']")
        lang = lang_el.get_text(strip=True) if lang_el else ""
        repos.append({"owner": owner, "name": name, "url": full, "description": desc, "stars": int(re.sub(r'[^0-9]', '', stars or '0') or 0), "language": lang})
    return repos

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--language", default="Swift")
    ap.add_argument("--since", choices=["daily","weekly","monthly"], default="weekly")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--out", default="./out/trending.json")
    args = ap.parse_args()

    url = f"{BASE}/trending/{args.language}?since={args.since}"
    html = get_html(url)
    repos = parse_trending(html)[:args.limit]
    ensure_out()
    json_dump(repos, args.out)
    print(f"Wrote {len(repos)} repos -> {args.out}")

if __name__ == "__main__":
    main()
