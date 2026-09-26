"""Agent chat catalog."""

from __future__ import annotations

__all__ = ["provider_row"]


def provider_row(provider: str) -> dict:
    """Get provider row."""
    return {"name": provider, "models": []}