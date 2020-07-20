import unittest

import ori.concurrency


def demo_func(value):
    return value


BACKGROUND_FUNCTIONS = {
    "run_in_background_thread": ori.concurrency.run_in_background_thread,
    "run_in_background_process": ori.concurrency.run_in_background_process,
}


class TestConcurrency(unittest.TestCase):
    def test_run_in_background(self):
        for func_name in BACKGROUND_FUNCTIONS:
            background_func = BACKGROUND_FUNCTIONS[func_name]
            with self.subTest(func_name=func_name):
                backgroundable = background_func(demo_func)
                assert backgroundable.executor
                future_3 = backgroundable(3)
                future_5 = backgroundable(5)
                assert 5 == future_5.result()
                assert 3 == future_3.result()
