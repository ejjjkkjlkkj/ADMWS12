import unittest

from src.platform.state import PlatformState, can_transition, transition


class PlatformStateTests(unittest.TestCase):
    def test_valid_transitions(self):
        valid = (
            (PlatformState.EMPTY, PlatformState.DISCOVERING),
            (PlatformState.DISCOVERING, PlatformState.DISCOVERED),
            (PlatformState.DISCOVERED, PlatformState.INITIALIZING),
            (PlatformState.INITIALIZING, PlatformState.READY),
            (PlatformState.READY, PlatformState.DEGRADED),
            (PlatformState.DEGRADED, PlatformState.READY),
            (PlatformState.READY, PlatformState.STOPPING),
            (PlatformState.STOPPING, PlatformState.STOPPED),
        )
        for current, target in valid:
            self.assertTrue(can_transition(current, target))
            self.assertIs(transition(current, target), target)

    def test_invalid_transition_is_rejected(self):
        self.assertFalse(can_transition(PlatformState.EMPTY, PlatformState.READY))
        with self.assertRaises(ValueError):
            transition(PlatformState.EMPTY, PlatformState.READY)

    def test_terminal_states_are_terminal(self):
        for state in (PlatformState.FAILED, PlatformState.STOPPED):
            for target in PlatformState:
                self.assertFalse(can_transition(state, target))


if __name__ == "__main__":
    unittest.main()
