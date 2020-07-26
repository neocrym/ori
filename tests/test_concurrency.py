"""
Tests for the :mod:`ori.concurrency` module.
"""
import unittest

import ori.concurrency


def demo_func(value):
    """A test function to run in the background."""
    return value


BACKGROUND_FUNCTIONS = {
    "run_in_background_thread": ori.concurrency.run_in_background_thread,
    "run_in_background_process": ori.concurrency.run_in_background_process,
}


class TestConcurrency(unittest.TestCase):
    """Unit tests for ori.concurrency."""

    def test_run_in_background(self):
        """Test that we can make a function backgroundable."""
        for func_name in BACKGROUND_FUNCTIONS:
            background_func = BACKGROUND_FUNCTIONS[func_name]
            with self.subTest(func_name=func_name):
                backgroundable = background_func(demo_func)
                assert backgroundable.executor
                future_3 = backgroundable(3)
                future_5 = backgroundable(5)
                assert 5 == future_5.result()
                assert 3 == future_3.result()
