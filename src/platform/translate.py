"""Translate adapter evidence into core capability states."""
from .capability import Capability, CapabilityState
from .evidence import EvidenceState
from .evidence_record import Evidence


def capability_from_evidence(name: str, evidence: Evidence) -> Capability:
    if not name:
        raise ValueError("capability name must not be empty")
    states = {
        EvidenceState.OBSERVED: CapabilityState.AVAILABLE,
        EvidenceState.ABSENT: CapabilityState.UNAVAILABLE,
        EvidenceState.UNSUPPORTED: CapabilityState.UNSUPPORTED,
        EvidenceState.FAILED: CapabilityState.FAILED,
        EvidenceState.UNKNOWN: CapabilityState.UNKNOWN,
    }
    return Capability(name=name, state=states[evidence.state])
