from pathlib import Path
import json


def test_uefi_source_metadata():
    data = json.loads(
        Path("data/metadata/sources/uefi_2.11.json").read_text(encoding="utf-8")
    )
    assert data["version"] == "2.11"
    assert data["publisher"] == "UEFI Forum"
    assert data["repository_policy"]["raw_document"] == "do_not_commit"


def test_uefi_mapping():
    data = json.loads(
        Path("data/metadata/uefi_2.11_mapping.json").read_text(encoding="utf-8")
    )
    assert "uefi-specification-2.11" in data["sources"]
    assert "protocol_summary" in data["record_types"]


def test_uefi_sft_records():
    path = Path("data/sft/uefi_foundation.jsonl")
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(records) >= 4
    for record in records:
        assert record["messages"]
        assert {"source_id", "topic", "version", "record_type"} <= record["metadata"].keys()
