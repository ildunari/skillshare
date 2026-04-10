#!/usr/bin/env python3
'''
Scan text for banned phrases ("AI-isms") defined in references/taboo-phrases.md.

The taboo file contains machine-readable blocks:

  ## HARD_BANNED (machine-readable)
  phrase
  another phrase
  ## /HARD_BANNED

and similarly for SOFT_FLAGS.

This scanner ignores matches inside fenced code blocks and simple quoted strings.

Usage:
  python scripts/banned_phrase_scan.py --taboo references/taboo-phrases.md --in after.txt
  cat after.txt | python scripts/banned_phrase_scan.py --taboo references/taboo-phrases.md --stdin
'''
from __future__ import annotations

import argparse
import json
import re
from typing import Dict, List, Tuple


def read_text(path: str | None, stdin: bool) -> str:
    if stdin:
        import sys
        return sys.stdin.read()
    if not path:
        raise SystemExit("Provide --in <file> or --stdin")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()



def normalize_text(text: str) -> str:
    # Keep indices stable (1-char → 1-char replacements).
    return (
        text.replace("’", "'")
            .replace("‘", "'")
            .replace("“", '"')
            .replace("”", '"')
            .replace("–", "–")
            .replace("—", "—")
    )

def parse_block(md: str, start_marker: str, end_marker: str) -> List[str]:
    start = md.find(start_marker)
    end = md.find(end_marker)
    if start == -1 or end == -1 or end <= start:
        return []
    block = md[start + len(start_marker):end]
    lines = []
    for line in block.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        lines.append(s)
    return dedupe(lines)


def dedupe(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def ignore_spans(text: str) -> List[Tuple[int, int]]:
    spans: List[Tuple[int, int]] = []
    # fenced code blocks
    for m in re.finditer(r"```[\s\S]*?```", text):
        spans.append((m.start(), m.end()))
    # simple same-line quotes (avoid spanning newlines)
    for m in re.finditer(r"\"[^\"\n]{0,300}\"", text):
        spans.append((m.start(), m.end()))
    for m in re.finditer(r"“[^”\n]{0,300}”", text):
        spans.append((m.start(), m.end()))
    spans.sort()
    return spans


def in_any_span(i: int, spans: List[Tuple[int, int]]) -> bool:
    # spans are sorted; linear scan is fine (small).
    for a, b in spans:
        if a <= i < b:
            return True
    return False


def phrase_regex(phrase: str) -> re.Pattern:
    """Build a regex for a taboo phrase.

    Supports a few structural-pattern shorthands:
    - "not only...but also" style (two anchors with limited gap)
    - "from x to y" range constructions
    """
    phrase_norm = phrase.strip()

    # Structural shorthand: anchor...anchor
    if "..." in phrase_norm:
        a, b = [p.strip() for p in phrase_norm.split("...", 1)]
        a_parts = [re.escape(p) for p in a.split()]
        b_parts = [re.escape(p) for p in b.split()]
        a_rx = r"\b" + r"\s+".join(a_parts) + r"\b" if a_parts else ""
        b_rx = r"\b" + r"\s+".join(b_parts) + r"\b" if b_parts else ""
        # Allow a limited gap so we don't match across entire documents
        return re.compile(a_rx + r"[\s\S]{0,120}?" + b_rx, flags=re.IGNORECASE)

    # Structural shorthand: "from x to y"
    if phrase_norm.lower() == "from x to y":
        return re.compile(r"\bfrom\b[\s\S]{0,80}?\bto\b", flags=re.IGNORECASE)

    # Single word: word boundaries; multi-word: flexible whitespace between words
    if " " not in phrase_norm:
        return re.compile(rf"\b{re.escape(phrase_norm)}\b", flags=re.IGNORECASE)

    parts = [re.escape(p) for p in phrase_norm.split()]
    return re.compile(r"\b" + r"\s+".join(parts) + r"\b", flags=re.IGNORECASE)



def scan(text: str, phrases: List[str], spans: List[Tuple[int, int]]) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for phrase in phrases:
        rx = phrase_regex(phrase)
        matches = []
        ignored = 0
        for m in rx.finditer(text):
            if in_any_span(m.start(), spans):
                ignored += 1
                continue
            # context snippet
            a = max(0, m.start() - 40)
            b = min(len(text), m.end() + 40)
            snippet = text[a:b].replace("\n", " ")
            matches.append(snippet)
            if len(matches) >= 3:
                break
        total = len(list(rx.finditer(text)))
        if total - ignored > 0:
            results.append({
                "phrase": phrase,
                "count": total - ignored,
                "examples": matches,
                "ignored_in_code_or_quotes": ignored,
            })
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="Scan text for taboo phrases.")
    ap.add_argument("--taboo", required=True, help="Path to references/taboo-phrases.md")
    ap.add_argument("--in", dest="in_path", help="Text file path")
    ap.add_argument("--stdin", action="store_true", help="Read text from stdin")
    args = ap.parse_args()

    taboo_md = read_text(args.taboo, stdin=False)
    text = read_text(args.in_path, args.stdin)
    text = normalize_text(text)

    hard = parse_block(taboo_md, "## HARD_BANNED (machine-readable)", "## /HARD_BANNED")
    soft = parse_block(taboo_md, "## SOFT_FLAGS (machine-readable)", "## /SOFT_FLAGS")
    structural = parse_block(taboo_md, "## STRUCTURAL_FLAGS (machine-readable)", "## /STRUCTURAL_FLAGS")

    spans = ignore_spans(text)

    hard_hits = scan(text, hard, spans)
    soft_hits = scan(text, soft, spans)
    structural_hits = scan(text, structural, spans)

    out = {
        "hard_banned_hits": hard_hits,
        "soft_flag_hits": soft_hits,
        "structural_flag_hits": structural_hits,
        "hard_pass": len(hard_hits) == 0,
        "soft_pass": len(soft_hits) == 0,
        "structural_warn": len(structural_hits) > 0,
    }

    import sys
    sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
