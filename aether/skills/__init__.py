"""Skills package."""

from __future__ import annotations

__all__ = ["Skill", "SkillContext", "skill_action"]


class SkillContext:
    """Context for skill execution."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Skill:
    """Base skill class."""
    def __init__(self, config: dict):
        self.config = config


def skill_action(func):
    """Decorator for skill actions."""
    return func