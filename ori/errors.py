"""All exceptions for the Ori module."""


class OriError(Exception):
    """The base class efor all Ori errors."""


class OriValidationError(OriError):
    """Raise when Ori receives bad input from the user."""
