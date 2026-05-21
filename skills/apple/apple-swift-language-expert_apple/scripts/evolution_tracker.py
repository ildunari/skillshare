#!/usr/bin/env python3
"""Swift Evolution proposal tracker.

This script fetches the latest Swift Evolution proposals from the official
GitHub repository and prints a summary of proposals that have been accepted
and implemented.  If network access is unavailable, it prints instructions
for manual verification.

Usage::

    python3 evolution_tracker.py

This tool is intentionally simple: it uses the GitHub raw URL for the
swift-evolution README and extracts proposal identifiers and titles.  For more
advanced tracking, consider using the GitHub API or community dashboards.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request


REPO_README_URL = "https://raw.githubusercontent.com/apple/swift-evolution/main/README.md"


def fetch_readme(url: str = REPO_README_URL) -> str:
    """Fetch the README.md from swift-evolution.

    Returns the text content.  Raises urllib.error.URLError on failure.
    """
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read().decode("utf-8")


def parse_proposals(readme_text: str):
    """Parse proposal identifiers and descriptions from the README.

    Returns a list of tuples: (identifier, description).  Only proposals
    appearing in the `Accepted (Implemented)` section are extracted.
    """
    proposals = []
    in_section = False
    for line in readme_text.splitlines():
        # Detect the accepted implemented section header
        if line.strip().lower().startswith("### accepted and implemented proposals"):
            in_section = True
            continue
        if in_section:
            # End when hitting another header
            if line.startswith("###") and not line.lower().startswith("### accepted"):
                break
            # Match bullet lines with [SE-XXXX]
            m = re.match(r"\* \[(SE-[0-9]+)\]\([^\)]+\) - (.+)", line)
            if m:
                proposals.append((m.group(1), m.group(2).strip()))
    return proposals


def main():
    print("🔍 Swift Evolution proposal tracker")
    try:
        readme_text = fetch_readme()
    except urllib.error.URLError as exc:
        print("❌ Could not fetch the Swift Evolution README.  Network may be unavailable.")
        print(f"Error: {exc}")
        print("\nTo manually check proposals, visit https://github.com/apple/swift-evolution and review the dashboard.")
        return 1
    proposals = parse_proposals(readme_text)
    if not proposals:
        print("No implemented proposals found.  The README format may have changed.")
        return 1
    print(f"Found {len(proposals)} implemented proposals.  Showing the first 20:")
    for ident, desc in proposals[:20]:
        print(f"  {ident}: {desc}")
    print("\nSee the complete list on the Swift Evolution dashboard or adjust this script to paginate further.")
    return 0


if __name__ == "__main__":
    sys.exit(main())