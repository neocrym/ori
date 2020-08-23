"""All exceptions for the Ori module."""


class OriError(Exception):
    """The base class efor all Ori errors."""


class OriValidationError(OriError):
    """Raise when Ori receives bad input from the user."""


class OriNoInteractiveProcessPools(OriError):
    """Raises when the user tries to use process pools in interactive mode.

    The :class:`concurrent.futures.ProcessPoolExecutor` does not work when
    the user is running in an interactive shell. Code must be saved to disk
    and importable in order to be used.
    """
