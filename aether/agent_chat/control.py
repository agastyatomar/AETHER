"""Agent chat control."""

from __future__ import annotations

__all__ = ["supports_restricted_turn"]


def supports_restricted_turn(provider: str) -> bool:
    """Check if provider supports restricted turn."""
    return True