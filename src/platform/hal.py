"""Minimal HAL boundary; hardware adapters are not implemented here."""
from dataclasses import dataclass
from .capability import Capability
from .state import PlatformState

@dataclass
class PlatformContext:
    state: PlatformState=PlatformState.EMPTY
    capabilities: tuple[Capability,...]=()

    def has(self,name: str)->bool:
        return any(c.name==name and c.usable() for c in self.capabilities)
