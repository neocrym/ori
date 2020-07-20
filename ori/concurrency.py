"""Utilities for concurrency of Python functions with multithreading or multiprocessing."""
import concurrent.futures
import functools
import typing

from ori.errors import OriValidationError


def run_in_background(
    func: typing.Callable,
    *,
    executor_class: type,
    max_workers: typing.Optional[int] = None,
):
    """
    Runs the function in a backgroud thread.

    Returns the worker but does not wait for it."""
    if not callable(func):
        raise OriValidationError(
            "You need to provide a callable function as the first " "argument."
        )
    executor = executor_class(max_workers=max_workers)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return executor.submit(func, *args, **kwargs)

    wrapper.executor = executor
    return wrapper


def run_in_background_thread(
    func: typing.Callable, *, max_workers: typing.Optional[int] = None,
):
    """
    Run the given function in a background thread.

    Returns a started `threading.Thread` worker.
    """
    return run_in_background(
        func=func,
        executor_class=concurrent.futures.ThreadPoolExecutor,
        max_workers=max_workers,
    )


def run_in_background_process(
    func: typing.Callable, *, max_workers: typing.Optional[int] = None,
):
    """
    Rusn the given function in a background process.

    Returns a started `multiprocessing.Process` worker.
    """
    return run_in_background(
        func=func,
        executor_class=concurrent.futures.ProcessPoolExecutor,
        max_workers=max_workers,
    )
