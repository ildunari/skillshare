#!/usr/bin/env python3
'''
Extract "must-keep" constraints from a source text.

This is intentionally conservative: it extracts facts that are easy to detect and
high-risk to accidentally change during rewriting (URLs, emails, numbers, dates,
quotes, code blocks).

It also emits "candidates" (e.g., possible proper nouns) as suggestions that a
human or LLM should review and (optionally) add to must-keep.

Usage examples:
  # Read from stdin, write JSON to stdout
  python scripts/extract_constraints.py --stdin

  # Read from stdin, write JSON to a file
  python scripts/extract_constraints.py --stdin --out constraints.json

  # Read from a file
  python scripts/extract_constraints.py --in before.txt --out constraints.json
'''
from __future__ import annotations

import argparse
import hashlib
import json
import re
from typing import List, Tuple


MONTHS = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"


def read_text(path: str | None, stdin: bool) -> str:
    if stdin:
        import sys
        return sys.stdin.read()
    if not path:
        raise SystemExit("Provide --in <file> or --stdin")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def dedupe_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def filter_redundant_bare_numbers(items: List[str]) -> List[str]:
    """Remove bare numeric tokens that are substrings of longer captured facts.

    Example: if we captured "Jan 15, 2026" and also captured "15" and "2026",
    keep the full date and drop the bare numbers.
    """
    items = dedupe_preserve_order(items)
    lower_items = [x.lower() for x in items]
    by_len = sorted(range(len(items)), key=lambda i: len(items[i]), reverse=True)

    def is_bare_number(s: str) -> bool:
        s = s.strip()
        return re.fullmatch(r"[+-]?\d{1,4}", s) is not None

    keep = [True] * len(items)
    for i in range(len(items)):
        if not is_bare_number(items[i]):
            continue
        for j in by_len:
            if j == i:
                continue
            if len(items[j]) <= len(items[i]):
                continue
            if lower_items[i] in lower_items[j]:
                keep[i] = False
                break

    return [items[i] for i in range(len(items)) if keep[i]]


def filter_bare_numbers_against_corpus(nums: List[str], corpus: List[str]) -> List[str]:
    """Drop bare-number entries if they're already embedded in longer corpus tokens."""
    nums = dedupe_preserve_order(nums)
    corpus = dedupe_preserve_order(corpus)
    corpus_lower = [c.lower() for c in corpus]

    def is_bare_number(s: str) -> bool:
        s = s.strip()
        return re.fullmatch(r"[+-]?\d{1,4}", s) is not None

    keep: List[str] = []
    for n in nums:
        if not is_bare_number(n):
            keep.append(n)
            continue
        n_low = n.lower()
        redundant = False
        for c, c_low in zip(corpus, corpus_lower):
            if len(c) <= len(n):
                continue
            if n_low in c_low:
                redundant = True
                break
        if not redundant:
            keep.append(n)
    return keep


def find_code_blocks(text: str) -> List[str]:
    # Triple-backtick blocks (common)
    blocks = re.findall(r"```[\s\S]*?```", text)
    return dedupe_preserve_order(blocks)


def extract_urls(text: str) -> List[str]:
    # Avoid trailing punctuation that often follows URLs in prose.
    urls = re.findall(r"https?://[^\s\)\]\}<>\"']+", text)
    # Strip common trailing punctuation
    cleaned = [u.rstrip(".,;:!?") for u in urls]
    return dedupe_preserve_order(cleaned)


def extract_emails(text: str) -> List[str]:
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    return dedupe_preserve_order(emails)


def extract_times(text: str) -> List[str]:
    # 9:30, 09:30am, 9:30 a.m.
    times = re.findall(
        r"\b\d{1,2}:\d{2}(?:\s?(?:a\.?m\.?|p\.?m\.?))?\b",
        text,
        flags=re.IGNORECASE,
    )
    return dedupe_preserve_order(times)


def extract_dates(text: str) -> List[str]:
    dates: List[str] = []
    # ISO
    dates += re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)

    # Month Day, Year  (Jan 2, 2026) / (January 2 2026)
    dates += re.findall(
        rf"\b{MONTHS}\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,)?\s+\d{{4}}\b",
        text,
        flags=re.IGNORECASE,
    )

    # Day Month Year (2 Jan 2026)
    dates += re.findall(
        rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+{MONTHS}\s+\d{{4}}\b",
        text,
        flags=re.IGNORECASE,
    )

    # Quarter / year (Q4 2025)
    dates += re.findall(r"\bQ[1-4]\s+\d{4}\b", text, flags=re.IGNORECASE)

    # Month Year (Jan 2026) - soft; but include
    dates += re.findall(rf"\b{MONTHS}\s+\d{{4}}\b", text, flags=re.IGNORECASE)

    return dedupe_preserve_order([d.strip() for d in dates])


