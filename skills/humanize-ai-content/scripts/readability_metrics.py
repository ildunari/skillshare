#!/usr/bin/env python3
'''
Compute lightweight readability and "rhythm" metrics.

This is not a full NLP pipeline; it's a deterministic signal to detect:
- monotone sentence length
- overly long sentences
- basic readability (Flesch / Flesch-Kincaid)
- repeated n-grams and sentence starters

The metrics are intended for humanization QA, not academic evaluation.

Usage:
  python scripts/readability_metrics.py --in after.txt
  cat after.txt | python scripts/readability_metrics.py --stdin
'''
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import Counter
from typing import List, Tuple


def read_text(path: str | None, stdin: bool) -> str:
    if stdin:
        import sys
        return sys.stdin.read()
    if not path:
        raise SystemExit("Provide --in <file> or --stdin")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```[\s\S]*?```", " ", text)


def split_sentences(text: str) -> List[str]:
    # Basic sentence splitter: punctuation boundaries + newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    sentences = [p.strip() for p in parts if p.strip()]
    return sentences


def words_in(text: str) -> List[str]:
    # Keep contractions; drop punctuation.
    return re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text)


VOWELS = "aeiouy"


def count_syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1

    # vowel groups
    groups = re.findall(r"[aeiouy]+", w)
    syll = len(groups)

    # silent 'e'
    if w.endswith("e") and not w.endswith("le"):
        syll -= 1

    # 'le' ending (table, little) where preceding char isn't vowel
    if w.endswith("le") and len(w) > 2 and w[-3] not in VOWELS:
        syll += 1

    return max(1, syll)


def flesch_reading_ease(words: int, sentences: int, syllables: int) -> float:
    if words == 0 or sentences == 0:
        return 0.0
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)


def flesch_kincaid_grade(words: int, sentences: int, syllables: int) -> float:
    if words == 0 or sentences == 0:
        return 0.0
    return 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59


def trigram_stats(words: List[str]) -> Tuple[float, List[Tuple[str, int]]]:
    ws = [w.lower() for w in words]
    if len(ws) < 3:
        return 0.0, []
    trigrams = [" ".join(ws[i:i+3]) for i in range(len(ws) - 2)]
    total = len(trigrams)
    counts = Counter(trigrams)
    unique = len(counts)
    repetition_ratio = 1.0 - (unique / total) if total else 0.0
    top = [(t, c) for t, c in counts.most_common(10) if c >= 3]
    return repetition_ratio, top


