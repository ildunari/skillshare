#!/usr/bin/env python3
"""Create a self-evolve-codex run folder with goal/log scaffolding."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    keep = []
    for ch in value.lower():
        if ch.isalnum():
            keep.append(ch)
        elif keep and keep[-1] != "-":
            keep.append("-")
    return "".join(keep).strip("-") or "target"


def copy_target(target: Path, destination: Path) -> None:
    if target.is_dir():
        shutil.copytree(target, destination)
    elif target.is_file():
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, destination / target.name)
    else:
        raise SystemExit(f"Target does not exist: {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Skill, prompt, plugin, or file to evolve")
    parser.add_argument("--objective", required=True, help="One-sentence improvement objective")
    parser.add_argument("--metrics", default="plugin-eval score, required checks, behavioral evals")
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--hours", type=float, default=None)
    default_run_root = Path.home() / ".codex" / "evolution-runs" / "self-evolve-codex"
    parser.add_argument("--run-root", type=Path, default=default_run_root)
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = args.run_root.expanduser() / timestamp / slugify(target.stem if target.is_file() else target.name)
    original_dir = run_dir / "original"
    candidate_dir = run_dir / "candidate"
    run_dir.mkdir(parents=True, exist_ok=False)
    copy_target(target, original_dir / target.name)
    copy_target(target, candidate_dir / target.name)

    goal = f"""# Self-Evolve Codex Goal

## Objective

{args.objective}

## Target

- Canonical source: {target}
- Candidate copy: {candidate_dir / target.name}
- Editable surface: candidate copy only until finalist review
- Read-only benchmark fixtures: original source and current metric commands

## Metrics

- {args.metrics}

## Limits

- Maximum iterations: {args.max_iterations}
- Wall-clock budget hours: {args.hours if args.hours is not None else "not specified"}
- Plateau: stop after 3 consecutive completed iterations improve the primary score by less than 2 points total

## Loop

1. Record the baseline before editing.
2. Make one focused candidate change.
3. Run the same benchmark.
4. Keep winners, discard regressions, and log the evidence.
"""
    (run_dir / "GOAL.md").write_text(goal, encoding="utf-8")
    runlog = "\n".join(
        [
            "# Self-Evolve Run Log",
            "",
            f"- Target: {target}",
            f"- Started: {timestamp} UTC",
            f"- Goal: {args.objective}",
            "",
            "## Baseline",
            "",
            "Pending.",
            "",
            "## Iterations",
            "",
        ]
    )
    (run_dir / "RUNLOG.md").write_text(runlog, encoding="utf-8")
    (run_dir / "DECISIONS.md").write_text("# Decisions\n\n", encoding="utf-8")
    (run_dir / "metrics.jsonl").write_text("", encoding="utf-8")
    (run_dir / "run.json").write_text(
        json.dumps(
            {
                "target": str(target),
                "run_dir": str(run_dir),
                "objective": args.objective,
                "metrics": args.metrics,
                "max_iterations": args.max_iterations,
                "hours": args.hours,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
