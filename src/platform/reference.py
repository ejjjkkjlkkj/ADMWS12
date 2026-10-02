"""Reference capability source for tests and prototypes."""
from dataclasses import dataclass

from .capability import Capability


@dataclass(frozen=True)
class StaticCapabilitySource:
    """Return a predefined capability snapshot without hardware access."""

    capabilities: tuple[Capability, ...]

    def discover(self) -> tuple[Capability, ...]:
        return self.capabilities
