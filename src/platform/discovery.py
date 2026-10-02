"""Platform capability discovery boundary.

This module defines the discovery contract without binding the core to hardware,
firmware vendors, operating systems, or device identifiers.
"""
from dataclasses import dataclass
from typing import Protocol, Sequence

from .capability import Capability


class CapabilitySource(Protocol):
    """Source capable of observing platform capabilities."""

    def discover(self) -> Sequence[Capability]:
        """Return a snapshot of observable capabilities."""
        ...


@dataclass(frozen=True)
class DiscoveryResult:
    """Validated result of one discovery pass."""

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
