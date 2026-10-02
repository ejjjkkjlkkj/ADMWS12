from pathlib import Path

from scripts.dataset_quality import load_records, validate


def test_foundation_dataset_quality():
    path = Path("data/sft/uefi_foundation.jsonl")
    records = load_records(path)
    assert len(records) >= 4
    assert validate(records, path) == []
