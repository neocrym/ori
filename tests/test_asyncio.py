"""Unit test module for :mod:`ori.asyncio`."""
import unittest

import ori.asyncio


async def some_async_function(value):
    """A demo async function. Does not do any actual I/O."""
    return value


class TestAsyncio(unittest.TestCase):
    """Unit tests for ori.asyncio."""

    def test__sync(self):
        """Test that the basicss of sync() work."""
        assert ori.asyncio.sync(some_async_function(3)) == 3
