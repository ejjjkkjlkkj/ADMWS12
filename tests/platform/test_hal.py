import unittest

from src.platform.capability import Capability, CapabilityState
from src.platform.hal import PlatformContext


class PlatformContextTests(unittest.TestCase):
    def test_has_requires_available_capability(self):
        context = PlatformContext(
            capabilities=(
                Capability("cpu", CapabilityState.AVAILABLE),
                Capability("wifi", CapabilityState.UNAVAILABLE),
            )
        )
        self.assertTrue(context.has("cpu"))
        self.assertFalse(context.has("wifi"))
        self.assertFalse(context.has("gpu"))


if __name__ == "__main__":
    unittest.main()
