#!/usr/bin/env python3
"""
dtcg_to_sd.py — Convert DTCG 2025.10 tokens to Style Dictionary format.

SD v4 natively reads DTCG ($value/$type/$description), so this converter
is primarily useful for:
  1. Extracting tokens from a full design-spec.json into standalone token files
  2. Expanding composite tokens (typography → individual tokens) for tools that can't handle composites
  3. Stripping tokenMeta / validation / non-token fields
  4. Converting between DTCG and legacy SD format if needed

Usage:
  python dtcg_to_sd.py <design_spec.json> [--output tokens/] [--expand-composites] [--legacy]
"""

import json
import sys
import os
from pathlib import Path


def extract_tokens_from_spec(spec: dict) -> dict:
    """Extract just the tokens tree from a full design-spec.json."""
    return spec.get("tokens", spec)


def expand_composites(tokens: dict, prefix: str = "") -> dict:
    """Expand composite tokens (typography, shadow) into individual tokens."""
    result = {}

    for key, value in tokens.items():
        if key.startswith("$"):
            result[key] = value
            continue

        path = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            if "$value" in value and "$type" in value:
                token_type = value["$type"]
                token_value = value["$value"]

                if token_type == "typography" and isinstance(token_value, dict):
                    # Expand typography into individual tokens
                    group = {}
                    if "fontFamily" in token_value:
                        family = token_value["fontFamily"]
                        if isinstance(family, list):
                            family = ", ".join(family)
                        group["fontFamily"] = {
                            "$type": "fontFamily",
                            "$value": family,
                        }
                    if "fontSize" in token_value:
                        group["fontSize"] = {
                            "$type": "dimension",
                            "$value": token_value["fontSize"],
                        }
                    if "fontWeight" in token_value:
                        group["fontWeight"] = {
                            "$type": "fontWeight",
                            "$value": token_value["fontWeight"],
                        }
                    if "lineHeight" in token_value:
                        group["lineHeight"] = {
                            "$type": "dimension",
                            "$value": token_value["lineHeight"],
                        }
                    if "letterSpacing" in token_value:
                        group["letterSpacing"] = {
                            "$type": "dimension",
                            "$value": token_value["letterSpacing"],
                        }
                    # Keep the composite too
                    group["_composite"] = value
                    if "$description" in value:
                        for sub in group.values():
                            if isinstance(sub, dict) and "$type" in sub:
                                sub.setdefault("$description", value["$description"])
                    result[key] = group

                elif token_type == "shadow" and isinstance(token_value, dict):
                    # Keep shadow as-is (SD v4 handles composite shadows)
                    result[key] = value
                else:
                    result[key] = value
            else:
                # Recurse into groups
                result[key] = expand_composites(value, path)
        else:
            result[key] = value

    return result


def to_legacy_format(tokens: dict) -> dict:
    """Convert DTCG ($value/$type) to legacy SD format (value/type)."""
    result = {}

    for key, value in tokens.items():
        if key.startswith("$"):
            # Map DTCG keys to legacy
            if key == "$value":
                result["value"] = value
            elif key == "$type":
                result["type"] = value
            elif key == "$description":
                result["comment"] = value
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = to_legacy_format(value)
        else:
            result[key] = value

    return result


def split_by_category(tokens: dict) -> dict[str, dict]:
    """Split token tree into separate files by top-level category."""
    files = {}
    for key, value in tokens.items():
        if key.startswith("$"):
            continue
        if isinstance(value, dict):
            files[key] = {key: value}
    return files


def main():
    if len(sys.argv) < 2:
        print("Usage: python dtcg_to_sd.py <spec.json> [--output dir/] [--expand-composites] [--legacy] [--split]", file=sys.stderr)
        sys.exit(1)

    spec_path = sys.argv[1]
    args = sys.argv[2:]

    output_dir = "tokens"
    do_expand = "--expand-composites" in args
    do_legacy = "--legacy" in args
    do_split = "--split" in args

    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_dir = args[idx + 1]

    with open(spec_path) as f:
        spec = json.load(f)

    tokens = extract_tokens_from_spec(spec)

    if do_expand:
        tokens = expand_composites(tokens)

    if do_legacy:
        tokens = to_legacy_format(tokens)

    os.makedirs(output_dir, exist_ok=True)

    if do_split:
        files = split_by_category(tokens)
        for category, content in files.items():
            out_path = Path(output_dir) / f"{category}.json"
            with open(out_path, "w") as f:
                json.dump(content, f, indent=2)
            print(f"  → {out_path}")
    else:
        out_path = Path(output_dir) / "tokens.json"
        with open(out_path, "w") as f:
            json.dump(tokens, f, indent=2)
        print(f"  → {out_path}")

    print(f"✓ Converted {spec_path} → {output_dir}/")


if __name__ == "__main__":
    main()
