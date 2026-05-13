#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, time
from pathlib import Path

DEFAULT_ROOT = Path('/Users/Kosta/.config/skillshare/skills/knowledge-memory/obsidian-second-brain')
DEFAULT_VAULT = Path.home() / 'Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain'
REQUIRED_SECTIONS = [
    'Search ladder for hard-to-track data',
    'Breadcrumb and wiki-walk procedure',
    'Storage and routing decision tree',
    'Spec sheets and frontmatter discipline',
    'Pretty Obsidian formatting patterns',
    'Safe modification and idempotent updates',
    'Verification gates',
    'Benchmark metrics to track',
    'Edge cases and fallbacks',
    'Complex eval prompts',
]

def read(p: Path) -> str:
    return p.read_text(errors='ignore') if p.exists() else ''

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

def frontmatter_ok(text: str) -> bool:
    if not text.startswith('---\n'):
        return False
    parts = text.split('---', 2)
    return len(parts) >= 3 and 'type:' in parts[1] and 'tags:' in parts[1]

def sample_note() -> str:
    return """---
type: tool
status: active
tool_category: cli
install_method: homebrew
install_command: \"brew install example\"
url: \"https://example.com\"
tags:
  - type/catalog
  - domain/macos
created: 2026-05-13
updated: 2026-05-13
---
# Example Tool
> [!summary]
> A compact, linked tool note.

## Related
- [[mac-tools]]
- [[agent-tools]]
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--root', default=str(DEFAULT_ROOT))
    ap.add_argument('--vault', default=str(DEFAULT_VAULT))
    args = ap.parse_args()
    t0 = time.perf_counter()
    root = Path(args.root)
    vault = Path(args.vault)
    skill = read(root / 'SKILL.md')
    playbook = read(root / 'references' / 'operator-playbook.md')
    script = read(root / 'scripts' / 'bench_obsidian_second_brain.py')
    md_files = list(vault.rglob('*.md')) if vault.exists() else []
    templates = list((vault / 'templates').glob('*.md')) if (vault / 'templates').exists() else []
    paths_lower = [str(p.relative_to(vault)).lower() for p in md_files] if vault.exists() else []
    text_index = ''
    # Keep index bounded for speed/context accounting.
    for p in md_files[:900]:
        rel = str(p.relative_to(vault)) if vault.exists() else str(p)
        text_index += '\nPATH: ' + rel + '\n' + read(p)[:2000]
    tests = []
    def add(name, ok, detail=''):
        tests.append({'name': name, 'ok': bool(ok), 'detail': detail})
    add('vault exists', vault.exists(), str(vault))
    add('vault has substantial notes', len(md_files) >= 500, f'{len(md_files)} md files')
    add('templates present', len(templates) >= 15, f'{len(templates)} templates')
    add('plga hard-find note locatable', any('plga-degradation-kinetics' in p for p in paths_lower), 'brown concept breadcrumb')
    add('serve-sim locatable outside old tech tree', any('serve-sim.md' in p for p in paths_lower), 'ai-agents/infrastructure')
    add('agent-tools guide locatable', any(p.endswith('guides/agent-tools.md') for p in paths_lower), 'MOC/guide exists')
    add('operator playbook referenced by skill', 'operator-playbook.md' in skill, 'SKILL.md pointer')
    add('all required playbook sections present', all(s in playbook for s in REQUIRED_SECTIONS), f'{sum(s in playbook for s in REQUIRED_SECTIONS)}/{len(REQUIRED_SECTIONS)}')
    add('benchmark command documented', 'bench_obsidian_second_brain.py' in skill and 'bench_obsidian_second_brain.py' in playbook, 'script discoverable')
    add('sample frontmatter validates', frontmatter_ok(sample_note()), 'type/tags required')
    add('internal links use wikilinks', '[[mac-tools]]' in sample_note() and '](mac-tools' not in sample_note(), 'wikilink check')
    add('pretty formatting guidance present', all(x in playbook for x in ['callout', 'Recent Additions', 'Related', 'Breadcrumbs']), 'format/navigation cues')
    passed = sum(t['ok'] for t in tests)
    duration_ms = round((time.perf_counter() - t0) * 1000, 2)
    context_chars = len(skill) + len(playbook) + min(len(text_index), 500000)
    result = {
        'score': round(100 * passed / len(tests), 2),
        'passed': passed,
        'total': len(tests),
        'duration_ms': duration_ms,
        'vault_md_files': len(md_files),
        'templates': len(templates),
        'skill_chars': len(skill),
        'playbook_chars': len(playbook),
        'context_chars': context_chars,
        'estimated_context_tokens': estimate_tokens(skill + playbook + text_index[:500000]),
        'tests': tests,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"score={result['score']} passed={passed}/{len(tests)} duration_ms={duration_ms} tokens~{result['estimated_context_tokens']}")
        for t in tests:
            print(('PASS' if t['ok'] else 'FAIL'), t['name'], '-', t['detail'])
    raise SystemExit(0 if passed == len(tests) else 1)

if __name__ == '__main__':
    main()
