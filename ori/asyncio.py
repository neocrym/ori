"""Utility code for working with Python's asyncio."""
import asyncio
import typing


def sync(
    awaitable: typing.Awaitable,
    event_loop: typing.Optional[asyncio.events.AbstractEventLoop] = None,
):
    """Run an awaitable synchronously. Good for calling asyncio code from sync Python."""
    if not event_loop:
        event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(awaitable)
