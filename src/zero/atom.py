"""First-principles immutable atom representation for ADMWS12."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

SCHEMA = "admws12/atom/1"

class AtomError(ValueError):
    """Raised when an atom violates zero-layer invariants."""


def canonical_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise AtomError("payload is not canonical JSON data: " + str(exc)) from exc
    return text.encode("utf-8")


def atom_id(kind: str, version: int, payload: Any) -> str:
    material = canonical_bytes({"kind": kind, "version": version, "payload": payload})
    return hashlib.sha256(material).hexdigest()

@dataclass(frozen=True)
class Atom:
    """Immutable, content-addressed project primitive."""
    kind: str
    version: int
    payload: Any
    provenance: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise AtomError("kind must be a non-empty string")
        if not isinstance(self.version, int) or self.version < 1:
            raise AtomError("version must be a positive integer")
        if not isinstance(self.provenance, Mapping) or not self.provenance:
            raise AtomError("provenance must be a non-empty mapping")
        canonical_bytes(self.payload)
        canonical_bytes(dict(self.provenance))

    @property
    def id(self) -> str:
        return atom_id(self.kind, self.version, self.payload)

    def envelope(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "atom_id": self.id,
            "kind": self.kind,
            "version": self.version,
            "payload": self.payload,
            "provenance": dict(self.provenance),
        }

    def verify(self) -> None:
        if self.id != atom_id(self.kind, self.version, self.payload):
            raise AtomError("atom identity mismatch")


def verify_envelope(envelope: Mapping[str, Any]) -> None:
    required = {"schema", "atom_id", "kind", "version", "payload", "provenance"}
    missing = required - envelope.keys()
    if missing:
        raise AtomError("missing envelope fields: " + ", ".join(sorted(missing)))
    if envelope["schema"] != SCHEMA:
        raise AtomError("unsupported schema: " + repr(envelope["schema"]))
    expected = atom_id(envelope["kind"], envelope["version"], envelope["payload"])
    if envelope["atom_id"] != expected:
        raise AtomError("atom_id does not match canonical content")
    Atom(envelope["kind"], envelope["version"], envelope["payload"], envelope["provenance"])
