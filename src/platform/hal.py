"""Platform context and lifecycle integration."""
from dataclasses import dataclass
from .capability import Capability, CapabilityState
from .discovery import CapabilitySource, DiscoveryResult
from .state import PlatformState, transition


@dataclass
class PlatformContext:
    state: PlatformState = PlatformState.EMPTY
    capabilities: tuple[Capability, ...] = ()
    degraded_capabilities: tuple[str, ...] = ()
    failure_reason: str | None = None

    def has(self, name: str) -> bool:
        return any(c.name == name and c.usable() for c in self.capabilities)

    def begin_discovery(self) -> None:
        self.state = transition(self.state, PlatformState.DISCOVERING)

    def complete_discovery(self, source: CapabilitySource) -> DiscoveryResult:
        result = DiscoveryResult.from_source(source)
        self.capabilities = result.capabilities
        self.state = transition(self.state, PlatformState.DISCOVERED)
        return result

    def initialize(
        self,
        mandatory: tuple[str, ...] = (),
        optional: tuple[str, ...] = (),
    ) -> PlatformState:
        """Validate discovered capabilities and enter runtime state."""
        self.state = transition(self.state, PlatformState.INITIALIZING)

        if len(set(mandatory)) != len(mandatory):
            self.state = PlatformState.FAILED
            self.failure_reason = "duplicate mandatory capability name"
            raise ValueError(self.failure_reason)

        if len(set(optional)) != len(optional):
            self.state = PlatformState.FAILED
            self.failure_reason = "duplicate optional capability name"
            raise ValueError(self.failure_reason)

        overlap = set(mandatory) & set(optional)
        if overlap:
            self.state = PlatformState.FAILED
            self.failure_reason = "capability cannot be both mandatory and optional"
            raise ValueError(self.failure_reason)

        missing = tuple(name for name in mandatory if not self.has(name))
        if missing:
            self.state = PlatformState.FAILED
            self.failure_reason = "mandatory capabilities unavailable: " + ", ".join(missing)
            return self.state

        degraded = tuple(
            name
            for name in optional
            if not any(c.name == name and c.state is CapabilityState.AVAILABLE
                       for c in self.capabilities)
        )
        self.degraded_capabilities = degraded
        self.failure_reason = None

        target = PlatformState.DEGRADED if degraded else PlatformState.READY
        self.state = transition(self.state, target)
        return self.state
