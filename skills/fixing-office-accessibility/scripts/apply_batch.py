#!/usr/bin/env python3
"""Apply an OfficeCLI batch with backup, validation, and automatic restore on failure."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_cmd(cmd: List[str]) -> Dict[str, Any]:
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    return {
        "command": " ".join(cmd),
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def default_backup_path(file_path: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return file_path.with_name(f"{file_path.name}.stage4-backup.{stamp}")


def load_commands(commands_path: Path) -> Any:
    data = json.loads(commands_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("commands JSON must be an array of OfficeCLI batch command objects")
    return data


def append_log(log_path: Optional[Path], entry: Dict[str, Any]) -> None:
    if not log_path:
        return
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run officecli batch, validate, and restore backup on failure.")
    parser.add_argument("--file", required=True, type=Path, help="Office document path")
    parser.add_argument("--commands", required=True, type=Path, help="JSON array of OfficeCLI batch commands")
    parser.add_argument("--backup", type=Path, help="Backup path; default is timestamped next to file")
    parser.add_argument("--log", type=Path, help="JSONL change log path")
    parser.add_argument("--dry-run", action="store_true", help="Validate command file and print planned work without writing")
    args = parser.parse_args()

    entry: Dict[str, Any] = {
        "type": "officecli_batch",
        "started_at": utc_now(),
        "document_path": str(args.file),
        "commands_path": str(args.commands),
        "backup_path": None,
        "restored_from_backup": False,
    }

    try:
        commands = load_commands(args.commands)
        entry["commands"] = commands
        if args.dry_run:
            entry["dry_run"] = True
            print(json.dumps(entry, indent=2))
            return 0

        if not args.file.exists():
            raise FileNotFoundError(f"Document not found: {args.file}")

        backup = args.backup or default_backup_path(args.file)
        if not backup.exists():
            shutil.copy2(args.file, backup)
        entry["backup_path"] = str(backup)

        batch = run_cmd(["officecli", "batch", str(args.file), "--input", str(args.commands), "--json"])
        entry["batch_result"] = batch

        validation = run_cmd(["officecli", "validate", str(args.file), "--json"])
        entry["validation_status"] = {
            "passed": validation["returncode"] == 0,
            "command": validation["command"],
            "checked_at": utc_now(),
            "stdout": validation["stdout"],
            "stderr": validation["stderr"],
        }

        if batch["returncode"] != 0 or validation["returncode"] != 0:
            shutil.copy2(backup, args.file)
            entry["restored_from_backup"] = True
            entry["finished_at"] = utc_now()
            append_log(args.log, entry)
            print(json.dumps(entry, indent=2), file=sys.stderr)
            return 1

        entry["finished_at"] = utc_now()
        append_log(args.log, entry)
        print(json.dumps(entry, indent=2))
        return 0
    except Exception as exc:  # noqa: BLE001
        entry["error"] = str(exc)
        entry["finished_at"] = utc_now()
        append_log(args.log, entry)
        print(json.dumps(entry, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
