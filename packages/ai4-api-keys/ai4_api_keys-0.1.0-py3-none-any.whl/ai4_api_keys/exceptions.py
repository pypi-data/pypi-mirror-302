"""Exceptions for the ai4_api_keys package."""

import enum


class BaseError(Exception):
    """Base class for all exceptions."""

    pass


class InvalidKeyError(BaseError):
    """Raised when an invalid key is provided."""

    def __init__(self, key: str):
        """Initialize the exception."""
        self.key = key
        super().__init__(f"Invalid key: {key}")


class InvalidScopeError(BaseError):
    """Raised when an invalid scope is provided."""

    def __init__(self, scope: str, requested_scope: str):
        """Initialize the exception."""
        self.scope = scope
        super().__init__(f"Invalid scope: {scope}, requested: {requested_scope}")


class InvalidLevelError(BaseError):
    """Raised when an invalid access level is provided."""

    # MyPy complains about this line, but it's correct with
    # "InvalidLevelError" has incompatible type "type[APILevels]"; expected "Enum"
    def __init__(self, level: str, valid_levels: enum.Enum):  # type: ignore
        """Initialize the exception."""
        self.level = level
        super().__init__(f"Invalid level: {level}, valid levels: {valid_levels}")
