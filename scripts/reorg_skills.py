#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import yaml
import re

TEXT_EXTS = {'.md', '.yaml', '.yml', '.txt'}
CANDIDATE_RE = re.compile(r'(?P<path>(?:\.\./)+[^\s)\]}`"\'>]+)')


def load_moves(path: Path):
    data = yaml.safe_load(path.read_text()) or {}
    moves = data.get('moves') or []
    pairs = [(m['old'], m['new']) for m in moves]
    pairs.sort(key=lambda x: len(Path(x[0]).parts), reverse=True)
    return pairs


def build_top_level_map(pairs):
    top = {}
    for old, new in pairs:
        old_top = Path(old).parts[0]
        new_top = Path(new).parts[:2]
        if old_top in top and top[old_top] != new_top:
            raise ValueError(f'Conflicting bucket for {old_top}: {top[old_top]} vs {new_top}')
        top[old_top] = new_top
    return top


def remap_rel(rel: str, pairs):
    p = Path(rel)
    for old, new in pairs:
        oldp = Path(old)
        if p == oldp or oldp in p.parents:
            suffix = p.relative_to(oldp)
            return str(Path(new) / suffix) if str(suffix) != '.' else new
    return rel


def rewrite_candidate(old_file_rel: str, candidate: str, pairs, old_paths_set: set[str]):
    old_file = Path(old_file_rel)
    target_old = (old_file.parent / candidate).resolve().relative_to(Path('/tmp/skillshare-old-root'))
    target_old_str = str(target_old)
    if target_old_str not in old_paths_set:
        return candidate
    new_file_rel = remap_rel(old_file_rel, pairs)
    new_target_rel = remap_rel(target_old_str, pairs)
    new_rel = Path(new_target_rel).relative_to(Path(new_file_rel).parent) if Path(new_target_rel).is_absolute() else None
    # Relative_to only works for absolute; use os.path.relpath semantics manually
    import os
    return os.path.relpath(new_target_rel, start=str(Path(new_file_rel).parent))


def rewrite_text(old_file_rel: str, text: str, pairs, old_paths_set: set[str]):
    def repl(match):
        cand = match.group('path')
        try:
            # Resolve against a fake root built from old tree
            old_file_abs = Path('/tmp/skillshare-old-root') / old_file_rel
            target_abs = (old_file_abs.parent / cand).resolve()
            try:
                target_old = target_abs.relative_to(Path('/tmp/skillshare-old-root'))
            except ValueError:
                return cand
            target_old_str = str(target_old)
            if target_old_str not in old_paths_set:
                return cand
            import os
            new_file_rel = remap_rel(old_file_rel, pairs)
            new_target_rel = remap_rel(target_old_str, pairs)
            return os.path.relpath(new_target_rel, start=str(Path(new_file_rel).parent))
        except Exception:
            return cand
    return CANDIDATE_RE.sub(repl, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default='.')
    ap.add_argument('--map', dest='map_path', default='skill-reorg-map.yaml')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    skills_root = repo / 'skills'
    pairs = load_moves((repo / args.map_path).resolve())
    top_map = build_top_level_map(pairs)

    old_skill_dirs = {old for old, _ in pairs}
    old_paths_set = set()
    text_snapshots = {}

    for p in skills_root.rglob('*'):
        if '_archived' in p.parts:
            continue
        if p.is_file():
            rel = str(p.relative_to(skills_root))
            old_paths_set.add(rel)
            if p.suffix in TEXT_EXTS:
                text_snapshots[rel] = p.read_text()

    planned_top_moves = []
    for src_top, new_parts in sorted(top_map.items()):
        src = skills_root / src_top
        dest = skills_root.joinpath(*new_parts)
        if src.exists():
            planned_top_moves.append((src, dest))

    if not args.apply:
        print('Top-level moves:')
        for src, dest in planned_top_moves:
            print(f'{src.relative_to(skills_root)} -> {dest.relative_to(skills_root)}')
        return

    # Move top-level dirs into buckets
    for src, dest in planned_top_moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            raise RuntimeError(f'Destination exists: {dest}')
        shutil.move(str(src), str(dest))

    # Rewrite text files after move
    for old_rel, old_text in text_snapshots.items():
        new_rel = remap_rel(old_rel, pairs)
        new_path = skills_root / new_rel
        if not new_path.exists():
            continue
        new_text = rewrite_text(old_rel, old_text, pairs, old_paths_set)
        if new_text != old_text:
            new_path.write_text(new_text)

    print(f'Moved {len(planned_top_moves)} top-level directories and rewrote text references.')


if __name__ == '__main__':
    main()
