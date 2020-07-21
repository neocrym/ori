"""
Module for the poolchain.

The "poolchain" is a high-level abstraction over the Python
:mod:`concurrent.futures` concurrency  module. A poolchain used
to run a single iterable (e.g. a list) through a chain of functions 
and collect an iterable of results at the end.

For example, here is one way to use a poolchain.

.. highlight:: python
.. code-block:: python

    from ori.poolchain import PoolChain

    results = (
        PoolChain()
        .add_threadpool(lambda num: num * 10)
        .add_threadpool(lambda num: str(num))
        .add_threadpool(lambda s: s + " is a number")
    ).execute_lazy([1, 2, 3, 4, 5])

    for row in results:
        print(row)
    # `results` is an iterator, so we go through it with a for loop.
    # we could have run `.execute_eager()` to automatically
    # turn the iterator into a list.


The general workflow is to create a :mod:`PoolChain` object and
then make a series of chained calls that add functions to execute
over every item in the iterable in sequence.

After the chain of functions has been specified, call one of the
`.execute_*()` functions like :func:`PoolChain.execute_lazy`
to get an iterator of the final return value or
:func:`PoolChain.execute_eager` to get an entire list upfront.


"""

import concurrent.futures
import typing

from ori.errors import OriValidationError


class _ChainElement(typing.NamedTuple):
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
        self.chain: typing.Iterable[_ChainElement] = []

    def add(
        self,
        function: typing.Callable,
        *,
        executor_class: type,
        max_workers: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        chunksize: int = 1,
    ):
        """
        Add a new element to the poolchain.

        Note that if your `executor_class` is a
        :class:`concurrent.futures.ProcessPoolExecutor`, you will not be
        able to pass `lambda` functions as `func`. You will need to use
        named functions defined with the `def` keyword.

        Args:
            function: This is the function that you want to run at the
                end of the current chain.
            executor_class: the :class:`concurrent.futures.Executor` subclass
                type to use to execute this part of the poolchain.
            max_workers: The maximum number of workers that the
                :class:`concurrent.futures.ProcessPoolExecutor` can start.
                If this is `None`, then then the executor will create
                the same number of workers as you have processors on
                your machine. This is usually a sensible default.
            timeout: The amount of time (in seconds) to wait for a
                :class:`concurrent.futures.Future` before throwing an error.
            chunksize: Sometimes the executor runs faster when providing chunks
                of the iterable to workers rather than just one iterable
                element at a time (the default). Try setting chunksize to
                a value greater than one to more efficiently use
                interprocess communication.

        Returns:
            The PoolChain object itself, allowing you to chain subsequent
            `add_*()` calls and at the end an `execute_*()` call.

        Raises:
            OriValidationError: Thrown if you don't send a real function, or
                a real Executor, a non-integer for one of the integer fields,
                etc.
        """
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
            _ChainElement(
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
    ):
        """Add a function to run with threadpool to the poolchain.

        Args:
            function: This is the function that you want to run at the
                end of the current chain.
            max_workers: The maximum number of workers that the
                :class:`concurrent.futures.ProcessPoolExecutor` can start.
                If this is `None`, then then the executor will create
                the same number of workers as you have processors on
                your machine. This is usually a sensible default.
            timeout: The amount of time (in seconds) to wait for a
                :class:`concurrent.futures.Future` before throwing an error.

        Returns:
            The PoolChain object itself, allowing you to chain subsequent
            `add_*()` calls and at the end an `execute_*()` call.

        Raises:
            OriValidationError: Thrown if you don't send a real function, or
                a real Executor, a non-integer for one of the integer fields,
                etc.
        """
        return self.add(
            function=function,
            executor_class=concurrent.futures.ThreadPoolExecutor,
            max_workers=max_workers,
            timeout=timeout,
        )

    def add_processpool(
        self,
        function: typing.Callable,
        *,
        max_workers: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        chunksize: int = 1,
    ):
        """
        Add a function to run with a "process pool" to the poolchain.
        
        You cannot pass a `lambda` function to a process pool. You need
        to make up your poolchain entirely with named functions defined with
        the `def` keyword.

        Args:
            function: This is the function that you want to run at the
                end of the current chain.
            max_workers: The maximum number of workers that the
                :class:`concurrent.futures.ProcessPoolExecutor` can start.
                If this is `None`, then then the executor will create
                the same number of workers as you have processors on
                your machine. This is usually a sensible default.
            timeout: The amount of time (in seconds) to wait for a
                :class:`concurrent.futures.Future` before throwing an error.
            chunksize: Sometimes the executor runs faster when providing chunks
                of the iterable to workers rather than just one iterable
                element at a time (the default). Try setting chunksize to
                a value greater than one to more efficiently use
                interprocess communication.

        Returns:
            The PoolChain object itself, allowing you to chain subsequent
            `add_*()` calls and at the end an `execute_*()` call.

        Raises:
            OriValidationError: Thrown if you don't send a real function, or
                a real Executor, a non-integer for one of the integer fields,
                etc.
        """
        return self.add(
            function=function,
            executor_class=concurrent.futures.ProcessPoolExecutor,
            max_workers=max_workers,
            timeout=timeout,
            chunksize=chunksize,
        )

    def execute_lazy(self, iterable: typing.Iterable[typing.Any]):
        """Process the given iterable through the poolchain.

        When you call this function, the poolchain begins executing
        immediately

        Returns:
            This function returns an iterator that lazily executes
            the poolchain.
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
        """
        Run the given iterable through the poolchain, eagerly returning a list.

        This method returns the results upfront in a list, which lets you
        look at the entire output without having to iterate through it yourself.

        Args:
            iterable: This is an iterable where every element in the
                iterable is processed through the chain.

        Returns:
            This function returns a complete Python list containing the return
            value of every element in the list.
        """
        return list(self.execute_lazy(iterable))

    def execute_lazy_single_threaded(self, iterable: typing.Iterable[typing.Any]):
        """
        Execute the chain in the current thread, returning a generator.

        This function is typically used when you want to test your chain without
        creating threads or processes. When running in one thread,
        :mod:`PoolChain` would never be faster than just running the functions
        yourself in sequence.

        This function returns a generator that you have to iterate through
        yourself for results.

        Args:
            iterable: This is an iterable where every element in the
                iterable is processed through the chain.

        Returns:
            This function returns an iterator that lazily executes
            the poolchain in the current thread. Every time the next
            output is fetched, the corresponding input is sent through
            every function in the chain.
        
        """
        for item in iterable:
            current_val = item
            for element in self.chain:
                current_val = element.function(current_val)
            yield current_val

    def execute_eager_single_threaded(self, iterable: typing.Iterable[typing.Any]):
        """
        Execute the chain in the current thread, returning a Python list.

        This method is typically used when you want to test your chain without
        creating threads or processes. When running in one thread,
        :mod:`PoolChain` would never be faster than just running the functions
        yourself in sequence.

        This method also returns the results upfront in a list, which lets you
        look at the entire output without having to iterate through it yourself.

        Args:
            iterable: This is an iterable where every element in the
                iterable is processed through the chain.

        Returns:
            This function returns a complete Python list containing the return
            value of every element in the list.
            
        """
        return list(self.execute_lazy_single_threaded(iterable))
