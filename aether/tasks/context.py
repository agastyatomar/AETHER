"""Tasks context."""

from __future__ import annotations

__all__ = ["client_timezone"]


def client_timezone() -> str:
    """Get client timezone."""
    return "UTC"