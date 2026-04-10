#!/usr/bin/env python3
'''
Guardrail: flag if the rewrite changed "too much".

This uses difflib.SequenceMatcher similarity:
  similarity = ratio in [0,1]
  changed_percent = 1 - similarity

This is a blunt instrument. It's meant to catch cases where the rewrite turned into
a new message (even if facts were preserved).

Usage:
  python scripts/diff_check.py --before before.txt --after after.txt --max-change 0.40
'''
from __future__ import annotations

import argparse
import json
import re
import difflib


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def normalize(s: str) -> str:
    # Collapse whitespace for a more stable similarity score
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def main() -> None:
    ap = argparse.ArgumentParser(description="Diff guardrail for rewrites.")
    ap.add_argument("--before", required=True, help="Path to original text")
    ap.add_argument("--after", required=True, help="Path to rewritten text")
    ap.add_argument("--max-change", type=float, default=0.40, help="Max allowed change fraction (default 0.40)")
    args = ap.parse_args()

    before = normalize(read_file(args.before))
    after = normalize(read_file(args.after))

    char_sim = ratio(before, after)
    char_changed = 1.0 - char_sim

    # Word-level similarity
    before_words = before.split()
    after_words = after.split()

    before_word_count = len(before_words)
    after_word_count = len(after_words)
    length_ratio = (after_word_count / before_word_count) if before_word_count else 0.0
    length_warn = (length_ratio > 1.3) or (before_word_count > 0 and length_ratio < 0.6)
    word_sim = ratio(" ".join(before_words), " ".join(after_words))
    word_changed = 1.0 - word_sim

    out = {
        "max_change": args.max_change,
        "before_word_count": before_word_count,
        "after_word_count": after_word_count,
        "length_ratio": round(length_ratio, 4),
        "length_warn": length_warn,
        "char_similarity": round(char_sim, 4),
        "char_changed_percent": round(char_changed, 4),
        "word_similarity": round(word_sim, 4),
        "word_changed_percent": round(word_changed, 4),
        "pass": char_changed <= args.max_change,
    }

    import sys
    sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
