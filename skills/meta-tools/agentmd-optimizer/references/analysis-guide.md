# Analysis Guide

Reference for Phases 0–5 of the upgraded Instruction & Skill Optimizer.

## First rule: separate the questions

The optimizer must keep these distinct:
- **Disk footprint** — files present anywhere on the machine
- **Possible runtime load** — files a runtime could inspect
- **Likely session stack** — files plausibly loaded together in one session
- **On-demand loading** — skills, references, and bundled resources loaded only when triggered

A machine-wide token total is useful, but it is not the same as a real session burden.

## Recommended budgets

These are directional ceilings, not hard limits.

| Layer | Guideline |
|---|---|
| Global file | ~800 tokens |
| Project/root file | ~400 tokens |
| Subdirectory file | ~200 tokens |
| Combined likely stack | ~1400–2000 tokens before user input |
| Directive count in one stack | ideally <150 |

## What to prioritize

### Highest-value findings
1. files in active plausible load stacks
2. exact duplicates across runtime installs
3. near duplicates with merge potential
4. contradictory directives in the same stack
5. high-confidence delete candidates in archive/vendor/mirror/cache paths

### Lower-value findings
- giant disk-only clusters that do not materially affect active sessions
- wording polish without load or drift impact
- semantic overlap with low confidence and no action path

## Bloat signals
- token budget far above guidance
- long manuals embedded in instruction files
- huge section count / giant table of contents
- setup notes and migration guides mixed into standing instructions
- duplicated explanation where short conditionals would work

## Drift signals
- same policy restated at multiple hierarchy levels
- same topic with different values
- stale model references
- TODO/FIXME notes inside always-loaded instructions
- runtime copies of one skill with different content hashes

## Delete safety principles
High-confidence delete candidates usually live in:
- `node_modules`
- cache/temp/plugin-cache paths
- archive/backup paths
- obvious mirror/sync dump trees
- exact duplicate copies once one canonical source is preserved

Large unique files are usually **EXTRACT** or **SPLIT**, not **DELETE**.

## Reporting principles
Every final report should answer:
1. What likely hurts real sessions?
2. What is just storage/maintenance duplication?
3. What is safe to delete now?
4. What needs manual review?
5. What should become one canonical source plus generated/runtime copies?
