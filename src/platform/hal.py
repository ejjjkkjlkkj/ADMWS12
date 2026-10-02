"""Platform context and discovery lifecycle integration."""
from dataclasses import dataclass
from .capability import Capability
from .discovery import CapabilitySource, DiscoveryResult
from .state import PlatformState, transition


@dataclass
class PlatformContext:
    state: PlatformState = PlatformState.EMPTY
    capabilities: tuple[Capability, ...] = ()

    def has(self, name: str) -> bool:
        return any(c.name == name and c.usable() for c in self.capabilities)

    def begin_discovery(self) -> None:
        self.state = transition(self.state, PlatformState.DISCOVERING)

    def complete_discovery(self, source: CapabilitySource) -> DiscoveryResult:
        result = DiscoveryResult.from_source(source)
        self.capabilities = result.capabilities
        self.state = transition(self.state, PlatformState.DISCOVERED)
        return result
