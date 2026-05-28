#!/usr/bin/env python3
"""Create a Hermes personality-skill self-evolution run scaffold."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    out = []
    for ch in value.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in {" ", "-", "_", "/"}:
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "personality-skill"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="Target personality skill name or path")
    ap.add_argument("--run-root", default=str(Path.home() / ".hermes/evolution-runs/personality-skills"))
    ap.add_argument("--source-skill", help="Optional existing skill directory to snapshot")
    args = ap.parse_args()

    target_slug = slugify(Path(args.target).name)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    root = Path(args.run_root).expanduser() / stamp / target_slug

    for rel in [
        "corpus/train", "corpus/dev", "corpus/holdout", "skill-original",
        "skill-candidate", "benchmark", "iteration-001", "dashboard"
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)

    if args.source_skill:
        src = Path(args.source_skill).expanduser()
        if src.exists():
            shutil.copytree(src, root / "skill-original" / src.name, dirs_exist_ok=True)
            shutil.copytree(src, root / "skill-candidate" / src.name, dirs_exist_ok=True)

    (root / "SPEC.md").write_text(f"""# Personality Skill Evolution Run\n\nTarget: {args.target}\nCreated: {stamp}\n\n## Goal\n\nBuild or improve a contextual writing-voice skill with fresh generator/reviewer/patcher loops.\n\n## Stop rule\n\nDefault: 10-30 loops or 4 plateau loops.\n\n## Notes\n\nKeep private examples local and redacted. Generator/patcher must not see holdout exemplar bodies.\n""")
    (root / "corpus/README.md").write_text("# Corpus\n\nPut train/dev/holdout examples here. Redact private details. Keep metadata in JSONL next to text files.\n")
    (root / "benchmark/tasks.jsonl").write_text("")
    (root / "benchmark/rubric.json").write_text(json.dumps({
        "weights": {
            "voice_fidelity": 0.22,
            "audience_register_fit": 0.16,
            "intent_preservation": 0.16,
            "fact_discipline": 0.16,
            "naturalness": 0.12,
            "brevity_density": 0.08,
            "boundary_handling": 0.05,
            "anti_pattern_avoidance": 0.05,
        },
        "auto_fail": ["invented_facts", "private_detail_leak", "wrong_relationship_or_stakes", "generic_customer_service_voice"]
    }, indent=2) + "\n")
    (root / "SUMMARY.md").write_text("# Summary\n\nNo iterations run yet.\n")

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
