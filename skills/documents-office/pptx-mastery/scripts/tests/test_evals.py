import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVALS_JSON = ROOT / "evals" / "evals.json"


class EvalSchemaTests(unittest.TestCase):
    def test_eval_count_is_minimum_coverage(self):
        payload = json.loads(EVALS_JSON.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(payload.get("evals", [])), 15)

    def test_eval_ids_are_unique(self):
        payload = json.loads(EVALS_JSON.read_text(encoding="utf-8"))
        ids = [entry["id"] for entry in payload["evals"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_expected_outputs_are_measurable(self):
        payload = json.loads(EVALS_JSON.read_text(encoding="utf-8"))
        for entry in payload["evals"]:
            expected = entry.get("expected_output", "")
            self.assertRegex(
                expected,
                re.compile(r"\d"),
                msg=f"expected_output must contain measurable numeric criteria for eval id={entry.get('id')}",
            )
            self.assertGreaterEqual(
                len(entry.get("assertions", [])),
                4,
                msg=f"eval id={entry.get('id')} must include at least 4 assertions",
            )


if __name__ == "__main__":
    unittest.main()
