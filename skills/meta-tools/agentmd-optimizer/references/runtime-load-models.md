# Runtime Load Models

Use this reference when answering the question that matters most in instruction-file cleanup: **what actually loads together?**

## Core distinction

Keep these concepts separate at all times:

1. **Disk footprint** — files that exist somewhere on the machine
2. **Possible runtime load** — files that a runtime could consider, based on naming and location
3. **Likely session stack** — files that plausibly load together for one runtime from one working directory
4. **On-demand skill content** — metadata always visible, full body and bundled references only when the skill triggers

Do not collapse these categories into one number.

## Runtime heuristics

### Claude-style stacks
Typical hierarchy:
- global `~/.claude/CLAUDE.md`
- home-level `~/CLAUDE.md` where applicable
- project root `CLAUDE.md`
- deeper subdirectory `CLAUDE.md`
- triggered skills and their referenced files on demand

### Codex-style stacks
Typical hierarchy:
- global `~/.codex/AGENTS.md` and/or `~/.agents/AGENTS.md`
- project root `AGENTS.md`
- deeper subdirectory `AGENTS.md`
- Codex skills only when invoked or matched implicitly

### Gemini-style stacks
Typical hierarchy:
- global `~/.gemini/GEMINI.md`
- project/root `GEMINI.md`
- runtime-specific skill installs only when the runtime uses them

### Cursor-style stacks
These are often more fragmented:
- `.cursor/rules/*.mdc`
- sometimes nearby `CLAUDE.md` / `AGENTS.md` if reused across tools
- auto-activation may depend on file patterns rather than the directory alone

## Reporting rules

When presenting results:
- show **per-stack token totals**, not only machine totals
- show **runtime + project root** together
- mark whether the stack is **high / medium / low risk**
- explain when a scary duplicate cluster is likely a maintenance issue rather than a per-session load issue

## Visual recommendations

Prefer these diagrams:
- load-stack chain for one runtime + cwd
- session-impact matrix (runtime × project)
- duplicate cluster graphs separated from active stack graphs
