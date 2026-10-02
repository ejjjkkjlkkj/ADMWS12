from src.chain.chain import Chain, ChainError, verify_chain


def tool(seed: str) -> str:
    return (seed.encode("utf-8").hex() + "0" * 64)[:64]


def test_chain_identity_is_deterministic():
    tools = (tool("a"), tool("b"))
    first = Chain("validation", 1, tools, {"ordered": True}, {"source": "tool"})
    second = Chain("validation", 1, tools, {"ordered": True}, {"source": "tool"})
    assert first.id == second.id


def test_tool_order_changes_identity():
    a, b = tool("a"), tool("b")
    first = Chain("flow", 1, (a, b), {"ordered": True}, {"source": "tool"})
    second = Chain("flow", 1, (b, a), {"ordered": True}, {"source": "tool"})
    assert first.id != second.id


def test_chain_requires_tools():
    try:
        Chain("empty", 1, (), {}, {"source": "tool"})
    except ChainError:
        return
    raise AssertionError("empty chain was accepted")


def test_chain_envelope_verifies():
    chain = Chain("flow", 1, (tool("a"),), {"ordered": True}, {"source": "tool"})
    verify_chain(chain.envelope())


def test_tampered_chain_is_rejected():
    chain = Chain("flow", 1, (tool("a"),), {"ordered": True}, {"source": "tool"})
    envelope = chain.envelope()
    envelope["policy"]["ordered"] = False
    try:
        verify_chain(envelope)
    except ChainError:
        return
    raise AssertionError("tampered chain was accepted")
