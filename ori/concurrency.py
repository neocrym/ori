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
    Runs the function in a background thread or process, depending on the
    executor that you provided.

    Most users will want to use :meth:`ori.concurrency.run_in_background_thread` or
    :meth:`ori.concurrency.run_in_background_process` instead.

    Args:
        func: The function to run in the background.
        executor_class: A `concurrent.futures.Executor` subclass that the
            function will be submitted to. Two popular choices are
            :class:`concurrent.futures.ThreadPoolExecutor` or
            :class:`concurrent.futures.ProcessPoolExecutor`, but you can pass
            your own subclass if if it follows the same API.
        max_workers: Specify this to set the maximum number of parallel
            threads or processes to run at once. If this is set to
            None, then the executor's default maximum number of workers
            are used.

    Returns:
        This function returns a wrapper of the `func` function that you passed.
        The wrapper takes the exact same arguments, but instead returns
        a :class:`concurrent.futures.Future` object. To wait for the return
        value of `func`, call `.result()` on the future that this function
        returns.

    Raises:
        OriValidationError: When you provide a value for `func` that is not
            a callable function.

    """
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
    Runs the function in a background thread.

    Args:
        func: The function to run in the background.
        max_workers: Specify this to set the maximum number of parallel
            threads or processes to run at once. If this is set to
            None, then the executor's default maximum number of workers
            are used.

    Returns:
        This function returns a wrapper of the `func` function that you passed.
        The wrapper takes the exact same arguments, but instead returns
        a :class:`concurrent.futures.Future` object. To wait for the return
        value of `func`, call `.result()` on the future that this function
        returns.

    Raises:
        OriValidationError: When you provide a value for `func` that is not
            a callable function.

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
    Runs the function in a background process.

    Args:
        func: The function to run in the background.
        max_workers: Specify this to set the maximum number of parallel
            threads or processes to run at once. If this is set to
            None, then the executor's default maximum number of workers
            are used.

    Returns:
        This function returns a wrapper of the `func` function that you passed.
        The wrapper takes the exact same arguments, but instead returns
        a :class:`concurrent.futures.Future` object. To wait for the return
        value of `func`, call `.result()` on the future that this function
        returns.

    Raises:
        OriValidationError: When you provide a value for `func` that is not
            a callable function.
    """
    return run_in_background(
        func=func,
        executor_class=concurrent.futures.ProcessPoolExecutor,
        max_workers=max_workers,
    )
