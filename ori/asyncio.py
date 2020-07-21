"""Utility code for working with Python's asyncio."""
import asyncio
import typing


def sync(
    awaitable: typing.Awaitable,
    event_loop: typing.Optional[asyncio.events.AbstractEventLoop] = None,
):
    """
    Run an awaitable synchronously. Good for calling asyncio code from sync Python.

    The usage is as follows:

    .. highlight:: python
    .. code-block:: python

        from ori.asyncio import sync

        async def your_function(arg1, arg2):
            # Additional asyncio code can go here
            return arg1 + arg2

        # If you call your_function() directly, you will get a coroutine
        # object. You need to either use the await keyword...
        # or the sync() wrapper as below.

        value = sync(your_function(1, 2))
        assert value == 3

    Args:
        awaitable: This is a function declared with `async def` or another type
            of awaitable object in Python.
        event_loop: An :mod:`asyncio` event loop. This defaults to `None`, in which
            case this function will try to pull the running event loop.
            If no event loop exists, this function will try to create one.

    Returns:
        This returns the same value that `awaitable` would if you
        used the `await` keyword instead of :func:`sync`.

    Raises:
        TypeError: If `awaitable` is not actually an awaitable object,
            then we raise a TypeError.
    """
    if not event_loop:
        event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(awaitable)
