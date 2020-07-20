"""Module for the poolchain."""

import concurrent.futures
import typing

from ori.errors import OriValidationError


class ChainElement(typing.NamedTuple):
    """A single element in our PoolChain."""

    function: typing.Callable
    executor_class: type
    max_workers: typing.Optional[int]
    timeout: typing.Optional[int]
    chunksize: int


class PoolChain:
    """Creates a poolchain."""

    def __init__(self):
        """Create a new poolchain."""
        self.chain: typing.Iterable[ChainElement] = []

    def add(
        self,
        function: typing.Callable,
        *,
        executor_class: type = concurrent.futures.ThreadPoolExecutor,
        max_workers: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        chunksize: int = 1,
    ):
        """Add a new element to the poolchain."""
        if not isinstance(executor_class, type):
            raise OriValidationError(
                "For the `executor_class` argument, you should pass a Python "
                "class. Did you pass a Python instance instead?"
            )
        if not getattr(executor_class, "map", False):
            raise OriValidationError(
                "Your `executor_class` needs to implement the `.map` "
                "method. It looks like it does not."
            )
        if (
            function.__name__ == "<lambda>"
            and executor_class == concurrent.futures.ProcessPoolExecutor
        ):
            raise OriValidationError(
                "You cannot use lambda functions with ProcessPoolExecutor. "
                "Define a named function with the `def` keyword instead."
            )
        if max_workers is not None:
            if not isinstance(max_workers, int):
                raise OriValidationError(
                    "The `max_workers` argument should be an int or None."
                )
            if max_workers < 1:
                raise OriValidationError(
                    "You need to define one or more worker. "
                    f"You defined {max_workers} workers."
                )
        if timeout is not None:
            if not isinstance(timeout, int):
                raise OriValidationError("Timeout should be None or an integer.")
            if timeout < 1:
                raise OriValidationError(
                    "Timeout should be None or an integer greater than 0."
                )
        self.chain.append(
            ChainElement(
                function=function,
                executor_class=executor_class,
                max_workers=max_workers,
                timeout=timeout,
                chunksize=chunksize,
            )
        )
        return self

    def add_threadpool(
        self,
        function: typing.Callable,
        *,
        max_workers: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        chunksize: int = 1,
    ):
        """Add a function to run with threadpool to the poolchain."""
        return self.add(
            function=function,
            executor_class=concurrent.futures.ThreadPoolExecutor,
            max_workers=max_workers,
            timeout=timeout,
            chunksize=chunksize,
        )

    def add_processpool(
        self,
        function: typing.Callable,
        *,
        max_workers: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        chunksize: int = 1,
    ):
        """Add a function to run with a "process pool" to the poolchain."""
        return self.add(
            function=function,
            executor_class=concurrent.futures.ProcessPoolExecutor,
            max_workers=max_workers,
            timeout=timeout,
            chunksize=chunksize,
        )

    def execute_lazy(self, iterable: typing.Iterable[typing.Any]):
        """Process the given iterable through the poolchain.

        Returns a generator.
        """
        if len(self.chain) < 1:
            raise OriValidationError("Try adding some workers first.")

        current_iterable = iterable
        executors = []
        for element in self.chain:
            current_executor = element.executor_class(max_workers=element.max_workers,)
            executors.append(current_executor)
            current_iterable = current_executor.map(
                element.function,
                current_iterable,
                timeout=element.timeout,
                chunksize=element.chunksize,
            )
        for item in current_iterable:
            yield item
        for executor in executors:
            executor.shutdown(wait=True)

    def execute_eager(self, iterable: typing.Iterable[typing.Any]):
        """Preocess the given iterable through the poolchain, eagerly returning a list."""
        return list(self.execute_lazy(iterable))

    def execute_lazy_single_threaded(self, iterable: typing.Iterable[typing.Any]):
        """Execute the chain in the current thread, returning a generator."""
        for item in iterable:
            current_val = item
            for element in self.chain:
                current_val = element.function(current_val)
            yield current_val

    def execute_eager_single_threaded(self, iterable: typing.Iterable[typing.Any]):
        """Execute the chain in the current thread, returning a Python list."""
        return list(self.execute_lazy_single_threaded(iterable))
