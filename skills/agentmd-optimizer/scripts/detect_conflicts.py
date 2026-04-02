#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict

from _shared import load_json, write_json

TOPIC_PATTERNS = {
    "indentation": re.compile(r"indent|tabs?|spaces?", re.I),
    "verbosity": re.compile(r"concise|brief|verbose|detailed|short|long", re.I),
    "testing": re.compile(r"tests?|lint|typecheck|verify|validate", re.I),
    "tool-preference": re.compile(r"prefer .*cli|prefer .*mcp|prefer .*ssh|browser", re.I),
    "formatting": re.compile(r"markdown|bullet|prose|table|json", re.I),
}
POLARITY_POSITIVE = re.compile(r"\b(use|prefer|always|must|write|keep|run)\b", re.I)
POLARITY_NEGATIVE = re.compile(r"\b(avoid|never|do not|don't|skip)\b", re.I)


def topic_for(text: str) -> str | None:
    for topic, pattern in TOPIC_PATTERNS.items():
        if pattern.search(text):
            return topic
    return None


def polarity_for(text: str) -> str:
    neg = bool(POLARITY_NEGATIVE.search(text))
    pos = bool(POLARITY_POSITIVE.search(text))
    if neg and not pos:
        return "negative"
    if pos and not neg:
        return "positive"
    return "mixed"


def main():
    parser = argparse.ArgumentParser(description="Detect likely conflicts across extracted directives.")
    parser.add_argument("directive_index")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    data = load_json(args.directive_index)
    directives = data["directives"]
    by_topic = defaultdict(list)
    for d in directives:
        topic = topic_for(d["text"])
        if topic:
            by_topic[topic].append({**d, "polarity": polarity_for(d["text"])})

    conflicts = []
    for topic, items in by_topic.items():
        positives = [i for i in items if i["polarity"] == "positive"]
        negatives = [i for i in items if i["polarity"] == "negative"]
        if positives and negatives:
            conflicts.append({
                "topic": topic,
                "severity": "important",
                "positive_examples": positives[:5],
                "negative_examples": negatives[:5],
                "file_count": len({i['file'] for i in items}),
                "note": "Mixed positive/negative guidance found for the same topic. Review whether this is an intentional override or drift.",
            })

    payload = {
        "summary": {"conflict_count": len(conflicts)},
        "conflicts": sorted(conflicts, key=lambda c: c["file_count"], reverse=True),
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
