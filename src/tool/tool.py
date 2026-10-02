"""First-principles deterministic tool contract built on components."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

SCHEMA = "admws12/tool/1"


class ToolError(ValueError):
    """Raised when a tool violates tool-layer invariants."""


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
        raise ToolError("value is not canonical JSON data: " + str(exc)) from exc


def tool_id(
    name: str,
    version: int,
    component_ids: Sequence[str],
    input_schema: Any,
    output_schema: Any,
    policy: Any,
) -> str:
    material = _canonical(
        {
            "name": name,
            "version": version,
            "component_ids": list(component_ids),
            "input_schema": input_schema,
            "output_schema": output_schema,
            "policy": policy,
        }
    )
    return hashlib.sha256(material).hexdigest()


@dataclass(frozen=True)
class Tool:
    """Immutable description of a project-owned executable capability."""

    name: str
    version: int
    component_ids: tuple[str, ...]
    input_schema: Any
    output_schema: Any
    policy: Any
    provenance: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ToolError("name must be a non-empty string")
        if not isinstance(self.version, int) or self.version < 1:
            raise ToolError("version must be a positive integer")
        if not self.component_ids:
            raise ToolError("tool must contain at least one component")
        if any(
            not isinstance(value, str)
            or len(value) != 64
            or any(char not in "0123456789abcdef" for char in value)
            for value in self.component_ids
        ):
            raise ToolError("component_ids must be lowercase SHA-256 identities")
        if len(set(self.component_ids)) != len(self.component_ids):
            raise ToolError("component_ids must be unique")
        if not isinstance(self.provenance, Mapping) or not self.provenance:
            raise ToolError("provenance must be a non-empty mapping")
        _canonical(self.input_schema)
        _canonical(self.output_schema)
        _canonical(self.policy)
        _canonical(dict(self.provenance))

    @property
    def id(self) -> str:
        return tool_id(
            self.name,
            self.version,
            self.component_ids,
            self.input_schema,
            self.output_schema,
            self.policy,
        )

    def envelope(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "tool_id": self.id,
            "name": self.name,
            "version": self.version,
            "component_ids": list(self.component_ids),
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "policy": self.policy,
            "provenance": dict(self.provenance),
        }

    def verify(self) -> None:
        expected = tool_id(
            self.name,
            self.version,
            self.component_ids,
            self.input_schema,
            self.output_schema,
            self.policy,
        )
        if self.id != expected:
            raise ToolError("tool identity mismatch")


def verify_tool(envelope: Mapping[str, Any]) -> None:
    required = {
        "schema",
        "tool_id",
        "name",
        "version",
        "component_ids",
        "input_schema",
        "output_schema",
        "policy",
        "provenance",
    }
    missing = required - envelope.keys()
    if missing:
        raise ToolError("missing tool fields: " + ", ".join(sorted(missing)))
    if envelope["schema"] != SCHEMA:
        raise ToolError("unsupported schema: " + repr(envelope["schema"]))
    tool = Tool(
        envelope["name"],
        envelope["version"],
        tuple(envelope["component_ids"]),
        envelope["input_schema"],
        envelope["output_schema"],
        envelope["policy"],
        envelope["provenance"],
    )
    if envelope["tool_id"] != tool.id:
        raise ToolError("tool_id does not match canonical content")
