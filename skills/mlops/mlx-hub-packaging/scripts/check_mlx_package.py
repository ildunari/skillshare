#!/usr/bin/env python3
"""Check that an MLX model package contains expected non-weight files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List

REQUIRED_BY_TASK: Dict[str, List[str]] = {
    "llm": ["config.json", "tokenizer_config.json"],
    "vlm": ["config.json", "tokenizer_config.json"],
    "embedding": ["config.json"],
    "reranker": ["config.json"],
}
RECOMMENDED_BY_TASK: Dict[str, List[str]] = {
    "llm": ["generation_config.json", "tokenizer.json", "special_tokens_map.json", "README.md"],
    "vlm": ["processor_config.json", "preprocessor_config.json", "image_processor_config.json", "generation_config.json", "tokenizer.json", "special_tokens_map.json", "README.md"],
    "embedding": ["tokenizer_config.json", "tokenizer.json", "README.md"],
    "reranker": ["tokenizer_config.json", "tokenizer.json", "README.md"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check MLX package contents.")
    parser.add_argument("path", help="Model package directory")
    parser.add_argument("--task", choices=sorted(REQUIRED_BY_TASK), default="llm")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_dir():
        print(f"FAIL: not a directory: {path}", file=sys.stderr)
        return 1

    files = {p.name for p in path.iterdir() if p.is_file()}
    weight_files = [p.name for p in path.iterdir() if p.is_file() and p.name.endswith((".safetensors", ".bin"))]
    missing_required = [name for name in REQUIRED_BY_TASK[args.task] if name not in files]
    missing_recommended = [name for name in RECOMMENDED_BY_TASK[args.task] if name not in files]

    if not weight_files:
        print("FAIL: no weight files found", file=sys.stderr)
        return 1
    if missing_required:
        print(f"FAIL: missing required files: {', '.join(missing_required)}", file=sys.stderr)
        return 1

    print("PASS: required files present")
    print(f"weight_files={len(weight_files)}")
    if missing_recommended:
        print("WARN: missing recommended files: " + ", ".join(missing_recommended))
    return 0


if __name__ == "__main__":
    sys.exit(main())
