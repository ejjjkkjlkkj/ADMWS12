#!/usr/bin/env python3
"""Run deterministic quality checks for ADMWS12 JSONL SFT datasets."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


REQUIRED_METADATA = {"source_id", "topic", "version", "record_type"}
ALLOWED_ROLES = {"user", "assistant"}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_records(path: Path) -> list[dict]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: record must be an object")
        records.append(value)
    return records


def validate(records: list[dict], path: Path) -> list[str]:
    errors: list[str] = []
    prompt_hashes: Counter[str] = Counter()
    answer_hashes: Counter[str] = Counter()

    for number, record in enumerate(records, 1):
        messages = record.get("messages")
        metadata = record.get("metadata")
        if not isinstance(messages, list) or not messages:
            errors.append(f"{path}:{number}: messages must be a non-empty list")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"{path}:{number}: metadata must be an object")
            continue

        missing = REQUIRED_METADATA - metadata.keys()
        if missing:
            errors.append(
                f"{path}:{number}: missing metadata: {', '.join(sorted(missing))}"
            )

        roles = [m.get("role") for m in messages if isinstance(m, dict)]
        if any(role not in ALLOWED_ROLES for role in roles):
            errors.append(f"{path}:{number}: invalid message role")

        contents = [m.get("content", "") for m in messages if isinstance(m, dict)]
        if any(not isinstance(content, str) or not content.strip() for content in contents):
            errors.append(f"{path}:{number}: empty message content")

        user_text = "\n".join(
            m["content"] for m in messages
            if isinstance(m, dict) and m.get("role") == "user"
        )
        assistant_text = "\n".join(
            m["content"] for m in messages
            if isinstance(m, dict) and m.get("role") == "assistant"
        )
        if user_text:
            prompt_hashes[digest(user_text)] += 1
        if assistant_text:
            answer_hashes[digest(assistant_text)] += 1

    for key, count in prompt_hashes.items():
        if count > 1:
            errors.append(f"{path}: duplicate user prompt hash {key}")
    for key, count in answer_hashes.items():
        if count > 1:
            errors.append(f"{path}: duplicate assistant answer hash {key}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    records = load_records(args.path)
    errors = validate(records, args.path)
    if errors:
        print("\n".join(errors))
        return 1

    topics = Counter(
        record["metadata"]["topic"]
        for record in records
        if isinstance(record.get("metadata"), dict) and "topic" in record["metadata"]
    )
    print(f"records={len(records)}")
    print(f"topics={len(topics)}")
    for topic, count in sorted(topics.items()):
        print(f"topic={topic} count={count}")
    print("dataset quality: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
