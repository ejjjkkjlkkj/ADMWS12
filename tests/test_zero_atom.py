from src.zero.atom import Atom, AtomError, atom_id, canonical_bytes, verify_envelope


def test_canonical_json_ignores_mapping_order():
    assert canonical_bytes({"b": 2, "a": 1}) == canonical_bytes({"a": 1, "b": 2})


def test_same_content_has_same_id():
    left = atom_id("concept", 1, {"b": 2, "a": 1})
    right = atom_id("concept", 1, {"a": 1, "b": 2})
    assert left == right


def test_payload_change_changes_id():
    assert atom_id("concept", 1, {"value": 1}) != atom_id("concept", 1, {"value": 2})


def test_provenance_is_required():
    try:
        Atom("concept", 1, {"value": 1}, {})
    except AtomError:
        pass
    else:
        raise AssertionError("empty provenance must be rejected")


def test_envelope_verifies():
    atom = Atom("concept", 1, {"value": "zero"}, {"origin": "admws12"})
    verify_envelope(atom.envelope())


def test_tampered_envelope_is_rejected():
    atom = Atom("concept", 1, {"value": "zero"}, {"origin": "admws12"})
    envelope = atom.envelope()
    envelope["payload"] = {"value": "tampered"}
    try:
        verify_envelope(envelope)
    except AtomError:
        pass
    else:
        raise AssertionError("tampered content must be rejected")
