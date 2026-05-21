#!/usr/bin/env python3
"""Create a sprite-sheet-maker run folder with manifest, brief, and prompts."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULTS = {
    "character": "idle:6:loop,run:8:loop,jump:6,attack-light:6,hurt:4,defeat:8",
    "prop": "idle:6:loop,activate:6,active:4:loop",
    "torch": "idle-flame:6:loop,flare:6,dim:5,extinguish:6,relight:6",
    "effect": "spawn:5,active-loop:6:loop,impact:6,dissipate:6",
    "pickup": "idle:6:loop,spark:6:loop,collect:6,respawn:6",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-") or "sprite-asset"


def parse_cell(raw: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)x(\d+)\s*", raw.lower())
    if not match:
        raise SystemExit(f"--cell must look like 128x128, got {raw!r}")
    return int(match.group(1)), int(match.group(2))


def parse_animations(raw: str) -> list[dict[str, object]]:
    animations: list[dict[str, object]] = []
    for item in [part.strip() for part in raw.split(",") if part.strip()]:
        parts = item.split(":")
        if len(parts) < 2:
            raise SystemExit(f"Animation must look like id:frames[:loop], got {item!r}")
        row_id = slugify(parts[0])
        try:
            frames = int(parts[1])
        except ValueError as exc:
            raise SystemExit(f"Frame count must be an integer in {item!r}") from exc
        loop = any(part.lower() in {"loop", "true", "yes"} for part in parts[2:])
        animations.append(
            {
                "id": row_id,
                "frames": frames,
                "loop": loop,
                "purpose": infer_purpose(row_id, loop),
                "frame_duration_ms": 120,
            }
        )
    return animations


def infer_purpose(row_id: str, loop: bool) -> str:
    purposes = {
        "idle": "neutral readable loop",
        "run": "locomotion loop",
        "walk": "slower locomotion loop",
        "jump": "anticipation, lift, peak, descent, land",
        "hurt": "readable hit reaction",
        "defeat": "non-looping defeat animation",
        "death": "non-looping defeat animation",
        "idle-flame": "steady flame loop",
        "flare": "brief brighter flame burst",
        "dim": "flame lowers toward weak state",
        "extinguish": "flame goes out",
        "relight": "flame returns from dark state",
    }
    return purposes.get(row_id, "looping action" if loop else "non-looping action")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def base_prompt(args: argparse.Namespace, manifest: dict[str, object]) -> str:
    locks = manifest.get("identity_lock") or ["<add stable identity lock before generation>"]
    lock_text = "; ".join(str(item) for item in locks)
    return f"""Asset: {args.asset_name}
Use: canonical game sprite reference for a later sprite sheet
Camera: {args.camera}
Style: {args.style}
Subject: {args.description}
Silhouette: readable, game-scale silhouette with one clear signature shape
Palette/materials: limited palette appropriate to the style
Gameplay feel: {args.gameplay_feel}
Output: one clean complete sprite pose, centered, full body/object visible, generous padding
Background: flat {manifest["sheet"]["chroma_key"]} chroma-key background, one uniform color, no shadows or gradients
Preserve for all future rows: {lock_text}
Avoid: text, UI, watermark, scene background, cropped parts, tiny unreadable detail
"""


def row_prompt(args: argparse.Namespace, manifest: dict[str, object], animation: dict[str, object]) -> str:
    locks = manifest.get("identity_lock") or ["<add stable identity lock before generation>"]
    lock_text = "; ".join(str(item) for item in locks)
    loop_text = "loop" if animation["loop"] else "non-loop"
    return f"""Asset: {args.asset_name}
Animation row: {animation["id"]}, {animation["frames"]} frames, {loop_text}
Use: sprite-sheet row for {args.camera} {args.style}
Input images:
- Image 1: canonical base identity reference
Preserve exactly: {lock_text}
Action beats: {animation["purpose"]}
Layout: one horizontal strip, equal spacing, one complete pose per slot, centered inside each slot, no overlap
Background: perfectly flat {manifest["sheet"]["chroma_key"]}; do not use that color in the sprite
Avoid: text, labels, frame numbers, visible guides, scenery, detached shadows, motion blur, cropped limbs, duplicate frames, new props unless requested
"""


def brief(args: argparse.Namespace, manifest: dict[str, object]) -> str:
    rows = "\n".join(
        f"| {a['id']} | {a['frames']} | {'yes' if a['loop'] else 'no'} | {a['purpose']} |"
        for a in manifest["animations"]
    )
    return f"""# {args.asset_name}

## Goal

{args.description}

## Player Read

The player should recognize the asset's role and state from silhouette and motion at game scale.

## Camera And Scale

- Camera: {args.camera}
- Cell: {manifest['cell']['width']}x{manifest['cell']['height']}
- Asset type: {args.asset_type}

## Art Direction

{args.style}

## Identity Locks

- <add stable shape, marking, palette, prop, or material details before generation>

## Animation Plan

| Row | Frames | Loop | Purpose |
| --- | ---: | --- | --- |
{rows}

## Technical Notes

- Background: {manifest['sheet']['background']} ({manifest['sheet']['chroma_key']})
- Final format: PNG/WebP plus JSON manifest
- Created: {manifest['created_at']}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset-name", required=True)
    parser.add_argument("--asset-type", default="character")
    parser.add_argument("--camera", default="side-view")
    parser.add_argument("--style", default="chunky pixel-art-adjacent game sprite")
    parser.add_argument("--description", default="A game-ready animated sprite asset.")
    parser.add_argument("--gameplay-feel", default="clear, readable, responsive")
    parser.add_argument("--animations", default="")
    parser.add_argument("--cell", default="128x128")
    parser.add_argument("--columns", type=int, default=8)
    parser.add_argument("--background", default="chroma-key")
    parser.add_argument("--chroma-key", default="#00ff00")
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()

    slug = slugify(args.asset_name)
    cell_w, cell_h = parse_cell(args.cell)
    raw_animations = args.animations or DEFAULTS.get(args.asset_type, DEFAULTS["character"])
    animations = parse_animations(raw_animations)
    rows = len(animations)
    columns = max(args.columns, max(int(animation["frames"]) for animation in animations))
    output_dir = (
        Path(args.output_dir)
        if args.output_dir
        else Path.cwd() / "sprite-runs" / f"{slug}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    for rel in [
        "prompts/rows",
        "references/user",
        "references/style",
        "references/layout-guides",
        "generated/base",
        "generated/rows",
        "final/frames",
        "qa",
    ]:
        (output_dir / rel).mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "asset_name": args.asset_name,
        "asset_slug": slug,
        "asset_type": args.asset_type,
        "camera": args.camera,
        "style": args.style,
        "description": args.description,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "cell": {"width": cell_w, "height": cell_h},
        "sheet": {
            "columns": columns,
            "rows": rows,
            "background": args.background,
            "chroma_key": args.chroma_key,
        },
        "palette": [],
        "identity_lock": [],
        "animations": animations,
        "files": {
            "brief": "brief.md",
            "base_prompt": "prompts/00-base.md",
            "spritesheet": "final/spritesheet.png",
            "contact_sheet": "qa/contact-sheet.png",
        },
    }

    write(output_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    write(output_dir / "brief.md", brief(args, manifest))
    write(output_dir / "prompts/00-base.md", base_prompt(args, manifest))
    for animation in animations:
        write(output_dir / f"prompts/rows/{animation['id']}.md", row_prompt(args, manifest, animation))

    print(output_dir)


if __name__ == "__main__":
    main()
