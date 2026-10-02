"""Adapter-local evidence record."""
from dataclasses import dataclass
from .evidence import EvidenceState


@dataclass(frozen=True)
class Evidence:
    kind: str
    state: EvidenceState
    value: object = None

    def __post_init__(self):
        if not self.kind:
            raise ValueError("evidence kind must not be empty")
