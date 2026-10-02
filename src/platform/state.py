"""Platform lifecycle state machine."""
from enum import Enum

class PlatformState(Enum):
    EMPTY="empty"
    DISCOVERING="discovering"
    DISCOVERED="discovered"
    INITIALIZING="initializing"
    READY="ready"
    DEGRADED="degraded"
    FAILED="failed"
    STOPPING="stopping"
    STOPPED="stopped"

_ALLOWED={
PlatformState.EMPTY:{PlatformState.DISCOVERING},
PlatformState.DISCOVERING:{PlatformState.DISCOVERED,PlatformState.FAILED},
PlatformState.DISCOVERED:{PlatformState.INITIALIZING},
PlatformState.INITIALIZING:{PlatformState.READY,PlatformState.DEGRADED,PlatformState.FAILED},
PlatformState.READY:{PlatformState.DEGRADED,PlatformState.STOPPING},
PlatformState.DEGRADED:{PlatformState.READY,PlatformState.STOPPING},
PlatformState.FAILED:set(),PlatformState.STOPPING:{PlatformState.STOPPED},PlatformState.STOPPED:set(),}

def can_transition(current: PlatformState, target: PlatformState) -> bool:
    return target in _ALLOWED[current]
