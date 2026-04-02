#!/usr/bin/env python3
"""
view_analyzer.py

Analyse SwiftUI view files for common performance issues and anti‑patterns.

This tool reads a Swift source file and uses heuristic checks to identify potential
problems, such as long‑running work inside `body`, misuse of @ObservedObject, unbounded
GeometryReader usage and conditional branches returning different view types.

Usage:
    python view_analyzer.py path/to/ViewFile.swift
"""
import argparse
import re
import sys


class Warning:
    def __init__(self, line_no: int, message: str):
        self.line_no = line_no
        self.message = message

    def __str__(self):
        return f"Line {self.line_no}: {self.message}"


def analyse_file(path: str) -> list[Warning]:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    warnings: list[Warning] = []
    code = ''.join(lines)
    # Check for URLSession or network calls inside body
    body_pattern = re.compile(r"var\s+body\s*:\s*some\s+View\s*\{", re.MULTILINE)
    for i, line in enumerate(lines, start=1):
        if 'URLSession' in line and 'body' in code[:code.find(line)]:
            warnings.append(Warning(i, "Possible network call inside body; perform side effects in task or view model."))
    # Check for DateFormatter instantiation in body
    for i, line in enumerate(lines, start=1):
        if re.search(r"DateFormatter\s*\(", line):
            warnings.append(Warning(i, "Creating DateFormatter inside body; cache formatters outside of body."))
    # Check for @ObservedObject instantiation
    for i, line in enumerate(lines, start=1):
        if re.search(r"@ObservedObject\s+var\s+\w+\s*=", line):
            warnings.append(Warning(i, "@ObservedObject should not instantiate its own model; use @StateObject instead."))
    # Check for unconditional GeometryReader without frame constraints
    for i, line in enumerate(lines, start=1):
        if 'GeometryReader' in line:
            # Look ahead few lines for .frame
            has_frame = False
            for j in range(i, min(len(lines), i + 5)):
                if '.frame' in lines[j]:
                    has_frame = True
                    break
            if not has_frame:
                warnings.append(Warning(i, "GeometryReader without explicit frame may take all available space; consider constraining it."))
    # Check for AnyView usage
    for i, line in enumerate(lines, start=1):
        if 'AnyView(' in line:
            warnings.append(Warning(i, "Using AnyView erases type information and can impact performance; consider alternatives."))
    # Check for conditionals returning different types in body
    # If there is 'if' inside body and lines contain both Text and Image or different SwiftUI types
    in_body = False
    body_indent = None
    branch_types = set()
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith('var body'):
            in_body = True
            body_indent = len(line) - len(line.lstrip())
            continue
        if in_body:
            indent = len(line) - len(line.lstrip())
            # End of body
            if indent < body_indent and stripped == '}' and body_indent is not None:
                in_body = False
                if len(branch_types) > 1:
                    warnings.append(Warning(i, f"Different view types in conditional branches: {branch_types}. This affects view identity and animations."))
                branch_types = set()
                continue
            if 'if ' in stripped or 'else' in stripped:
                continue
            # Collect view type names: simplified heuristic based on capitalised word at start
            match = re.match(r"([A-Z][A-Za-z0-9_]*)\(", stripped)
            if match:
                branch_types.add(match.group(1))
    # Check ForEach without id for identifiable data
    for i, line in enumerate(lines, start=1):
        if re.search(r"ForEach\s*\(.*in", line) and '.id(' not in line:
            warnings.append(Warning(i, "ForEach missing .id() parameter; this may cause identity issues."))
    return warnings


def main():
    parser = argparse.ArgumentParser(description="Analyse SwiftUI view for anti-patterns and performance issues.")
    parser.add_argument("file", help="Path to the SwiftUI view file")
    args = parser.parse_args()

    warnings = analyse_file(args.file)
    if not warnings:
        print("No issues detected.")
        sys.exit(0)
    for w in warnings:
        print(w)
    sys.exit(1)


if __name__ == '__main__':
    main()