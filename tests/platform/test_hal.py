import unittest

from src.platform.capability import Capability, CapabilityState
from src.platform.hal import PlatformContext
from src.platform.state import PlatformState


class StaticSource:
    def __init__(self, capabilities):
        self.capabilities = capabilities

    def discover(self):
        return self.capabilities


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

    def test_discovery_lifecycle(self):
        context = PlatformContext()
        context.begin_discovery()
        self.assertIs(context.state, PlatformState.DISCOVERING)

        result = context.complete_discovery(
            StaticSource([Capability("cpu", CapabilityState.AVAILABLE)])
        )

        self.assertIs(context.state, PlatformState.DISCOVERED)
        self.assertEqual(context.capabilities, result.capabilities)
        self.assertTrue(context.has("cpu"))

    def test_discovery_cannot_start_from_discovered(self):
        context = PlatformContext(state=PlatformState.DISCOVERED)
        with self.assertRaises(ValueError):
            context.begin_discovery()


if __name__ == "__main__":
    unittest.main()
