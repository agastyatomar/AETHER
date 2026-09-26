"""Agent chat service."""

from __future__ import annotations

__all__ = ["SessionBusy", "resolve_runner"]


class SessionBusy(Exception):
    """Raised when session is busy."""
    pass


def resolve_runner(provider: str) -> str:
    """Resolve runner for provider."""
    return provider