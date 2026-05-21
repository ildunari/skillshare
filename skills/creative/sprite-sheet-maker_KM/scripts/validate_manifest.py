#!/usr/bin/env python3
"""Validate a sprite-sheet-maker manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_mapping(data: object, name: str) -> dict[str, object]:
    if not isinstance(data, dict):
        fail(f"{name} must be an object")
    return data


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_manifest.py /path/to/manifest.json")

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"manifest not found: {path}")

    manifest = require_mapping(json.loads(path.read_text(encoding="utf-8")), "manifest")

    required = ["asset_name", "asset_slug", "asset_type", "camera", "style", "cell", "sheet", "animations", "files"]
    missing = [key for key in required if key not in manifest]
    if missing:
        fail(f"missing required keys: {', '.join(missing)}")

    cell = require_mapping(manifest["cell"], "cell")
    for key in ["width", "height"]:
        if not isinstance(cell.get(key), int) or int(cell[key]) <= 0:
            fail(f"cell.{key} must be a positive integer")

    sheet = require_mapping(manifest["sheet"], "sheet")
    for key in ["columns", "rows"]:
        if not isinstance(sheet.get(key), int) or int(sheet[key]) <= 0:
            fail(f"sheet.{key} must be a positive integer")

    animations = manifest["animations"]
    if not isinstance(animations, list) or not animations:
        fail("animations must be a non-empty array")

    ids: set[str] = set()
    max_frames = 0
    for index, animation_value in enumerate(animations):
        animation = require_mapping(animation_value, f"animations[{index}]")
        for key in ["id", "frames", "loop", "purpose"]:
            if key not in animation:
                fail(f"animations[{index}] missing {key}")
        row_id = animation["id"]
        if not isinstance(row_id, str) or not row_id:
            fail(f"animations[{index}].id must be a non-empty string")
        if row_id in ids:
            fail(f"duplicate animation id: {row_id}")
        ids.add(row_id)
        if not isinstance(animation["frames"], int) or int(animation["frames"]) <= 0:
            fail(f"animations[{index}].frames must be a positive integer")
        max_frames = max(max_frames, int(animation["frames"]))
        if not isinstance(animation["loop"], bool):
            fail(f"animations[{index}].loop must be boolean")

    if int(sheet["rows"]) != len(animations):
        fail(f"sheet.rows is {sheet['rows']} but animations has {len(animations)} rows")
    if int(sheet["columns"]) < max_frames:
        fail(f"sheet.columns is {sheet['columns']} but max frame count is {max_frames}")

    print("manifest-ok")


if __name__ == "__main__":
    main()

