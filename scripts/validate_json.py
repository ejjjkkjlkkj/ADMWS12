#!/usr/bin/env python3
"""Validate JSON metadata and JSONL dataset files used by ADMWS12."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def validate_json(path: Path) -> list[str]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]
    return []


def validate_jsonl(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"{path}: {exc}"]

    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{number}: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path}:{number}: record must be a JSON object")
    return errors


def main() -> int:
    roots = [Path("data/metadata"), Path("data/sft")]
    errors: list[str] = []

    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() == ".json":
                errors.extend(validate_json(path))
            elif path.suffix.lower() == ".jsonl":
                errors.extend(validate_jsonl(path))

    if errors:
        print("\n".join(errors))
        return 1

    print("ADMWS12 metadata validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
