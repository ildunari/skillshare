#!/usr/bin/env python3
"""Audit GPT Image 2 prompts and parameters for common failure risks.

This script does not call an image API. It checks prompt/parameter shape so an
agent can catch avoidable problems before generation: invalid GPT Image 2 sizes,
transparency mismatch, chart/data risk, unsupported expectations, prompt bloat,
and text-in-image hazards.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Finding:
    severity: str
    category: str
    message: str
    fix: str


def parse_size(size: str | None) -> tuple[int, int] | None:
    if not size or size == "auto":
        return None
    match = re.fullmatch(r"(\d+)x(\d+)", size.strip())
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def audit_size(size: str | None, model: str) -> list[Finding]:
    findings: list[Finding] = []
    dims = parse_size(size)
    if not size or size == "auto":
        return findings
    if dims is None:
        findings.append(Finding(
            "error", "size", f"Size '{size}' is not in WIDTHxHEIGHT format.",
            "Use auto or a size like 1024x1024, 1536x1024, 1024x1536, 2048x1152, or 2560x1440.",
        ))
        return findings
    width, height = dims
    if model.startswith("gpt-image-2"):
        pixels = width * height
        ratio = max(width / height, height / width)
        if width % 16 or height % 16:
            findings.append(Finding(
                "error", "size", f"{width}x{height} is not a multiple of 16 in both dimensions.",
                "Round each dimension to the nearest multiple of 16.",
            ))
        if max(width, height) > 3840:
            findings.append(Finding(
                "error", "size", f"{width}x{height} exceeds the GPT Image 2 max edge of 3840 px.",
                "Use an edge at or below 3840 px.",
            ))
        if ratio > 3:
            findings.append(Finding(
                "error", "size", f"{width}x{height} has an aspect ratio greater than 3:1.",
                "Use a less extreme aspect ratio, such as 16:9, 3:2, 1:1, 2:3, or 9:16.",
            ))
        if pixels < 655_360 or pixels > 8_294_400:
            findings.append(Finding(
                "error", "size", f"{width}x{height} has {pixels:,} pixels, outside GPT Image 2 bounds.",
                "Use a total pixel count between 655,360 and 8,294,400.",
            ))
        if width > 2560 or height > 1440:
            findings.append(Finding(
                "warning", "size", f"{width}x{height} is above the commonly recommended 2560x1440 detail range.",
                "Use this only when extra detail is worth possible latency or experimental behavior.",
            ))
    return findings


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def audit_prompt(prompt: str, model: str, size: str | None, quality: str | None, output_format: str | None) -> list[Finding]:
    p = prompt.lower()
    findings: list[Finding] = []

    findings.extend(audit_size(size, model))

    words = re.findall(r"\b\w+\b", prompt)
    if len(words) > 350:
        findings.append(Finding(
            "warning", "prompt_length", f"Prompt is {len(words)} words; long prompts often contain conflicts or diluted priorities.",
            "Convert to labeled sections and remove low-value adjectives. Keep exact content and constraints separate.",
        ))

    if model.startswith("gpt-image-2") and has_any(p, [r"transparent", r"alpha channel", r"no background", r"checkerboard"]):
        findings.append(Finding(
            "warning", "transparency", "Prompt requests transparency, but GPT Image 2 does not support true transparent backgrounds in the API.",
            "Use a plain solid background for extraction, or add a separate background-removal/fallback step. Avoid asking for a checkerboard.",
        ))

    if has_any(p, [r"\bchart\b", r"\bgraph\b", r"\bplot\b", r"axis", r"data", r"table"]):
        if not re.search(r"\d", prompt):
            findings.append(Finding(
                "warning", "data", "Prompt asks for a chart/data graphic but contains no numeric data.",
                "Supply the exact data or use a conceptual infographic label. Generate exact charts with code when precision matters.",
            ))
        if has_any(p, [r"exact", r"accurate", r"real data", r"precise"]):
            findings.append(Finding(
                "warning", "data", "Exact chart/data accuracy is risky in image generation alone.",
                "Render the chart deterministically first, then preserve it during image editing or use generated art only around it.",
            ))

    exact_text_requested = has_any(p, [r"exact text", r"verbatim", r"copy", r"headline", r"label", r"typography", r"poster text", r"ui label"])
    quoted_chunks = re.findall(r"[\"“”'][^\"“”']{2,}[\"“”']", prompt)
    if exact_text_requested and not quoted_chunks:
        findings.append(Finding(
            "warning", "text", "Prompt appears to need exact rendered text but does not quote the exact words.",
            "Quote exact text and ask for it once, verbatim. Keep total copy short.",
        ))
    if len(quoted_chunks) > 8:
        findings.append(Finding(
            "warning", "text", f"Prompt contains {len(quoted_chunks)} quoted text chunks.",
            "For long copy, generate the visual/layout first and add text in a design tool.",
        ))

    if quality == "low" and has_any(p, [r"infographic", r"scientific", r"diagram", r"ui", r"mockup", r"small text", r"labels", r"poster"]):
        findings.append(Finding(
            "warning", "quality", "Low quality is likely to hurt text, labels, and dense layout work.",
            "Use medium for drafts and high for final diagrams, UI, charts, or text-heavy images.",
        ))

    if has_any(p, [r"sprite", r"pixel art"]):
        if not has_any(p, [r"grid", r"sheet", r"cell"]):
            findings.append(Finding(
                "warning", "sprites", "Sprite/pixel-art prompt does not specify a grid or cells.",
                "Specify rows/columns, equal cells, one centered sprite per cell, and a plain extraction-friendly background.",
            ))
        if has_any(p, [r"pixel art"]) and not has_any(p, [r"no anti-alias", r"no antialias", r"crisp", r"hard pixels"]):
            findings.append(Finding(
                "info", "sprites", "Pixel art prompt may benefit from crisp-pixel constraints.",
                "Add 'no anti-aliasing, no blur, crisp square pixels, limited palette'.",
            ))

    if has_any(p, [r"photoreal", r"photo", r"realistic"]) and has_any(p, [r"8k", r"hyperreal", r"ultra detailed", r"cinematic masterpiece"]):
        findings.append(Finding(
            "info", "realism", "Glossy booster terms can make everyday realism look like CGI.",
            "Use camera, lens, lighting, material, and ordinary imperfection cues instead.",
        ))

    if has_any(p, [r"medical", r"legal", r"diagnosis", r"treatment", r"scientific claim", r"statistic"]):
        findings.append(Finding(
            "info", "claims", "Prompt may contain factual or high-stakes claims.",
            "Verify claims outside the image model and include only source-supplied text. Keep the visual educational, not advisory.",
        ))

    if output_format and output_format.lower() == "jpeg" and has_any(p, [r"text", r"labels", r"diagram", r"ui", r"icon", r"sprite"]):
        findings.append(Finding(
            "info", "format", "JPEG can add compression artifacts to text, icons, sprites, and diagrams.",
            "Prefer PNG or WebP for sharp graphics unless speed/file size is more important.",
        ))

    if has_any(p, [r"style of", r"in the style of", r"like .*artist", r"copy .*logo", r"disney", r"marvel", r"pokemon"]):
        findings.append(Finding(
            "warning", "rights", "Prompt may ask for protected style, logos, or existing characters.",
            "Use broad visual traits and original characters/marks instead of copying protected material.",
        ))

    if not findings:
        findings.append(Finding(
            "ok", "summary", "No obvious prompt or parameter risks found.",
            "Generate a small batch, inspect, then iterate with targeted edits.",
        ))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit GPT Image 2 prompts for common failure risks.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", help="Prompt text to audit")
    group.add_argument("--prompt-file", help="File containing prompt text")
    parser.add_argument("--model", default="gpt-image-2", help="Image model name, default: gpt-image-2")
    parser.add_argument("--size", default="auto", help="Requested size, e.g. 1536x1024 or auto")
    parser.add_argument("--quality", choices=["low", "medium", "high", "auto"], default="auto")
    parser.add_argument("--output-format", choices=["png", "jpeg", "webp"], default="png")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text")
    args = parser.parse_args(argv)

    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    else:
        prompt = args.prompt or ""

    findings = audit_prompt(prompt, args.model, args.size, args.quality, args.output_format)

    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print("Image prompt audit")
        print(f"model={args.model} size={args.size} quality={args.quality} output_format={args.output_format}")
        for finding in findings:
            label = finding.severity.upper()
            print(f"\n[{label}] {finding.category}: {finding.message}")
            print(f"Fix: {finding.fix}")

    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