def extract_numbers(text: str) -> List[str]:
    nums: List[str] = []

    # Currency: $1,000.50
    # Currency: $1,000.50, $4.2M, $500K, $1.3 billion
    nums += re.findall(
        r"(?:[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:[KMBTkmbt])\b|(?:\s?(?:thousand|million|billion|trillion))\b)?)",
        text,
        flags=re.IGNORECASE,
    )

    # Percentages: 40%, 40 %
    nums += re.findall(r"\b\d[\d,]*(?:\.\d+)?\s?%\b", text)

    # Numeric ranges: 1-2, 1–2, 1 to 2, 1—2
    nums += re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:-|–|—|to)\s*\d+(?:\.\d+)?\b",
        text,
        flags=re.IGNORECASE,
    )

    # Versions: v2, v2.1.3
    nums += re.findall(r"\bv\d+(?:\.\d+){0,3}\b", text, flags=re.IGNORECASE)

    # Plain numbers: 1, 1,000, 3.14
    nums += re.findall(r"\b\d[\d,]*(?:\.\d+)?\b", text)

    cleaned = [n.strip() for n in nums]
    return dedupe_preserve_order(cleaned)


def extract_quotes(text: str) -> List[str]:
    quotes: List[str] = []
    # Double quotes, curly quotes
    for pat in [r"\"([^\"]{6,200})\"", r"“([^”]{6,200})”"]:
        for m in re.finditer(pat, text):
            inner = m.group(1).strip()
            # Avoid capturing simple fragments without spaces (e.g., a single word)
            if " " in inner or len(inner) > 30:
                quotes.append(m.group(0))  # include quote marks
    return dedupe_preserve_order(quotes)


def extract_possible_proper_nouns(text: str) -> List[str]:
    '''
    Heuristic: capture 2-4 word title-case sequences.
    This is not guaranteed correct; treat as a suggestion list.
    '''
    candidates: List[str] = []
    # Exclude sentence-start capitalization by requiring preceding char isn't sentence boundary/newline.
    for m in re.finditer(r"(?<![\.!\?\n])\s([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b", text):
        candidates.append(m.group(1).strip())
    return dedupe_preserve_order(candidates)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract must-keep constraints from text.")
    ap.add_argument("--in", dest="in_path", help="Input text file path")
    ap.add_argument("--stdin", action="store_true", help="Read input from stdin")
    ap.add_argument("--out", dest="out_path", help="Output JSON path (default: stdout)")
    args = ap.parse_args()

    text = read_text(args.in_path, args.stdin)

    constraints = {
        "input_sha256": sha256_text(text),
        "must_keep": {
            "urls": extract_urls(text),
            "emails": extract_emails(text),
            "times": extract_times(text),
            "dates": extract_dates(text),
            "numbers": extract_numbers(text),
            "quotes": extract_quotes(text),
            "code_blocks": find_code_blocks(text),
        },
        "candidates": {
            "possible_proper_nouns": extract_possible_proper_nouns(text),
        },
        "manual_additions": [],
        "notes": [
            "must_keep is extracted conservatively. Review and add missing proper nouns/product names to manual_additions.",
            "Validation scripts treat must_keep as strict (verbatim) matches.",
        ],
    }

    # Flatten must_keep for convenience.
    flat: List[str] = []
    for _, v in constraints["must_keep"].items():
        flat.extend(v)

    # Remove redundant bare numbers inside the per-category numbers list as well.
    corpus = dedupe_preserve_order(flat)
    if "numbers" in constraints["must_keep"]:
        constraints["must_keep"]["numbers"] = filter_bare_numbers_against_corpus(constraints["must_keep"]["numbers"], corpus)

    # Re-flatten after filtering.
    flat = []
    for _, v in constraints["must_keep"].items():
        flat.extend(v)

    constraints["must_keep_flat"] = filter_redundant_bare_numbers(flat)

    out = json.dumps(constraints, indent=2, ensure_ascii=False)

    if args.out_path:
        with open(args.out_path, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        import sys
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
