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

    def test_initialize_reaches_ready_when_mandatory_capabilities_are_available(self):
        context = PlatformContext()
        context.begin_discovery()
        context.complete_discovery(
            StaticSource([
                Capability("cpu", CapabilityState.AVAILABLE),
                Capability("memory", CapabilityState.AVAILABLE),
            ])
        )

        state = context.initialize(mandatory=("cpu", "memory"))

        self.assertIs(state, PlatformState.READY)
        self.assertIs(context.state, PlatformState.READY)
        self.assertEqual(context.degraded_capabilities, ())
        self.assertIsNone(context.failure_reason)

    def test_initialize_enters_degraded_for_missing_optional_capability(self):
        context = PlatformContext()
        context.begin_discovery()
        context.complete_discovery(
            StaticSource([Capability("cpu", CapabilityState.AVAILABLE)])
        )

        state = context.initialize(
            mandatory=("cpu",),
            optional=("wifi", "gpu"),
        )

        self.assertIs(state, PlatformState.DEGRADED)
        self.assertEqual(context.degraded_capabilities, ("wifi", "gpu"))

    def test_initialize_fails_when_mandatory_capability_is_unavailable(self):
        context = PlatformContext()
        context.begin_discovery()
        context.complete_discovery(
            StaticSource([
                Capability("cpu", CapabilityState.AVAILABLE),
                Capability("memory", CapabilityState.UNAVAILABLE),
            ])
        )

        state = context.initialize(mandatory=("cpu", "memory"))

        self.assertIs(state, PlatformState.FAILED)
        self.assertIs(context.state, PlatformState.FAILED)
        self.assertIn("memory", context.failure_reason)

    def test_initialize_rejects_mandatory_optional_overlap(self):
        context = PlatformContext(state=PlatformState.DISCOVERED)

        with self.assertRaises(ValueError):
            context.initialize(mandatory=("cpu",), optional=("cpu",))

        self.assertIs(context.state, PlatformState.FAILED)

    def test_discovery_cannot_start_from_discovered(self):
        context = PlatformContext(state=PlatformState.DISCOVERED)
        with self.assertRaises(ValueError):
            context.begin_discovery()


if __name__ == "__main__":
    unittest.main()
