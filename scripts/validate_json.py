#!/usr/bin/env python3
"""Validate ADMWS12 JSON metadata and SFT JSONL files."""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED_SFT_METADATA = {"source_id", "topic", "version", "record_type"}
ALLOWED_ROLES = {"user", "assistant"}


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
            continue

        messages = value.get("messages")
        metadata = value.get("metadata")
        if not isinstance(messages, list) or not messages:
            errors.append(f"{path}:{number}: messages must be a non-empty list")
        else:
            for index, message in enumerate(messages, start=1):
                if not isinstance(message, dict):
                    errors.append(f"{path}:{number}: message {index} must be an object")
                    continue
                if message.get("role") not in ALLOWED_ROLES:
                    errors.append(f"{path}:{number}: invalid role in message {index}")
                if not isinstance(message.get("content"), str) or not message["content"].strip():
                    errors.append(f"{path}:{number}: empty content in message {index}")

        if not isinstance(metadata, dict):
            errors.append(f"{path}:{number}: metadata must be an object")
        else:
            missing = REQUIRED_SFT_METADATA - metadata.keys()
            if missing:
                errors.append(
                    f"{path}:{number}: missing metadata: {', '.join(sorted(missing))}"
                )

    return errors


def main() -> int:
    errors: list[str] = []

    for root in (Path("data/metadata"), Path("data/sft")):
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

    print("ADMWS12 metadata/SFT validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
