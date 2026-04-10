import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "evals" / "files" / "sample.deck.ir.json"


def _run(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return res.returncode, res.stdout


class SmokeTests(unittest.TestCase):
    def test_validate_ir_passes_sample(self):
        code, out = _run([sys.executable, str(ROOT / "scripts" / "validate_ir.py"), str(SAMPLE)])
        self.assertEqual(code, 0, out)

    def test_preflight_has_no_hard_fails_sample(self):
        preflight_script = ROOT / "scripts" / "preflight_ir.py"
        out_json = ROOT / "evals" / "files" / "_tmp.qa.json"
        out_md = ROOT / "evals" / "files" / "_tmp.qa.md"
        try:
            code, out = _run([
                sys.executable,
                str(preflight_script),
                str(SAMPLE),
                "--out",
                str(out_json),
                "--md",
                str(out_md),
            ])
            self.assertEqual(code, 0, out)
            report = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(report["summary"]["hard_fail"], 0, json.dumps(report["summary"], indent=2))
        finally:
            if out_json.exists():
                out_json.unlink()
            if out_md.exists():
                out_md.unlink()


if __name__ == "__main__":
    unittest.main()
