"""Tasks schema."""

from __future__ import annotations

__all__ = ["validate_event_schedule"]


def validate_event_schedule(schedule: dict) -> bool:
    """Validate event schedule."""
    return True