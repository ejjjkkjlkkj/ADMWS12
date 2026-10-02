import unittest

from src.platform.capability import Capability, CapabilityState


class CapabilityTests(unittest.TestCase):
    def test_unknown_is_not_usable(self):
        self.assertFalse(Capability("cpu").usable())

    def test_only_available_is_usable(self):
        for state in (
            CapabilityState.UNAVAILABLE,
            CapabilityState.UNSUPPORTED,
            CapabilityState.FAILED,
        ):
            self.assertFalse(Capability("cpu", state).usable())

        self.assertTrue(Capability("cpu", CapabilityState.AVAILABLE).usable())


if __name__ == "__main__":
    unittest.main()
