"""Skill creator service."""

from __future__ import annotations

from typing import Any

__all__ = ["SkillCreatorInput", "SkillCreatorService", "build_authoring_context"]


class SkillCreatorInput:
    """Input for skill creation."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class SkillCreatorService:
    """Service for creating skills."""

    def create_skill(self, input: SkillCreatorInput) -> Any:
        """Create a skill from input."""
        pass


def build_authoring_context() -> dict[str, Any]:
    """Build authoring context."""
    return {}