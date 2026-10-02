import json
from pathlib import Path


def test_zero_system_forbids_copied_foundations():
    data = json.loads(Path("configs/zero_system.json").read_text(encoding="utf-8"))
    policy = data["reuse_policy"]
    assert policy["copied_implementations"] is False
    assert policy["copied_binaries"] is False
    assert policy["copied_models_as_project_foundation"] is False


def test_zero_system_contains_language_model_and_firmware():
    data = json.loads(Path("configs/zero_system.json").read_text(encoding="utf-8"))
    domains = set(data["domains"])
    assert {"language", "model_architecture", "firmware"} <= domains


def test_layers_are_ordered():
    data = json.loads(Path("configs/zero_system.json").read_text(encoding="utf-8"))
    ids = [layer["id"] for layer in data["layers"]]
    assert ids == sorted(ids)
    assert ids[0] == "00"
    assert ids[-1] == "07"
