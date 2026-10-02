"""Project-owned deterministic component primitive built only on the zero layer."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

SCHEMA = "admws12/component/1"


class ComponentError(ValueError):
    """Raised when a component violates component-layer invariants."""


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
        raise ComponentError("value is not canonical JSON data: " + str(exc)) from exc


def component_id(kind: str, version: int, atom_ids: Sequence[str], parameters: Any) -> str:
    material = _canonical(
        {
            "kind": kind,
            "version": version,
            "atom_ids": list(atom_ids),
            "parameters": parameters,
        }
    )
    return hashlib.sha256(material).hexdigest()


@dataclass(frozen=True)
class Component:
    """Immutable composition of verified atom identities."""

    kind: str
    version: int
    atom_ids: tuple[str, ...]
    parameters: Any
    provenance: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ComponentError("kind must be a non-empty string")
        if not isinstance(self.version, int) or self.version < 1:
            raise ComponentError("version must be a positive integer")
        if not self.atom_ids:
            raise ComponentError("component must contain at least one atom")
        if any(
            not isinstance(atom, str)
            or len(atom) != 64
            or any(c not in "0123456789abcdef" for c in atom)
            for atom in self.atom_ids
        ):
            raise ComponentError("atom_ids must be lowercase SHA-256 identities")
        if len(set(self.atom_ids)) != len(self.atom_ids):
            raise ComponentError("atom_ids must be unique")
        if not isinstance(self.provenance, Mapping) or not self.provenance:
            raise ComponentError("provenance must be a non-empty mapping")
        _canonical(self.parameters)
        _canonical(dict(self.provenance))

    @property
    def id(self) -> str:
        return component_id(self.kind, self.version, self.atom_ids, self.parameters)

    def envelope(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "component_id": self.id,
            "kind": self.kind,
            "version": self.version,
            "atom_ids": list(self.atom_ids),
            "parameters": self.parameters,
            "provenance": dict(self.provenance),
        }

    def verify(self) -> None:
        expected = component_id(
            self.kind, self.version, self.atom_ids, self.parameters
        )
        if self.id != expected:
            raise ComponentError("component identity mismatch")


def verify_component(envelope: Mapping[str, Any]) -> None:
    required = {
        "schema",
        "component_id",
        "kind",
        "version",
        "atom_ids",
        "parameters",
        "provenance",
    }
    missing = required - envelope.keys()
    if missing:
        raise ComponentError("missing component fields: " + ", ".join(sorted(missing)))
    if envelope["schema"] != SCHEMA:
        raise ComponentError("unsupported schema: " + repr(envelope["schema"]))
    component = Component(
        envelope["kind"],
        envelope["version"],
        tuple(envelope["atom_ids"]),
        envelope["parameters"],
        envelope["provenance"],
    )
    if envelope["component_id"] != component.id:
        raise ComponentError("component_id does not match canonical content")
