"""Agentic IDE session."""

from __future__ import annotations

__all__ = ["get_registry", "running_call_signs"]


def get_registry() -> dict:
    """Get registry."""
    return {}


running_call_signs: dict = {}