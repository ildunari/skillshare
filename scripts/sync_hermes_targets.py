#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml


def load_yaml(path: Path):
    if not path.exists():
        raise FileNotFoundError(path)
    return yaml.safe_load(path.read_text()) or {}


def dump_yaml(path: Path, data: dict) -> None:
    header = "# yaml-language-server: $schema=https://raw.githubusercontent.com/runkids/skillshare/main/schemas/config.schema.json\n"
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    path.write_text(header + body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Hermes skillshare targets from a tracked allowlist")
    parser.add_argument("--config", default="config.yaml", help="Path to local skillshare config.yaml")
    parser.add_argument("--allowlist", default="hermes-allowlist.yaml", help="Path to tracked Hermes allowlist YAML")
    parser.add_argument("--mode", choices=["studio", "isolate"], required=True)
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    allowlist_path = Path(args.allowlist).expanduser().resolve()

    config = load_yaml(config_path)
    allowlist = load_yaml(allowlist_path)
    skills = allowlist.get("skills") or []
    if not isinstance(skills, list) or not all(isinstance(x, str) and x for x in skills):
        raise ValueError(f"Invalid skills list in {allowlist_path}")

    targets = config.setdefault("targets", {})

    # Clear all Hermes target variants first so mode switches are clean.
    for key in ("hermes", "hermes-default", "hermes-gpt"):
        targets.pop(key, None)

    if args.mode == "studio":
        home = Path.home()
        shared_include = list(skills)
        targets["hermes-default"] = {
            "skills": {
                "path": str(home / ".hermes" / "skills"),
                "include": shared_include,
            }
        }
        targets["hermes-gpt"] = {
            "skills": {
                "path": str(home / ".hermes" / "profiles" / "gpt" / "skills"),
                "include": list(skills),
            }
        }

    dump_yaml(config_path, config)
    print(f"Updated {config_path} in {args.mode} mode with {len(skills)} Hermes skill(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
