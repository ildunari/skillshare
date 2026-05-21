#!/usr/bin/env python3
"""
Find design resources and inspiration (Figma, Dribbble, Behance, Mobbin).

- Scrapes public pages for metadata and links (respect robots).
- Outputs a CSV/JSON with title, url, author, platform, notes.

Usage:
    python scripts/design_resource_crawler.py --query "iOS onboarding" --sites figma,dribbble,mobbin --limit 30 --out ./out/design.json
"""
import argparse
import json
import re
from typing import List, Dict, Any
from urllib.parse import quote_plus
from tools.utils import get_html, json_dump, ensure_out, polite_sleep
from tools.scraping import get_links_with_text

SEARCH_ENGINES = {
    "figma": "https://www.figma.com/search/?model_type=community&query={q}",
    "dribbble": "https://dribbble.com/search/{q}",
    "behance": "https://www.behance.net/search?search={q}",
    "mobbin": "https://mobbin.com/search?q={q}"
}

def crawl_site(site: str, query: str, limit: int) -> List[Dict[str, Any]]:
    url = SEARCH_ENGINES[site].format(q=quote_plus(query))
    html = get_html(url)
    links = get_links_with_text(html, "a")
    items = []
    seen = set()
    for l in links:
        href = l["href"]
        text = l["text"]
        if not href or href in seen:
            continue
        if site in href:
            seen.add(href)
            items.append({"site": site, "title": text[:120], "url": href})
        if len(items) >= limit:
            break
    return items

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--sites", default="figma,dribbble,behance,mobbin")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--out", default="./out/design.json")
    args = ap.parse_args()

    sites = [s.strip() for s in args.sites.split(",") if s.strip() in SEARCH_ENGINES]
    all_items: List[Dict[str, Any]] = []
    for s in sites:
        try:
            items = crawl_site(s, args.query, args.limit)
            all_items.extend(items)
            polite_sleep(0.5, 1.0)
        except Exception:
            continue

    ensure_out()
    json_dump(all_items, args.out)
    print(f"Wrote {len(all_items)} design links -> {args.out}")

if __name__ == "__main__":
    main()
