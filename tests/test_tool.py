from src.tool.tool import Tool, ToolError, verify_tool


def component(seed: str) -> str:
    return (seed.encode("utf-8").hex() + "0" * 64)[:64]


def test_tool_identity_is_deterministic():
    components = (component("a"), component("b"))
    first = Tool("validator", 1, components, {"type": "object"}, {"type": "result"}, {"deterministic": True}, {"source": "component"})
    second = Tool("validator", 1, components, {"type": "object"}, {"type": "result"}, {"deterministic": True}, {"source": "component"})
    assert first.id == second.id


def test_policy_change_changes_identity():
    c = (component("a"),)
    first = Tool("validator", 1, c, {}, {}, {"deterministic": True}, {"source": "component"})
    second = Tool("validator", 1, c, {}, {}, {"deterministic": False}, {"source": "component"})
    assert first.id != second.id


def test_tool_requires_components():
    try:
        Tool("empty", 1, (), {}, {}, {}, {"source": "component"})
    except ToolError:
        return
    raise AssertionError("empty tool was accepted")


def test_tool_rejects_duplicate_components():
    c = component("a")
    try:
        Tool("duplicate", 1, (c, c), {}, {}, {}, {"source": "component"})
    except ToolError:
        return
    raise AssertionError("duplicate component identities were accepted")


def test_tool_envelope_verifies():
    tool = Tool("validator", 1, (component("a"),), {"type": "object"}, {"type": "result"}, {"deterministic": True}, {"source": "component"})
    verify_tool(tool.envelope())


def test_tampered_tool_is_rejected():
    tool = Tool("validator", 1, (component("a"),), {"type": "object"}, {"type": "result"}, {"deterministic": True}, {"source": "component"})
    envelope = tool.envelope()
    envelope["policy"]["deterministic"] = False
    try:
        verify_tool(envelope)
    except ToolError:
        return
    raise AssertionError("tampered tool was accepted")
