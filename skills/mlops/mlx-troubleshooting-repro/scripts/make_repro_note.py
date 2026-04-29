#!/usr/bin/env python3
"""Create a Markdown minimal repro note for MLX issues."""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path


def safe_cmd(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"unavailable: {exc}"


def package_versions() -> str:
    packages = ["mlx", "mlx_lm", "mlx_vlm", "mlx_embeddings", "transformers", "huggingface_hub"]
    lines = []
    for package in packages:
        try:
            mod = __import__(package)
            version = getattr(mod, "__version__", "unknown")
            lines.append(f"- {package}: {version}")
        except Exception as exc:
            lines.append(f"- {package}: not importable ({exc})")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an MLX issue repro Markdown note.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--error-log", help="Path to full error log")
    parser.add_argument("--output", default="mlx_issue_repro.md")
    parser.add_argument("--expected", default="Model should convert, load, or generate successfully.")
    args = parser.parse_args()

    error_text = ""
    if args.error_log:
        error_path = Path(args.error_log)
        error_text = error_path.read_text(encoding="utf-8", errors="replace") if error_path.exists() else f"Error log not found: {error_path}"

    note = f"""# MLX issue repro: {args.title}

## Summary
Failure with `{args.model}`. Replace this sentence with the precise failure phase: conversion, load, preprocessing, generation, quantization, server, or upload.

## Environment
- Platform: {platform.platform()}
- Python: {sys.version.split()[0]}
- CPU: {safe_cmd(['sysctl', '-n', 'machdep.cpu.brand_string'])}

### Package versions
{package_versions()}

## Model
- Model ID/path/revision: `{args.model}`

## Command or code
```bash
{args.command}
```

## Expected behavior
{args.expected}

## Actual behavior
```text
{error_text if error_text else 'Paste full error log or invalid output here.'}
```

## What I already tried
- [ ] Updated MLX-related packages
- [ ] Tested unquantized or less aggressive quantization
- [ ] Tested a tiny prompt or media input
- [ ] Compared with Transformers baseline
- [ ] Checked related upstream issues and releases

## Minimal input files
List any image/audio/video/prompt files needed to reproduce.
"""
    Path(args.output).write_text(note, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
