#!/usr/bin/env python3
"""
Obsidian Second Brain — benchmark-driven operator skill evaluator.

Tests SKILL.md completeness, playbook quality, template conformance,
YAML edge cases, routing decisions, and sandbox read/write/verify cycles.

Safe: all writes go only to workspace/sandbox/ — never the live vault.

Run:
  python bench_obsidian_second_brain.py --root <skill-dir> [--json] [--keep-sandbox]
"""
from __future__ import annotations
import argparse, json, re, shutil, time
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VAULT = Path.home() / 'Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain'

DIMENSIONS = [
    'correctness', 'retrieval_quality', 'breadcrumb_quality', 'storage_routing',
    'frontmatter_spec', 'markdown_visual', 'safety_idempotency', 'verification_strength',
    'token_efficiency', 'evalability',
]

REQUIRED_PLAYBOOK_SECTIONS = [
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

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(p: Path) -> str:
    return p.read_text(errors='ignore') if p.exists() else ''


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _yaml_simple_parse(text: str) -> dict | None:
    """Minimal frontmatter extractor — no external deps required."""
    if not text.startswith('---\n'):
        return None
    parts = text.split('---', 2)
    if len(parts) < 3:
        return None
    block = parts[1]
    result: dict = {}
    current_key = None
    current_list: list | None = None
    for line in block.splitlines():
        list_item = re.match(r'^  - (.+)$', line)
        kv = re.match(r'^(\w[\w_-]*):\s*(.*)', line)
        if list_item and current_list is not None:
            val = list_item.group(1).strip('"\'')
            current_list.append(val)
        elif kv:
            current_list = None
            key = kv.group(1)
            val = kv.group(2).strip().strip('"\'')
            if val == '':
                current_list = []
                result[key] = current_list
                current_key = key
            else:
                result[key] = val
                current_key = key
        else:
            current_list = None
    return result


def yaml_parse(text: str) -> dict | None:
    """Parse YAML frontmatter; PyYAML preferred, falls back to simple extractor."""
    try:
        import yaml  # type: ignore
        if not text.startswith('---\n'):
            return None
        parts = text.split('---', 2)
        if len(parts) < 3:
            return None
        return yaml.safe_load(parts[1]) or {}
    except Exception:
        return _yaml_simple_parse(text)


def frontmatter_valid(text: str, required: tuple[str, ...] = ('type', 'tags')) -> bool:
    fm = yaml_parse(text)
    return fm is not None and all(k in fm for k in required)


# ---------------------------------------------------------------------------
# Canonical sample notes (used in benchmark tests — not vault content)
# ---------------------------------------------------------------------------

def sample_tool_note() -> str:
    """Canonical pretty tool note demonstrating all required patterns."""
    return """\
---
type: tool
status: active
tool_category: cli
install_method: homebrew
install_command: "brew install example-tool"
url: "https://example.com/tool"
aliases:
  - example tool
  - et
tags:
  - type/catalog
  - domain/macos
created: 2026-05-13
updated: 2026-05-13
---
# Example Tool

> [!summary]
> Compact CLI for example tasks. Fastest option for this use case.

## Breadcrumbs
[[mac-tools]] > [[example-tool]]

## Why it matters
Speeds up repetitive terminal tasks by 3×.

## Usage
```bash
example-tool run --fast
example-tool --help
```

## Related
- [[mac-tools]]
- [[agent-tools]]
- [[hermes-agent]]

## Sources
- [GitHub](https://example.com/tool)
- [Docs](https://example.com/tool/docs)
"""


def sample_lit_note() -> str:
    """Canonical complete literature note."""
    return """\
---
type: literature
status: to_read
citekey: "jones2024-plga-kinetics"
title: "PLGA Degradation Kinetics Under Physiological Conditions"
authors:
  - "Jones, A."
  - "Smith, B."
year: 2024
venue: "Biomaterials"
doi: "10.1016/j.biomaterials.2024.01.001"
url: "https://doi.org/10.1016/j.biomaterials.2024.01.001"
projects:
  - fibrosis-delivery
tags:
  - type/reference
  - domain/research
created: 2026-05-13
updated: 2026-05-13
---
# PLGA Degradation Kinetics Under Physiological Conditions

> [!abstract]
> Examines PLGA polymer degradation rates in aqueous environments — directly
> relevant to controlled drug delivery timescales in fibrosis work.

## Key findings

## Methods

## Relevance to my work

## Questions / follow-ups

## Raw notes
"""


def sample_incomplete_lit_note() -> str:
    """Deliberately incomplete lit note — missing citekey and doi."""
    return """\
---
type: literature
status: to_read
title: "Some Paper Without Citation"
authors:
  - "Author, A."
year: 2024
tags:
  - type/reference
  - domain/research
created: 2026-05-13
updated: 2026-05-13
---
# Some Paper Without Citation
"""


def sample_colon_yaml_note() -> str:
    """Note with colon-containing values that require YAML quoting."""
    return """\
---
type: tool
status: active
title: "Fast: A Multi-Purpose CLI"
url: "https://example.com/fast"
install_command: "brew install fast"
tags:
  - type/catalog
  - domain/macos
created: 2026-05-13
updated: 2026-05-13
---
# Fast: A Multi-Purpose CLI
"""


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description='Obsidian Second Brain skill benchmark')
    ap.add_argument('--json', action='store_true', help='JSON output')
    ap.add_argument('--root', default=str(DEFAULT_ROOT), help='Skill root directory')
    ap.add_argument('--vault', default=str(DEFAULT_VAULT), help='Brain vault root (read-only)')
    ap.add_argument('--keep-sandbox', action='store_true', help='Preserve sandbox/ after run')
    args = ap.parse_args()

    t0 = time.perf_counter()
    root = Path(args.root)
    vault = Path(args.vault)
    sandbox = root / 'sandbox'

    skill = read(root / 'SKILL.md')
    playbook = read(root / 'references' / 'operator-playbook.md')
    templates_doc = read(root / 'references' / 'vault-templates.md')

    # Read-only vault stats
    md_files = list(vault.rglob('*.md')) if vault.exists() else []
    vault_templates = list((vault / 'templates').glob('*.md')) if (vault / 'templates').exists() else []
    paths_lower = [str(p.relative_to(vault)).lower() for p in md_files] if vault.exists() else []

    tests: list[dict] = []

    def add(name: str, ok: bool, detail: str = '', dim: str = 'correctness') -> None:
        tests.append({'name': name, 'ok': bool(ok), 'detail': detail, 'dim': dim})

    # =====================================================================
    # CORRECTNESS
    # =====================================================================
    add('skill_file_exists', (root / 'SKILL.md').exists(), str(root / 'SKILL.md'))
    add('playbook_file_exists', (root / 'references' / 'operator-playbook.md').exists())
    add('templates_ref_exists', (root / 'references' / 'vault-templates.md').exists())
    add('all_playbook_sections_present',
        all(s in playbook for s in REQUIRED_PLAYBOOK_SECTIONS),
        f'{sum(s in playbook for s in REQUIRED_PLAYBOOK_SECTIONS)}/{len(REQUIRED_PLAYBOOK_SECTIONS)} sections')
    add('sample_tool_frontmatter_valid',
        frontmatter_valid(sample_tool_note()),
        'type+tags required')
    add('sample_lit_frontmatter_full',
        frontmatter_valid(sample_lit_note(), ('type', 'status', 'citekey', 'doi', 'tags')),
        'complete lit note fields')
    add('incomplete_lit_note_fails_strict_check',
        not frontmatter_valid(sample_incomplete_lit_note(), ('type', 'status', 'citekey', 'doi', 'tags')),
        'validation correctly rejects missing citekey/doi')

    # =====================================================================
    # RETRIEVAL QUALITY
    # Hard retrieval: skill must cover ALL 7 active top-level folders
    # =====================================================================
    hard_folders = ['ai-agents/', 'tech/', 'coding/', 'brown/', 'daily/', 'inbox/', 'wiki/']
    for folder in hard_folders:
        add(f'skill_covers_{folder.rstrip("/")}',
            folder in skill,
            f'folder {folder} referenced in skill', 'retrieval_quality')
    add('playbook_alias_synonym_pass',
        'Alias/synonym pass' in playbook or ('alias' in playbook.lower() and 'search' in playbook.lower()),
        'alias/synonym as explicit search step', 'retrieval_quality')
    add('skill_alias_search_mentioned',
        any(w in skill.lower() for w in ['alias', 'citekey', 'synonym']),
        'alias/citekey/synonym in skill', 'retrieval_quality')
    add('playbook_recent_capture_pass',
        'Recent-capture pass' in playbook or ('inbox' in playbook.lower() and 'recent' in playbook.lower()),
        'recent capture pass in search ladder', 'retrieval_quality')
    add('playbook_search_covers_property_pass',
        'Property pass' in playbook or 'frontmatter' in playbook.lower(),
        'property/frontmatter pass in ladder', 'retrieval_quality')

    # =====================================================================
    # BREADCRUMB QUALITY
    # =====================================================================
    add('playbook_3hop_chain_example',
        bool(re.search(r'\[\[.+?\]\].*?→.*?\[\[.+?\]\].*?→.*?\[\[.+?\]\]', playbook)),
        'concrete [[A]] → [[B]] → [[C]] example in playbook', 'breadcrumb_quality')
    add('playbook_hop_terminology',
        'hop' in playbook.lower() or '3-hop' in playbook or 'multi-hop' in playbook.lower(),
        'hop/3-hop terminology in wiki-walk section', 'breadcrumb_quality')
    add('sample_note_has_breadcrumb_section',
        '## Breadcrumbs' in sample_tool_note() and '>' in sample_tool_note(),
        '## Breadcrumbs section in canonical tool note', 'breadcrumb_quality')
    add('playbook_backlink_guidance',
        'backlink' in playbook.lower(),
        'backlink inspection described', 'breadcrumb_quality')
    add('playbook_moc_navigation',
        'MOC' in playbook or ('guide' in playbook.lower() and 'top-level' in playbook.lower()),
        'MOC/top-level guide navigation described', 'breadcrumb_quality')

    # =====================================================================
    # STORAGE / ROUTING
    # =====================================================================
    add('skill_routing_section_explicit',
        'Determine section first' in skill or 'route' in skill.lower(),
        'explicit routing decision in skill', 'storage_routing')
    add('skill_routing_ai_agents_vs_tech',
        'ai-agents/' in skill and 'tech/' in skill,
        'ai-agents/ and tech/ both named as destinations', 'storage_routing')
    add('playbook_routing_ai_agents_preferred',
        'ai-agents/' in playbook and ('prefer' in playbook.lower() or 'live' in playbook.lower()),
        'playbook says prefer ai-agents/ for live infra', 'storage_routing')
    add('skill_routing_coding_section',
        'coding/' in skill,
        'coding/ section present as routing destination', 'storage_routing')
    add('skill_routing_inbox_fallback',
        'inbox/quick' in skill,
        'inbox/quick/ as ambiguous-routing fallback', 'storage_routing')
    add('playbook_routing_neighborhood_principle',
        'neighborhood' in playbook.lower() or 'nearby' in playbook.lower(),
        'stay in note neighborhood principle', 'storage_routing')

    # =====================================================================
    # FRONTMATTER / SPEC COMPLIANCE
    # =====================================================================
    add('yaml_colon_title_quoted',
        bool(re.search(r"title:\s*['\"].*:.*['\"]", skill)) or
        bool(re.search(r"title:\s*['\"].*:.*['\"]", playbook)),
        "title with colon must be quoted in YAML examples", 'frontmatter_spec')
    add('yaml_url_quoted',
        bool(re.search(r'url:\s*"https://', skill)) or bool(re.search(r"url:\s*'https://", skill)) or
        bool(re.search(r'url:\s*"https://', playbook)) or bool(re.search(r"url:\s*'https://", playbook)),
        'URL values quoted in frontmatter examples', 'frontmatter_spec')
    add('yaml_aliases_in_templates',
        'aliases:' in templates_doc,
        'aliases: field in vault-templates.md', 'frontmatter_spec')
    add('yaml_aliases_in_skill',
        'aliases:' in skill,
        'aliases: field in SKILL.md frontmatter example', 'frontmatter_spec')
    add('yaml_list_array_syntax',
        bool(re.search(r'^  - ["\']', templates_doc, re.MULTILINE)),
        'YAML list arrays use "  - item" style', 'frontmatter_spec')
    add('templates_cover_core_types',
        all(t in templates_doc for t in ['type: tool', 'type: literature', 'type: meeting',
                                          'mcp-server', 'skill-ref']),
        'all core note types in templates doc', 'frontmatter_spec')
    add('yaml_colon_note_parses',
        yaml_parse(sample_colon_yaml_note()) is not None and
        (yaml_parse(sample_colon_yaml_note()) or {}).get('title') == 'Fast: A Multi-Purpose CLI',
        'YAML round-trip: colon in quoted title parses correctly', 'frontmatter_spec')

    # =====================================================================
    # MARKDOWN / VISUAL QUALITY
    # =====================================================================
    add('sample_tool_summary_callout',
        '> [!summary]' in sample_tool_note(),
        'summary callout in tool note', 'markdown_visual')
    add('sample_lit_abstract_callout',
        '> [!abstract]' in sample_lit_note(),
        'abstract callout in lit note', 'markdown_visual')
    add('sample_tool_related_section',
        '## Related' in sample_tool_note(),
        '## Related section with wikilinks', 'markdown_visual')
    add('sample_tool_wikilinks_not_md',
        '[[mac-tools]]' in sample_tool_note() and '](mac-tools' not in sample_tool_note(),
        'internal links are [[wikilinks]] not markdown', 'markdown_visual')
    add('playbook_callout_usage_guide',
        'callout' in playbook.lower() and ('[!tip]' in playbook or '[!warning]' in playbook or
                                            '[!example]' in playbook or 'callout' in playbook),
        'callout type guidance in playbook', 'markdown_visual')

    # =====================================================================
    # SAFETY / IDEMPOTENCY
    # =====================================================================
    add('playbook_idempotent_guide_append',
        'idempotent' in playbook.lower() or
        ('search' in playbook.lower() and 'duplicate' in playbook.lower()),
        'idempotent append: search before adding guide link', 'safety_idempotency')
    add('skill_no_clobber_existing',
        'overwrite' in skill.lower() or 'clobber' in skill.lower() or 'existing note' in skill.lower(),
        'no-clobber: read before overwrite', 'safety_idempotency')
    add('playbook_preserve_dataview',
        'Dataview' in playbook,
        'preserve Dataview blocks on edit', 'safety_idempotency')
    add('skill_pause_before_destructive',
        ('delete' in skill.lower() or 'archive' in skill.lower()) and
        ('pause' in skill.lower() or 'confirm' in skill.lower()),
        'pause/confirm before delete or archive', 'safety_idempotency')
    add('sandbox_idempotent_link_count',
        False,  # placeholder — resolved in sandbox block below
        'sandbox: idempotent append yields exactly 1 link', 'safety_idempotency')

    # =====================================================================
    # VERIFICATION STRENGTH
    # =====================================================================
    add('playbook_verification_gates',
        all(v in playbook.lower() for v in ['frontmatter', 'wikilink', 'guide append']),
        'gates cover frontmatter + wikilink + guide append', 'verification_strength')
    add('skill_verify_after_write',
        'verify' in skill.lower() and ('read path' in skill.lower() or 'obsidian vault' in skill.lower()),
        'explicit verify step after write', 'verification_strength')
    add('playbook_cli_unavailable_fallback',
        ('unavailable' in playbook.lower() or 'not running' in playbook.lower()) and
        'filesystem' in playbook.lower(),
        'CLI unavailable → filesystem fallback in playbook', 'verification_strength')
    add('skill_explicit_cli_fallback',
        'not running' in skill.lower() or 'unavailable' in skill.lower() or
        'fallback' in skill.lower() or 'MCP proxy' in skill,
        'skill has explicit CLI-unavailable fallback path', 'verification_strength')
    add('sandbox_yaml_roundtrip',
        False,  # placeholder — resolved in sandbox block below
        'sandbox: YAML with colon title round-trips correctly', 'verification_strength')

    # =====================================================================
    # TOKEN EFFICIENCY
    # =====================================================================
    add('skill_within_char_budget',
        len(skill) <= 22000,
        f'{len(skill)} chars (budget 22000)', 'token_efficiency')
    add('playbook_within_char_budget',
        len(playbook) <= 12000,
        f'{len(playbook)} chars (budget 12000)', 'token_efficiency')
    add('benchmark_command_in_both',
        'bench_obsidian_second_brain.py' in skill and 'bench_obsidian_second_brain.py' in playbook,
        'benchmark command discoverable from skill + playbook', 'token_efficiency')

    # =====================================================================
    # EVALABILITY
    # =====================================================================
    add('playbook_hard_eval_prompts_section',
        'Complex eval prompts' in playbook,
        'Complex eval prompts section present', 'evalability')
    add('eval_covers_cli_unavailable',
        'CLI unavailable' in playbook or 'cli unavailable' in playbook.lower() or
        'Obsidian CLI unavailable' in playbook,
        'eval prompt covers CLI-unavailable scenario', 'evalability')
    add('eval_covers_wiki_hop',
        'hop' in playbook.lower() or '3-hop' in playbook or 'wiki-walk' in playbook.lower(),
        'eval prompt covers 3-hop wiki-walk', 'evalability')
    add('eval_covers_duplicate_prevention',
        'duplicate' in playbook.lower(),
        'eval covers duplicate guide-link prevention', 'evalability')
    add('eval_covers_yaml_edge',
        'YAML' in playbook and any(w in playbook.lower() for w in ['colon', 'alias', 'url']),
        'eval covers YAML edge cases', 'evalability')
    add('eval_covers_routing_disambiguation',
        'ai-agents' in playbook and 'tech/agent-tools' in playbook,
        'eval covers ai-agents/ vs tech/agent-tools/ routing', 'evalability')
    add('sandbox_full_write_read_verify',
        False,  # placeholder — resolved in sandbox block below
        'sandbox: full write/read/verify cycle', 'evalability')

    # =====================================================================
    # VAULT-DEPENDENT (skip gracefully if vault not present)
    # =====================================================================
    if vault.exists():
        add('vault_has_substantial_notes',
            len(md_files) >= 500, f'{len(md_files)} notes', 'correctness')
        add('vault_templates_present',
            len(vault_templates) >= 15, f'{len(vault_templates)} templates', 'correctness')
        add('plga_hard_find_locatable',
            any('plga' in p for p in paths_lower),
            'brown/concepts or literature breadcrumb', 'retrieval_quality')
        add('serve_sim_in_ai_agents',
            any('serve-sim' in p for p in paths_lower),
            'ai-agents/ routing (not old tech/agent-tools)', 'storage_routing')
        add('agent_tools_guide_exists',
            any(p.endswith('guides/agent-tools.md') for p in paths_lower),
            'MOC guide page exists', 'storage_routing')

    # =====================================================================
    # SANDBOX LIVE TESTS (write only to sandbox/ — never live vault)
    # =====================================================================
    sandbox_idempotent_ok = False
    sandbox_idempotent_detail = 'not run'
    sandbox_yaml_ok = False
    sandbox_yaml_detail = 'not run'
    sandbox_full_ok = False
    sandbox_full_detail = 'not run'
    try:
        sandbox.mkdir(parents=True, exist_ok=True)

        # ---- Full write/read/verify ----
        note_path = sandbox / 'test-tool-note.md'
        note_path.write_text(sample_tool_note())
        content = note_path.read_text()
        fm = yaml_parse(content)
        assert fm is not None, 'YAML parse failed'
        assert fm.get('type') == 'tool', f"type={fm.get('type')}"
        assert '[[mac-tools]]' in content, 'wikilink missing'
        assert '> [!summary]' in content, 'callout missing'
        assert '## Related' in content, '## Related missing'
        sandbox_full_ok = True
        sandbox_full_detail = 'write+read+yaml+wikilink+callout all verified'

        # ---- Idempotent guide-link append ----
        guide_path = sandbox / 'test-guide.md'
        guide_path.write_text('# Test Guide\n\n## Recent Additions\n')
        link = '- [[test-tool-note]] — Example tool'
        for _ in range(2):  # append twice on purpose
            current = guide_path.read_text()
            if link not in current:
                guide_path.write_text(current + link + '\n')
        count = guide_path.read_text().count(link)
        assert count == 1, f'link appears {count} times (expected 1)'
        sandbox_idempotent_ok = True
        sandbox_idempotent_detail = f'link count = {count} after 2 attempted appends'

        # ---- YAML colon round-trip ----
        colon_path = sandbox / 'test-colon-yaml.md'
        colon_path.write_text(sample_colon_yaml_note())
        fm2 = yaml_parse(colon_path.read_text())
        assert fm2 is not None, 'YAML with colon failed to parse'
        assert fm2.get('title') == 'Fast: A Multi-Purpose CLI', \
            f'title mismatch: {fm2.get("title")!r}'
        sandbox_yaml_ok = True
        sandbox_yaml_detail = 'colon-title YAML round-trip OK'

    except Exception as e:
        detail = f'FAILED: {e}'
        if not sandbox_full_ok:
            sandbox_full_detail = detail
        elif not sandbox_idempotent_ok:
            sandbox_idempotent_detail = detail
        elif not sandbox_yaml_ok:
            sandbox_yaml_detail = detail

    finally:
        if not args.keep_sandbox and sandbox.exists():
            shutil.rmtree(sandbox)

    # Patch the placeholder tests
    for t in tests:
        if t['name'] == 'sandbox_idempotent_link_count':
            t['ok'] = sandbox_idempotent_ok
            t['detail'] = sandbox_idempotent_detail
        elif t['name'] == 'sandbox_yaml_roundtrip':
            t['ok'] = sandbox_yaml_ok
            t['detail'] = sandbox_yaml_detail
        elif t['name'] == 'sandbox_full_write_read_verify':
            t['ok'] = sandbox_full_ok
            t['detail'] = sandbox_full_detail

    # =====================================================================
    # Scoring
    # =====================================================================
    passed = sum(t['ok'] for t in tests)
    total = len(tests)
    score = round(100 * passed / total, 2)

    dim_scores: dict[str, float | None] = {}
    for dim in DIMENSIONS:
        dim_tests = [t for t in tests if t['dim'] == dim]
        dim_scores[dim] = (
            round(100 * sum(t['ok'] for t in dim_tests) / len(dim_tests), 1)
            if dim_tests else None
        )

    duration_ms = round((time.perf_counter() - t0) * 1000, 2)
    result = {
        'score': score,
        'passed': passed,
        'total': total,
        'duration_ms': duration_ms,
        'dimension_scores': dim_scores,
        'vault_md_files': len(md_files),
        'skill_chars': len(skill),
        'playbook_chars': len(playbook),
        'estimated_context_tokens': estimate_tokens(skill + playbook),
        'tests': tests,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'score={score}  passed={passed}/{total}  duration_ms={duration_ms}')
        print()
        for dim in DIMENSIONS:
            dim_tests = [t for t in tests if t['dim'] == dim]
            if dim_tests:
                d_pass = sum(t['ok'] for t in dim_tests)
                bar = '█' * d_pass + '░' * (len(dim_tests) - d_pass)
                print(f'  {dim:26s} {bar}  {d_pass}/{len(dim_tests)}')
        print()
        for t in tests:
            status = 'PASS' if t['ok'] else 'FAIL'
            print(f'  {status}  [{t["dim"][:12]:12s}]  {t["name"]}  —  {t["detail"]}')

    raise SystemExit(0 if passed == total else 1)


if __name__ == '__main__':
    main()
