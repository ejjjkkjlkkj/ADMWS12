"""Adapter-local evidence model."""

from enum import Enum


class EvidenceState(Enum):
    OBSERVED = "observed"
    ABSENT = "absent"
    UNSUPPORTED = "unsupported"
    FAILED = "failed"
    UNKNOWN = "unknown"
