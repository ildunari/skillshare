# Suggested folder and file layout

Install the suite in an agent-compatible skills folder:

```text
project-root/
  .agents/
    skills/
      mlx-model-repo-audit/
        SKILL.md
        scripts/audit_hf_repo.py
      mlx-llm-conversion/
        SKILL.md
      mlx-vlm-conversion/
        SKILL.md
        scripts/svg_sanity_check.py
      mlx-embedding-reranker/
        SKILL.md
      mlx-quantization-quality/
        SKILL.md
      mlx-local-benchmarking/
        SKILL.md
        scripts/benchmark_command.py
      mlx-troubleshooting-repro/
        SKILL.md
        scripts/make_repro_note.py
      mlx-hub-packaging/
        SKILL.md
        scripts/check_mlx_package.py
  docs/
    research-brief.md
    recommended-suite.md
    agent-operating-policy.md
    vfig-qwen3-vl-case-study.md
    validation-checklists.md
    unresolved-risks.md
    source-notes.md
  evals/
    description-trigger-evals.json
```

For Claude Code, copy the skill folders to `.claude/skills/` or `~/.claude/skills/`. For Codex CLI, use `.codex/skills/` or `~/.codex/skills/`; do not mirror Codex skills into `.agents/skills/`, which Codex may also discover and show as duplicates. For other agents using the open skill format, keep each folder's `SKILL.md` and bundled scripts intact.
