from pathlib import Path
import json


def test_uefi_source_metadata():
    path = Path("data/metadata/sources/uefi_2.11.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["version"] == "2.11"
    assert data["publisher"] == "UEFI Forum"
    assert data["repository_policy"]["raw_document"] == "do_not_commit"


def test_uefi_mapping():
    path = Path("data/metadata/uefi_2.11_mapping.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "uefi-specification-2.11" in data["sources"]
    assert "protocol_summary" in data["record_types"]
