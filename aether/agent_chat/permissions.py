"""Agent chat permissions."""

from __future__ import annotations

__all__ = ["ladder_key", "normalize_permission"]


def ladder_key(permission: str) -> int:
    """Get permission ladder key."""
    return 0


def normalize_permission(permission: str) -> str:
    """Normalize permission string."""
    return permission