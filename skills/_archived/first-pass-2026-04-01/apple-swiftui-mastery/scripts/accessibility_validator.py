#!/usr/bin/env python3
"""
accessibility_validator.py

Check SwiftUI files for basic accessibility compliance.  It scans for interactive
elements (Button, Toggle, TextField, Image) and ensures they provide an
`accessibilityLabel` or `accessibilityHidden` modifier.  The tool is heuristic and
should not replace manual accessibility testing with VoiceOver.

Usage:
    python accessibility_validator.py MyView.swift
"""
import argparse
import re


INTERACTIVE_ELEMENTS = ["Button", "Toggle", "TextField", "Slider"]


class Issue:
    def __init__(self, line_no: int, message: str):
        self.line_no = line_no
        self.message = message

    def __str__(self):
        return f"Line {self.line_no}: {self.message}"


def validate_file(path: str) -> list[Issue]:
    issues: list[Issue] = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        for element in INTERACTIVE_ELEMENTS:
            pattern = rf"{element}\s*\("
            if re.search(pattern, stripped):
                # Check subsequent lines for accessibility modifiers
                has_label = False
                j = i
                while j < len(lines) and lines[j].strip().endswith('{') is False:
                    # search until the start of closure body
                    j += 1
                # look ahead a few lines for .accessibilityLabel or .accessibilityHidden
                for k in range(j, min(len(lines), j + 10)):
                    if '.accessibility' in lines[k]:
                        has_label = True
                        break
                if not has_label:
                    issues.append(Issue(i, f"{element} may require an accessibilityLabel or accessibilityHidden modifier."))
    # Check for Images without labels
    for i, line in enumerate(lines, start=1):
        if re.search(r"Image\s*\(", line):
            if '.accessibilityHidden' not in line and '.accessibilityLabel' not in line:
                issues.append(Issue(i, "Image should provide an accessibility label or be hidden from assistive technologies."))
    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate SwiftUI views for accessibility labels and hints.")
    parser.add_argument("file", help="Path to the SwiftUI file to validate")
    args = parser.parse_args()

    issues = validate_file(args.file)
    if not issues:
        print("No accessibility issues found.")
    else:
        for issue in issues:
            print(issue)


if __name__ == '__main__':
    main()