"""First-principles deterministic chain contract built on tools."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

SCHEMA = "admws12/chain/1"


class ChainError(ValueError):
    """Raised when a chain violates chain-layer invariants."""


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ChainError("value is not canonical JSON data: " + str(exc)) from exc


def chain_id(
    name: str,
    version: int,
    tool_ids: Sequence[str],
    policy: Any,
) -> str:
    material = _canonical(
        {
            "name": name,
            "version": version,
            "tool_ids": list(tool_ids),
            "policy": policy,
        }
    )
    return hashlib.sha256(material).hexdigest()


@dataclass(frozen=True)
class Chain:
    """Immutable ordered composition of verified tool identities."""

    name: str
    version: int
    tool_ids: tuple[str, ...]
    policy: Any
    provenance: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ChainError("name must be a non-empty string")
        if not isinstance(self.version, int) or self.version < 1:
            raise ChainError("version must be a positive integer")
        if not self.tool_ids:
            raise ChainError("chain must contain at least one tool")
        if any(
            not isinstance(value, str)
            or len(value) != 64
            or any(char not in "0123456789abcdef" for char in value)
            for value in self.tool_ids
        ):
            raise ChainError("tool_ids must be lowercase SHA-256 identities")
        if not isinstance(self.provenance, Mapping) or not self.provenance:
            raise ChainError("provenance must be a non-empty mapping")
        _canonical(self.policy)
        _canonical(dict(self.provenance))

    @property
    def id(self) -> str:
        return chain_id(self.name, self.version, self.tool_ids, self.policy)

    def envelope(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "chain_id": self.id,
            "name": self.name,
            "version": self.version,
            "tool_ids": list(self.tool_ids),
            "policy": self.policy,
            "provenance": dict(self.provenance),
        }

    def verify(self) -> None:
        expected = chain_id(self.name, self.version, self.tool_ids, self.policy)
        if self.id != expected:
            raise ChainError("chain identity mismatch")


def verify_chain(envelope: Mapping[str, Any]) -> None:
    required = {"schema", "chain_id", "name", "version", "tool_ids", "policy", "provenance"}
    missing = required - envelope.keys()
    if missing:
        raise ChainError("missing chain fields: " + ", ".join(sorted(missing)))
    if envelope["schema"] != SCHEMA:
        raise ChainError("unsupported schema: " + repr(envelope["schema"]))
    chain = Chain(
        envelope["name"],
        envelope["version"],
        tuple(envelope["tool_ids"]),
        envelope["policy"],
        envelope["provenance"],
    )
    if envelope["chain_id"] != chain.id:
        raise ChainError("chain_id does not match canonical content")
