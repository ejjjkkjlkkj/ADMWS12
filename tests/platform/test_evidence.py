import unittest

from src.platform.capability import CapabilityState
from src.platform.evidence import EvidenceState
from src.platform.evidence_record import Evidence
from src.platform.translate import capability_from_evidence


class EvidenceTests(unittest.TestCase):
    def test_observed_maps_to_available(self):
        c = capability_from_evidence("execution.width", Evidence("cpu.width", EvidenceState.OBSERVED, 64))
        self.assertIs(c.state, CapabilityState.AVAILABLE)

    def test_absent_maps_to_unavailable(self):
        c = capability_from_evidence("network.wifi", Evidence("network.radio", EvidenceState.ABSENT))
        self.assertIs(c.state, CapabilityState.UNAVAILABLE)

    def test_failed_maps_to_failed(self):
        c = capability_from_evidence("firmware.mode", Evidence("firmware.query", EvidenceState.FAILED))
        self.assertIs(c.state, CapabilityState.FAILED)

    def test_unknown_maps_to_unknown(self):
        c = capability_from_evidence("display.output", Evidence("display.query", EvidenceState.UNKNOWN))
        self.assertIs(c.state, CapabilityState.UNKNOWN)

    def test_empty_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            Evidence("", EvidenceState.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
