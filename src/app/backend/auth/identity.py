"""Identity and token sources for authentication."""

import abc
from typing import Any, Callable, Dict, Literal, Optional, Protocol

from pydantic import BaseModel, Field


class TokenSource(Protocol):
    """Protocol for token sources."""

    @abc.abstractmethod
    def bearer_token(self) -> str:
        """Retrieve the bearer token."""


class OboTokenSource(TokenSource):
    """Token source that retrieves token from headers."""

    def __init__(self, headers_getter: Callable[[], Dict[str, str]]):
        """Initialize with a callable that returns headers.

        Args:
            headers_getter: A callable that returns a dictionary of headers.
        """
        self._headers_getter = headers_getter

    def bearer_token(self) -> str:
        """Retrieve the bearer token from headers."""
        h = self._headers_getter() or {}
        return h['x-forwarded-access-token']


class PatTokenSource(TokenSource):
    """Token source that uses a static PAT."""

    def __init__(self, pat: str):
        """Initialize with a personal access token (PAT)."""
        self._pat = pat

    def bearer_token(self) -> str:
        """Return the PAT as the bearer token."""
        return self._pat


class Identity(BaseModel):
    """User identity and authentication details."""

    email: Optional[str] = None
    display_name: Optional[str] = None
    auth_type: Literal['obo', 'pat'] = 'pat'
    # The token source that provides the bearer token for authentication
    # Using Field(repr=False) to prevent the token from being exposed in string representations
    # Type Any is used since TokenSource is a Protocol and can't be used directly in Pydantic
    token_source: Any = Field(repr=False)
