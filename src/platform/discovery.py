"""Platform capability discovery boundary.

The core receives capability facts, not hardware identities. Hardware-specific
adapters implement CapabilitySource outside this module.
"""
from dataclasses import dataclass
from typing import Protocol, Sequence

from .capability import Capability


class CapabilitySource(Protocol):
    """Hardware-independent contract for one discovery pass."""

    def discover(self) -> Sequence[Capability]:
        """Return observable platform capabilities."""
        ...


@dataclass(frozen=True)
class DiscoveryResult:
    """Validated immutable result of one discovery pass."""

    capabilities: tuple[Capability, ...]

    @classmethod
    def from_source(cls, source: CapabilitySource) -> "DiscoveryResult":
        capabilities = tuple(source.discover())
        names = [capability.name for capability in capabilities]

        if any(not name for name in names):
            raise ValueError("capability names must not be empty")
        if len(names) != len(set(names)):
            raise ValueError("capability names must be unique")

        return cls(capabilities)
