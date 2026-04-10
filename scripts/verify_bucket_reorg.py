#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


BUCKETS = {
    'agentic',
    'ai-platforms-mcp',
    'apple',
    'automation',
    'code-quality',
    'documents-office',
    'github-release',
    'knowledge-memory',
    'media-creative',
    'meta-tools',
    'personal-ops',
    'research-analysis',
    'ui-ux',
}

ALLOWED_TOP_LEVEL = BUCKETS | {
    '_archived',
    'registry.yaml',
    '.gitignore',
    '.skillignore',
    '.skillignore.local',
    '.DS_Store',
}

STALE_PATTERNS = {
    r'\.\./xlsx/SKILL\.md': 'use ../officecli-xlsx/SKILL.md',
    r'\.\./docx/SKILL\.md': 'use ../officecli-docx/SKILL.md',
    r'\.\./docx/creating\.md': 'use ../officecli-docx/creating.md',
}


def fail(msg: str) -> None:
    print(f'FAIL: {msg}')


def main() -> int:
    repo_root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path.cwd()
    skills_dir = repo_root / 'skills'
    plan_path = repo_root / 'skill-reorg-plan.md'

    failures: list[str] = []

    if not skills_dir.is_dir():
        fail(f'missing skills dir: {skills_dir}')
        return 1

    top_names = sorted(p.name for p in skills_dir.iterdir())
    unexpected = [name for name in top_names if name not in ALLOWED_TOP_LEVEL]
    if unexpected:
        failures.append(f'unexpected top-level entries under skills/: {unexpected}')

    nested_git = sorted(str(p.relative_to(repo_root)) for p in skills_dir.rglob('.git'))
    if nested_git:
        failures.append(f'nested .git directories present: {nested_git}')

    for pattern, hint in STALE_PATTERNS.items():
        regex = re.compile(pattern)
        for md in skills_dir.rglob('*.md'):
            text = md.read_text(errors='ignore')
            if regex.search(text):
                failures.append(f'stale reference in {md.relative_to(repo_root)} matching {pattern!r} ({hint})')

    if plan_path.exists():
        plan_text = plan_path.read_text(errors='ignore')
        if 'Status: planned, not yet executed.' in plan_text:
            failures.append('skill-reorg-plan.md still says planned/not executed')

    if failures:
        for item in failures:
            fail(item)
        return 1

    print('OK: bucket reorg checks passed')
    print('Buckets:', ', '.join(sorted(BUCKETS)))
    print('Top-level entries:', ', '.join(top_names))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