def main() -> None:
    ap = argparse.ArgumentParser(description="Readability and rhythm metrics.")
    ap.add_argument("--in", dest="in_path", help="Text file path")
    ap.add_argument("--stdin", action="store_true", help="Read text from stdin")
    args = ap.parse_args()

    raw = read_text(args.in_path, args.stdin)
    text = strip_code_blocks(raw)

    sentences = split_sentences(text)
    sent_words = [words_in(s) for s in sentences]
    sent_lens = [len(ws) for ws in sent_words if ws]

    all_words = [w for ws in sent_words for w in ws]
    word_count = len(all_words)
    sentence_count = len([s for s in sentences if s.strip()])

    syllables = sum(count_syllables(w) for w in all_words)

    avg_len = statistics.mean(sent_lens) if sent_lens else 0.0
    stdev_len = statistics.pstdev(sent_lens) if len(sent_lens) >= 2 else 0.0
    min_len = min(sent_lens) if sent_lens else 0
    max_len = max(sent_lens) if sent_lens else 0

    # Target range heuristic: most sentences in 8–25 words.
    in_range = [l for l in sent_lens if 8 <= l <= 25]
    pct_in_range = (len(in_range) / len(sent_lens) * 100.0) if sent_lens else 0.0

    # Monotony: too many sentences near the median length.
    if sent_lens:
        med = statistics.median(sent_lens)
        near_med = [l for l in sent_lens if abs(l - med) <= 2]
        pct_near_median = len(near_med) / len(sent_lens) * 100.0
    else:
        med = 0.0
        pct_near_median = 0.0

    rep_ratio, top_trigrams = trigram_stats(all_words)

    starters = [ws[0].lower() for ws in sent_words if ws]
    top_starters = Counter(starters).most_common(10)


    # Structural signals (lightweight heuristics)
    # Note: these are not "grammar rules" — they're tell detectors.
    em_dash_count = text.count("—") + text.count("–") + text.count("--")
    em_dash_density_per_500_words = (em_dash_count / word_count * 500.0) if word_count else 0.0

    participial_phrase_count = len(re.findall(r",\s+[A-Za-z]{2,}ing\b", text))
    sentence_initial_ing_count = 0
    for s in sentences:
        s_strip = s.strip()
        if re.match(r"^[A-Za-z]{2,}ing\b", s_strip, flags=re.IGNORECASE):
            sentence_initial_ing_count += 1

    tricolon_count_estimate = len(
        re.findall(r"\b[^\n,]{2,},\s+[^\n,]{2,},\s+(?:and|or)\s+[^\n.]{2,}", text, flags=re.IGNORECASE)
    )

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n"))
        if p.strip()
    ]
    para_word_counts = [len(re.findall(r"\b\w+\b", p)) for p in paragraphs]
    para_stdev = statistics.pstdev(para_word_counts) if len(para_word_counts) >= 2 else 0.0

    para_openers: List[str] = []
    for p in paragraphs:
        m = re.search(r"\b([A-Za-z']+)\b", p)
        if m:
            para_openers.append(m.group(1).lower())
    top_para_openers = Counter(para_openers).most_common(10)

    para_opener_repeat_ratio = 0.0
    if para_openers:
        para_opener_repeat_ratio = max(Counter(para_openers).values()) / len(para_openers)

    structural_flags = {
        "em_dash_count": em_dash_count,
        "em_dash_density_per_500_words": round(em_dash_density_per_500_words, 3),
        "participial_phrase_count": participial_phrase_count,
        "sentence_initial_ing_count": sentence_initial_ing_count,
        "tricolon_count_estimate": tricolon_count_estimate,
        "paragraph_count": len(paragraphs),
        "paragraph_word_count_stdev": round(para_stdev, 3),
        "top_paragraph_openers": top_para_openers,
        "flags": {
            "em_dash_overuse": em_dash_density_per_500_words > 2.0 and word_count >= 200,
            "participial_overuse": participial_phrase_count >= 3 and sentence_count >= 6,
            "hyper_symmetry": para_stdev < 5 and len(para_word_counts) >= 3,
            "paragraph_opener_repetition": para_opener_repeat_ratio >= 0.4 and len(para_openers) >= 5,
        },
    }


    out = {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "structural_flags": structural_flags,
        "sentence_length_words": {
            "avg": round(avg_len, 2),
            "stdev": round(stdev_len, 2),
            "min": min_len,
            "median": med,
            "max": max_len,
            "pct_in_8_to_25": round(pct_in_range, 2),
            "pct_within_2_of_median": round(pct_near_median, 2),
        },
        "readability": {
            "flesch_reading_ease": round(flesch_reading_ease(word_count, sentence_count, syllables), 2),
            "flesch_kincaid_grade": round(flesch_kincaid_grade(word_count, sentence_count, syllables), 2),
            "syllables": syllables,
        },
        "repetition": {
            "trigram_repetition_ratio": round(rep_ratio, 4),
            "top_trigrams": top_trigrams,
            "top_sentence_starters": top_starters,
        },
        "flags": {
            "low_sentence_length_variance": stdev_len < 4 and sentence_count >= 6,
            "very_long_sentence_present": max_len >= 35,
            "monotone_pacing": pct_near_median >= 70 and sentence_count >= 6,
        },
    }

    import sys
    sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
