from src.component.component import Component, ComponentError, verify_component


def atom(seed: str) -> str:
    return (seed.encode("utf-8").hex() + "0" * 64)[:64]


def test_component_identity_is_deterministic():
    atoms = (atom("a"), atom("b"))
    first = Component("text_unit", 1, atoms, {"width": 8}, {"source": "zero"})
    second = Component("text_unit", 1, atoms, {"width": 8}, {"source": "zero"})
    assert first.id == second.id


def test_parameter_change_changes_identity():
    atoms = (atom("a"),)
    first = Component("text_unit", 1, atoms, {"width": 8}, {"source": "zero"})
    second = Component("text_unit", 1, atoms, {"width": 16}, {"source": "zero"})
    assert first.id != second.id


def test_component_requires_atoms():
    try:
        Component("empty", 1, (), {}, {"source": "zero"})
    except ComponentError:
        return
    raise AssertionError("empty component was accepted")


def test_component_rejects_duplicate_atoms():
    a = atom("a")
    try:
        Component("duplicate", 1, (a, a), {}, {"source": "zero"})
    except ComponentError:
        return
    raise AssertionError("duplicate atom identities were accepted")


def test_component_envelope_verifies():
    component = Component(
        "text_unit", 1, (atom("a"),), {"width": 8}, {"source": "zero"}
    )
    verify_component(component.envelope())


def test_tampered_component_is_rejected():
    component = Component(
        "text_unit", 1, (atom("a"),), {"width": 8}, {"source": "zero"}
    )
    envelope = component.envelope()
    envelope["parameters"]["width"] = 9
    try:
        verify_component(envelope)
    except ComponentError:
        return
    raise AssertionError("tampered component was accepted")
