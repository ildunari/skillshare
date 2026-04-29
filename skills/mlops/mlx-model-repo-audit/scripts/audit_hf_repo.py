#!/usr/bin/env python3
"""Audit Hugging Face-style model repositories for MLX planning.

The script intentionally avoids making compatibility claims. It gathers repo
metadata and file lists so an agent can decide which MLX skill to use next.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

IMPORTANT_FILENAMES = {
    "config.json",
    "generation_config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    "chat_template.json",
    "preprocessor_config.json",
    "processor_config.json",
    "image_processor_config.json",
    "video_processor_config.json",
    "feature_extractor_config.json",
    "adapter_config.json",
}
IMPORTANT_SUFFIXES = (
    ".safetensors",
    ".safetensors.index.json",
    ".bin",
    ".model",
    ".tiktoken",
    ".json",
    ".txt",
)


def read_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def summarize_files(files: Iterable[str]) -> Dict[str, Any]:
    files = sorted(files)
    return {
        "count": len(files),
        "important_files": [f for f in files if Path(f).name in IMPORTANT_FILENAMES],
        "weight_files": [f for f in files if f.endswith((".safetensors", ".bin"))],
        "index_files": [f for f in files if f.endswith(".index.json")],
        "json_files": [f for f in files if f.endswith(".json")],
        "all_files": files,
    }


def audit_local(path: Path) -> Dict[str, Any]:
    files = [str(p.relative_to(path)) for p in path.rglob("*") if p.is_file()]
    result: Dict[str, Any] = {
        "source": "local",
        "path": str(path),
        "files": summarize_files(files),
        "configs": {},
    }
    for name in IMPORTANT_FILENAMES:
        config_path = path / name
        if config_path.exists() and config_path.suffix == ".json":
            result["configs"][name] = read_json(config_path)
    return result


def audit_hub(model_id: str) -> Dict[str, Any]:
    try:
        from huggingface_hub import HfApi, model_info
    except ImportError as exc:
        raise SystemExit(
            "Install huggingface_hub first: python -m pip install huggingface_hub"
        ) from exc

    api = HfApi()
    info = model_info(model_id, files_metadata=True)
    siblings = [s.rfilename for s in info.siblings or []]
    result: Dict[str, Any] = {
        "source": "huggingface_hub",
        "model_id": model_id,
        "sha": getattr(info, "sha", None),
        "pipeline_tag": getattr(info, "pipeline_tag", None),
        "library_name": getattr(info, "library_name", None),
        "tags": sorted(getattr(info, "tags", []) or []),
        "license": getattr(info, "card_data", None).get("license") if isinstance(getattr(info, "card_data", None), dict) else None,
        "files": summarize_files(siblings),
    }
    return result


def load_audit(target: str) -> Dict[str, Any]:
    path = Path(target).expanduser()
    if path.exists():
        return audit_local(path)
    return audit_hub(target)


def compare_configs(target: Dict[str, Any], base: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not base:
        return {}
    comparison: Dict[str, Any] = {"shared_important_files": [], "target_only_files": [], "base_only_files": []}
    target_files = {Path(f).name for f in target.get("files", {}).get("all_files", [])}
    base_files = {Path(f).name for f in base.get("files", {}).get("all_files", [])}
    important = set(IMPORTANT_FILENAMES)
    comparison["shared_important_files"] = sorted((target_files & base_files) & important)
    comparison["target_only_files"] = sorted((target_files - base_files) & important)
    comparison["base_only_files"] = sorted((base_files - target_files) & important)
    return comparison


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit model repo files for MLX planning.")
    parser.add_argument("target", help="Hugging Face model ID or local model directory")
    parser.add_argument("--base", help="Optional base model ID or local directory")
    parser.add_argument("--output", help="Write JSON audit to this path")
    args = parser.parse_args()

    target = load_audit(args.target)
    base = load_audit(args.base) if args.base else None
    report = {"target": target, "base": base, "comparison": compare_configs(target, base)}
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
