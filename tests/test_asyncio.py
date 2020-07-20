import asyncio
import unittest

import ori.asyncio


async def some_async_function(value):
    return value


class TestAsyncio(unittest.TestCase):
    def test__sync(self):
        assert ori.asyncio.sync(some_async_function(3)) == 3
