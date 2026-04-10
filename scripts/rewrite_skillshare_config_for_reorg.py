#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def load_moves(path: Path):
    data = yaml.safe_load(path.read_text()) or {}
    pairs = [(m['old'], m['new']) for m in (data.get('moves') or [])]
    pairs.sort(key=lambda x: len(Path(x[0]).parts), reverse=True)
    return pairs


def remap_value(value: str, pairs):
    p = Path(value)
    for old, new in pairs:
        oldp = Path(old)
        if p == oldp:
            return new.replace('/', '__')
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.yaml')
    ap.add_argument('--map', dest='map_path', default='skill-reorg-map.yaml')
    args = ap.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    map_path = Path(args.map_path).expanduser().resolve()
    config = yaml.safe_load(config_path.read_text()) or {}
    pairs = load_moves(map_path)

    for name, target in (config.get('targets') or {}).items():
        skills = (target or {}).get('skills') or {}
        for key in ('include', 'exclude'):
            vals = skills.get(key)
            if isinstance(vals, list):
                skills[key] = [remap_value(v, pairs) for v in vals]

    header = '# yaml-language-server: $schema=https://raw.githubusercontent.com/runkids/skillshare/main/schemas/config.schema.json\n'
    config_path.write_text(header + yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
    print(f'Updated {config_path}')


if __name__ == '__main__':
    main()
