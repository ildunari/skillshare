#!/usr/bin/env python3
"""
Deep Research Prompt Validator

Checks completed research prompts against the quality checklist.
Run on a markdown file containing one or more research prompts.

Usage:
    python prompt-validator.py <prompt_file.md>
    python prompt-validator.py --stdin < prompt_file.md
"""

import sys
import re
import os


def read_input():
    if len(sys.argv) > 1 and sys.argv[1] != "--stdin":
        with open(sys.argv[1], "r") as f:
            return f.read()
    else:
        return sys.stdin.read()


def split_prompts(text):
    """Split a multi-prompt file into individual prompts."""
    parts = re.split(r"^# PROMPT\b", text, flags=re.MULTILINE)
    prompts = []
    for part in parts:
        part = part.strip()
        if part:
            prompts.append("# PROMPT" + part if not part.startswith("# PROMPT") else part)
    if not prompts:
        prompts = [text]
    return prompts


def check_prompt(text, prompt_num=1):
    """Run all quality checks on a single prompt. Returns list of (status, check_name, detail)."""
    results = []
    text_lower = text.lower()
    word_count = len(text.split())

    # 1. Mandatory sections present
    sections = {
        "Context": bool(re.search(r"^##\s*Context", text, re.MULTILINE)),
        "Knowledge Gap": bool(re.search(r"^##\s*Knowledge Gap", text, re.MULTILINE)),
        "Focus Areas": bool(re.search(r"^##\s*Focus Area", text, re.MULTILINE)),
        "Reporting Requirements": bool(re.search(r"^##\s*Report", text, re.MULTILINE)),
        "Prioritized Sources": bool(re.search(r"^##\s*(Prioritized )?Source", text, re.MULTILINE)),
        "Usage Notes": bool(re.search(r"^##\s*Usage", text, re.MULTILINE)),
    }
    for section, present in sections.items():
        if present:
            results.append(("PASS", f"Section: {section}", "Present"))
        else:
            results.append(("FAIL", f"Section: {section}", "Missing — add this section"))

    # 2. Focus area count
    focus_items = re.findall(r"^- \*\*[^*]+\*\*", text, re.MULTILINE)
    fa_count = len(focus_items)
    if fa_count == 0:
        results.append(("FAIL", "Focus area count", "No bold-labeled focus areas found"))
    elif fa_count < 4:
        results.append(("WARN", "Focus area count", f"Only {fa_count} focus areas — consider adding more (4-10 recommended)"))
    elif fa_count > 10:
        results.append(("WARN", "Focus area count", f"{fa_count} focus areas — consider consolidating (4-10 recommended)"))
    else:
        results.append(("PASS", "Focus area count", f"{fa_count} focus areas"))

    # 3. Focus area depth (check if any are too short — likely headers not interrogations)
    shallow_count = 0
    for item in focus_items:
        start = text.find(item)
        # Find the next focus area or section to measure length
        next_item_pos = len(text)
        for other in focus_items:
            other_pos = text.find(other, start + 1)
            if other_pos > start and other_pos < next_item_pos:
                next_item_pos = other_pos
        next_section = re.search(r"^##\s", text[start + 1:], re.MULTILINE)
        if next_section:
            next_section_pos = start + 1 + next_section.start()
            next_item_pos = min(next_item_pos, next_section_pos)
        area_text = text[start:next_item_pos]
        area_words = len(area_text.split())
        if area_words < 50:
            shallow_count += 1

    if shallow_count > 0:
        results.append(("WARN", "Focus area depth",
                         f"{shallow_count} focus area(s) under 50 words — likely headers, not interrogation-style paragraphs. "
                         "See references/focus-area-writing-guide.md"))
    else:
        results.append(("PASS", "Focus area depth", "All focus areas have sufficient depth"))

    # 4. Reporting requirements checks
    has_reporting = bool(re.search(r"^##\s*Report", text, re.MULTILINE))
    if has_reporting:
        reporting_section = text[re.search(r"^##\s*Report", text, re.MULTILINE).start():]
        next_h2 = re.search(r"^##\s", reporting_section[3:], re.MULTILINE)
        if next_h2:
            reporting_section = reporting_section[:3 + next_h2.start()]

        # Word target
        has_word_target = bool(re.search(r"\d[\d,]*\s*(-|–|to)\s*\d[\d,]*\s*word", reporting_section, re.IGNORECASE))
        if has_word_target:
            results.append(("PASS", "Word target", "Present in reporting requirements"))
        else:
            results.append(("FAIL", "Word target", "No word target found — add one (e.g., 'Target 8,000-15,000 words')"))

        # Minimum deliverables
        has_deliverables = bool(re.search(r"include at minimum|at minimum|minimum:", reporting_section, re.IGNORECASE))
        if has_deliverables:
            # Count deliverable items
            deliverable_lines = re.findall(r"^- .+", reporting_section, re.MULTILINE)
            results.append(("PASS", "Minimum deliverables", f"Present ({len(deliverable_lines)} items)"))
        else:
            results.append(("FAIL", "Minimum deliverables",
                             "No 'include at minimum' section — add countable deliverables"))

        # Anti-padding rules
        has_do_not = bool(re.search(r"do not:|don't:", reporting_section, re.IGNORECASE))
        if has_do_not:
            results.append(("PASS", "Anti-padding rules", "'Do not' section present"))
        else:
            results.append(("FAIL", "Anti-padding rules",
                             "No 'Do not' section — add explicit exclusions"))

        # Depth over breadth
        has_depth = bool(re.search(r"depth over breadth|prioritize depth", reporting_section, re.IGNORECASE))
        if has_depth:
            results.append(("PASS", "Depth instruction", "'Prioritize depth over breadth' present"))
        else:
            results.append(("WARN", "Depth instruction",
                             "Consider adding 'Prioritize depth over breadth' instruction"))
    else:
        results.append(("FAIL", "Word target", "No reporting requirements section"))
        results.append(("FAIL", "Minimum deliverables", "No reporting requirements section"))
        results.append(("FAIL", "Anti-padding rules", "No reporting requirements section"))

    # 5. Source tiering
    has_tiers = bool(re.search(r"tier\s*[1-4]|search first|gold mine|highest value", text_lower))
    if has_tiers:
        results.append(("PASS", "Source tiering", "Sources appear to be tiered"))
    else:
        results.append(("WARN", "Source tiering",
                         "Sources may not be tiered — consider Tier 1/2/3/4 structure"))

    # 6. Invite surprise
    surprise_patterns = [
        r"surface.{0,30}(approach|technique|pattern|behavior)",
        r"follow.{0,20}interesting.{0,10}thread",
        r"might not.{0,10}(know|aware|expect)",
        r"i might not be aware",
    ]
    has_surprise = any(re.search(p, text_lower) for p in surprise_patterns)
    if has_surprise:
        results.append(("PASS", "Invite surprise", "Surprise invitation present"))
    else:
        results.append(("WARN", "Invite surprise",
                         "No 'invite surprise' signal — add 'Surface approaches I might not be aware of'"))

    # 7. Fallback priority
    has_fallback = bool(re.search(r"(if.{0,30}(hit|reach).{0,20}limit|prioritize.{0,20}order|priority.{0,10}order)",
                                   text_lower))
    if has_fallback:
        results.append(("PASS", "Fallback priority", "Fallback priority ordering present"))
    else:
        results.append(("WARN", "Fallback priority",
                         "No fallback priority ordering in usage notes"))

    # 8. Before/after demand
    has_before_after = bool(re.search(r"before.{0,5}(/|and).{0,5}after", text_lower))
    if has_before_after:
        results.append(("PASS", "Before/after demand", "Before/after comparison requested"))
    else:
        results.append(("WARN", "Before/after demand",
                         "No before/after comparison requested — this is the strongest depth driver"))

    # 9. Failure mode question
    failure_patterns = [
        r"failure (mode|case|stud)",
        r"what (break|fail|cause|goes wrong)",
        r"anti.?pattern",
        r"known (issue|gotcha|problem|bug)",
    ]
    has_failure = any(re.search(p, text_lower) for p in failure_patterns)
    if has_failure:
        results.append(("PASS", "Failure mode coverage", "Failure modes / anti-patterns addressed"))
    else:
        results.append(("WARN", "Failure mode coverage",
                         "No failure mode or anti-pattern questions — consider adding"))

    # 10. Expertise level stated
    expertise_patterns = [
        r"skip beginner",
        r"experienced.{0,20}(engineer|developer|practitioner|researcher|user)",
        r"practitioner.{0,5}(grade|level)",
        r"i('m| am) (an |a )?(experienced|senior|advanced)",
    ]
    has_expertise = any(re.search(p, text_lower) for p in expertise_patterns)
    if has_expertise:
        results.append(("PASS", "Expertise level", "Expertise level stated"))
    else:
        results.append(("WARN", "Expertise level",
                         "Expertise level not clearly stated — add to prevent beginner-level output"))

    return results


