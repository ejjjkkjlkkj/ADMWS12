import unittest

from src.platform.capability import Capability, CapabilityState
from src.platform.discovery import DiscoveryResult


class StaticSource:
    def __init__(self, capabilities):
        self.capabilities = capabilities

    def discover(self):
        return self.capabilities


class DiscoveryTests(unittest.TestCase):
    def test_discovery_creates_immutable_snapshot(self):
        source = StaticSource([Capability("cpu", CapabilityState.AVAILABLE)])
        result = DiscoveryResult.from_source(source)

        self.assertEqual(
            result.capabilities,
            (Capability("cpu", CapabilityState.AVAILABLE),),
        )
        self.assertIsInstance(result.capabilities, tuple)

    def test_duplicate_names_are_rejected(self):
        source = StaticSource([Capability("cpu"), Capability("cpu")])
        with self.assertRaises(ValueError):
            DiscoveryResult.from_source(source)

    def test_empty_name_is_rejected(self):
        source = StaticSource([Capability("")])
        with self.assertRaises(ValueError):
            DiscoveryResult.from_source(source)


if __name__ == "__main__":
    unittest.main()
