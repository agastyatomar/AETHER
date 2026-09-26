"""CLI capability provider."""

from __future__ import annotations

__all__ = ["equivalent_grants"]


def equivalent_grants(provider: str) -> list[str]:
    """Get equivalent grants for provider."""
    return []