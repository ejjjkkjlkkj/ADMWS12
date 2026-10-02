"""Blank-slate capability model."""
from dataclasses import dataclass
from enum import Enum

class CapabilityState(Enum):
    UNKNOWN="unknown"
    AVAILABLE="available"
    UNAVAILABLE="unavailable"
    UNSUPPORTED="unsupported"
    FAILED="failed"

@dataclass(frozen=True)
class Capability:
    name: str
    state: CapabilityState = CapabilityState.UNKNOWN
    value: object | None = None

    def usable(self) -> bool:
        return self.state is CapabilityState.AVAILABLE
