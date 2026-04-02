#!/usr/bin/env python3
"""Validate a deck IR JSON file against the bundled JSON schema.

Usage:
  python scripts/validate_ir.py deck.ir.json

Exit code:
  0 if valid, 1 if invalid.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"Failed to read JSON from {path}: {e}")


def _basic_validate(instance: Dict[str, Any]) -> List[Dict[str, str]]:
    errors: List[Dict[str, str]] = []

    if "deck" not in instance:
        errors.append({"path": "<root>", "message": "Missing top-level 'deck'"})
        return errors

    deck = instance["deck"]
    if not isinstance(deck, dict):
        errors.append({"path": "deck", "message": "'deck' must be an object"})
        return errors

    if "tokens" not in deck:
        errors.append({"path": "deck", "message": "deck must include 'tokens'"})
    if "slides" not in deck:
        errors.append({"path": "deck", "message": "deck must include 'slides'"})

    slides = deck.get("slides")
    if slides is not None and (not isinstance(slides, list) or not slides):
        errors.append({"path": "deck/slides", "message": "deck.slides must be a non-empty list"})

    return errors


def validate_instance(instance: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[str, List[Dict[str, str]]]:
    """Return (engine, errors) for IR validation."""
    try:
        import jsonschema

        validator = jsonschema.Draft202012Validator(schema)
        raw_errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        errors = []
        for err in raw_errors:
            path = "/".join(str(p) for p in err.path) or "<root>"
            errors.append({"path": path, "message": err.message})
        return "jsonschema", errors
    except Exception:
        return "basic", _basic_validate(instance)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_ir.py <deck.ir.json>")
        return 2

    ir_path = Path(sys.argv[1]).resolve()
    if not ir_path.exists():
        print(f"File not found: {ir_path}")
        return 2

    schema_path = Path(__file__).resolve().parent.parent / "references" / "ir.schema.json"
    if not schema_path.exists():
        print(f"Schema not found: {schema_path}")
        return 2

    instance = _load_json(ir_path)
    schema = _load_json(schema_path)

    engine, errors = validate_instance(instance, schema)
    if errors:
        print("❌ IR validation failed:\n")
        for err in errors[:50]:
            print(f"- {err['path']}: {err['message']}")
        if len(errors) > 50:
            print(f"... plus {len(errors) - 50} more")
        return 1

    if engine == "jsonschema":
        print("✅ IR is valid")
    else:
        print("✅ IR passed basic checks (jsonschema unavailable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