def print_results(results, prompt_num=1, prompt_count=1):
    prefix = f"Prompt {prompt_num}" if prompt_count > 1 else "Prompt"

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    passes = [r for r in results if r[0] == "PASS"]

    print(f"\n{'='*60}")
    print(f"  {prefix} Quality Report")
    print(f"{'='*60}")
    print(f"  PASS: {len(passes)}  |  WARN: {len(warns)}  |  FAIL: {len(fails)}")
    print(f"{'='*60}\n")

    if fails:
        print("FAILURES (must fix):")
        for _, name, detail in fails:
            print(f"  FAIL  {name}")
            print(f"        {detail}")
        print()

    if warns:
        print("WARNINGS (should fix):")
        for _, name, detail in warns:
            print(f"  WARN  {name}")
            print(f"        {detail}")
        print()

    if passes:
        print("PASSING:")
        for _, name, detail in passes:
            print(f"  PASS  {name}")
        print()

    # Overall verdict
    if len(fails) == 0 and len(warns) <= 2:
        print("VERDICT: Ready to run")
    elif len(fails) == 0:
        print("VERDICT: Runnable with improvements suggested")
    elif len(fails) <= 2:
        print("VERDICT: Fix failures before running")
    else:
        print("VERDICT: Needs significant work — see failures above")


def main():
    text = read_input()
    if not text.strip():
        print("Error: No input provided")
        print("Usage: python prompt-validator.py <file.md>")
        print("   or: python prompt-validator.py --stdin < file.md")
        sys.exit(1)

    prompts = split_prompts(text)

    for i, prompt in enumerate(prompts, 1):
        results = check_prompt(prompt, i)
        print_results(results, i, len(prompts))

    # Summary for multi-prompt files
    if len(prompts) > 1:
        print(f"\n{'='*60}")
        print(f"  Validated {len(prompts)} prompts")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
