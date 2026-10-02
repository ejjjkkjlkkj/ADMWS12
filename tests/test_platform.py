import unittest

from tests.platform.test_capability import CapabilityTests
from tests.platform.test_hal import PlatformContextTests
from tests.platform.test_state import PlatformStateTests


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for case in (CapabilityTests, PlatformContextTests, PlatformStateTests):
        suite.addTests(loader.loadTestsFromTestCase(case))
    return suite


if __name__ == "__main__":
    unittest.main()
