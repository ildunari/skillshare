#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent


def write_skill(path: Path, name: str, description: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        textwrap.dedent(
            f"""\
            ---
            name: {name}
            description: {description}
            ---

            # {name}
            """
        )
    )


def run_script(script: str, *args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(SCRIPTS_DIR / script), *args]
    return subprocess.run(cmd, check=True, env=env, capture_output=True, text=True)


class SkillCleanupPipelineTests(unittest.TestCase):
    def test_canonical_source_mode_supports_current_discovery_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_root = tmp_path / "source"
            codex_root = tmp_path / "codex"
            claude_root = tmp_path / "claude"
            source_skill = source_root / "alpha" / "SKILL.md"
            codex_skill = codex_root / "alpha" / "SKILL.md"
            write_skill(source_skill, "alpha", "Use when the user asks to audit a shared skill library.")
            write_skill(codex_skill, "alpha", "Use when the user asks to audit a shared skill library.")

            config_path = tmp_path / "config.yaml"
            config_path.write_text(
                textwrap.dedent(
                    f"""\
                    source: {source_root}
                    mode: copy
                    targets:
                      codex:
                        skills:
                          path: {codex_root}
                      claude:
                        skills:
                          path: {claude_root}
                    """
                )
            )

            discovery_path = tmp_path / "discovery.json"
            discovery_path.write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "path": str(source_skill),
                                "name": "alpha",
                                "entity_type": "skill",
                                "hash": "hash-alpha",
                                "agent_runtime": "unknown",
                                "ref_count": 0,
                                "script_count": 0,
                            },
                            {
                                "path": str(codex_skill),
                                "name": "alpha",
                                "entity_type": "skill",
                                "hash": "hash-alpha",
                                "agent_runtime": "codex-cli",
                                "ref_count": 0,
                                "script_count": 0,
                            },
                        ]
                    }
                )
            )

            env = os.environ.copy()
            env["SKILLSHARE_CONFIG_PATH"] = str(config_path)

            topology_path = tmp_path / "topology.json"
            run_script("analyze_skillshare_topology.py", str(discovery_path), "--output", str(topology_path), env=env)
            topology = json.loads(topology_path.read_text())
            self.assertEqual(topology["summary"]["mode"], "canonical-source")
            self.assertEqual(topology["summary"]["skill_count"], 1)

            drift_path = tmp_path / "drift.json"
            run_script("compare_canonical_vs_installs.py", str(topology_path), "--output", str(drift_path), env=env)
            drift = json.loads(drift_path.read_text())
            self.assertEqual(drift["summary"]["row_count"], 2)
            self.assertEqual(drift["summary"]["in_sync"], 1)
            self.assertEqual(drift["summary"]["undistributed_source"], 1)

            capabilities_path = tmp_path / "capabilities.json"
            run_script("extract_skill_capabilities.py", str(discovery_path), "--output", str(capabilities_path), env=env)
            capabilities = json.loads(capabilities_path.read_text())
            self.assertEqual(capabilities["summary"]["skill_count"], 2)

            duplicates_path = tmp_path / "duplicates.json"
            run_script("cluster_skill_duplicates.py", str(discovery_path), "--output", str(duplicates_path), env=env)
            duplicates = json.loads(duplicates_path.read_text())
            self.assertEqual(duplicates["summary"]["cluster_count"], 1)

    def test_broad_sweep_mode_supports_legacy_discovery_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            claude_skill = tmp_path / ".claude" / "skills" / "alpha" / "SKILL.md"
            codex_skill = tmp_path / ".codex" / "skills" / "beta" / "SKILL.md"
            write_skill(claude_skill, "alpha", "Use when the user asks to audit a distributed skill library.")
            write_skill(codex_skill, "beta", "Use when the user asks to audit a distributed skill library.")

            discovery_path = tmp_path / "discovery.json"
            discovery_path.write_text(
                json.dumps(
                    {
                        "items": [
                            {
                                "path": str(claude_skill),
                                "slug": "alpha",
                                "entity_type": "skill",
                                "content_hash": "hash-alpha",
                                "runtime": "claude-code",
                                "role": "runtime-install",
                                "reference_count": 0,
                                "script_count": 0,
                            },
                            {
                                "path": str(codex_skill),
                                "slug": "beta",
                                "entity_type": "skill",
                                "content_hash": "hash-beta",
                                "runtime": "codex-cli",
                                "role": "runtime-install",
                                "reference_count": 0,
                                "script_count": 0,
                            },
                        ]
                    }
                )
            )

            env = os.environ.copy()
            env["SKILLSHARE_CONFIG_PATH"] = str(tmp_path / "missing-config.yaml")

            topology_path = tmp_path / "topology.json"
            run_script("analyze_skillshare_topology.py", str(discovery_path), "--output", str(topology_path), env=env)
            topology = json.loads(topology_path.read_text())
            self.assertEqual(topology["summary"]["mode"], "broad-sweep")
            self.assertEqual(topology["summary"]["skill_count"], 2)
            self.assertEqual(topology["summary"]["runtime_count"], 2)

            drift_path = tmp_path / "drift.json"
            run_script("compare_canonical_vs_installs.py", str(topology_path), "--output", str(drift_path), env=env)
            drift = json.loads(drift_path.read_text())
            self.assertTrue(drift["summary"]["not_applicable"])

            capabilities_path = tmp_path / "capabilities.json"
            run_script("extract_skill_capabilities.py", str(discovery_path), "--output", str(capabilities_path), env=env)
            capabilities = json.loads(capabilities_path.read_text())
            self.assertEqual(capabilities["summary"]["skill_count"], 2)

            collisions_path = tmp_path / "collisions.json"
            run_script("detect_routing_collisions.py", str(capabilities_path), "--output", str(collisions_path), env=env)
            collisions = json.loads(collisions_path.read_text())
            self.assertGreaterEqual(collisions["summary"]["collision_count"], 1)

            duplicates_path = tmp_path / "duplicates.json"
            duplicates_path.write_text(json.dumps({"summary": {"cluster_count": 0}, "duplicate_clusters": []}))

            actions_path = tmp_path / "actions.json"
            run_script(
                "score_skill_actions.py",
                str(drift_path),
                str(duplicates_path),
                str(collisions_path),
                "--output",
                str(actions_path),
                env=env,
            )
            actions = json.loads(actions_path.read_text())
            self.assertTrue(actions["summary"]["drift_not_applicable"])
            self.assertEqual(actions["summary"]["mode"], "broad-sweep")
            self.assertGreaterEqual(len(actions["actions"]), 1)


if __name__ == "__main__":
    unittest.main()
