from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_self_evolve_run.py"


class InitSelfEvolveRunTests(unittest.TestCase):
    def test_creates_durable_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            target = tmp_path / "sample-skill"
            target.mkdir()
            (target / "SKILL.md").write_text(
                "---\nname: sample\n"
                "description: Use when testing the scaffold.\n---\n\n# Sample\n",
                encoding="utf-8",
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(target),
                    "--objective",
                    "Improve sample routing",
                    "--max-iterations",
                    "2",
                    "--run-root",
                    str(tmp_path / "runs"),
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            run_dir = Path(proc.stdout.strip())

            self.assertTrue((run_dir / "GOAL.md").exists())
            self.assertTrue((run_dir / "RUNLOG.md").exists())
            self.assertEqual((run_dir / "metrics.jsonl").read_text(encoding="utf-8"), "")
            self.assertTrue((run_dir / "original" / "sample-skill" / "SKILL.md").exists())
            self.assertTrue((run_dir / "candidate" / "sample-skill" / "SKILL.md").exists())

            run_json = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(run_json["objective"], "Improve sample routing")
            self.assertEqual(run_json["max_iterations"], 2)


if __name__ == "__main__":
    unittest.main()
