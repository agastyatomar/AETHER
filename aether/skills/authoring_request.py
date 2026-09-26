"""Skill authoring request detection."""

from __future__ import annotations

__all__ = ["is_skill_authoring_request"]


def is_skill_authoring_request(text: str) -> bool:
    """Detect if text is a skill authoring request."""
    return "create skill" in text.lower() or "author skill" in text.lower()