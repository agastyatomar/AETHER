"""Skill runner."""

from __future__ import annotations

from typing import Any

__all__ = ["SkillRunner"]


class SkillRunner:
    """Runner for skills."""

    def __init__(self, registry: Any):
        self.registry = registry

    async def run(self, skill_name: str, action: str, params: dict) -> Any:
        """Run skill action."""
        skill = self.registry.get_skill(skill_name)
        if skill and hasattr(skill, action):
            method = getattr(skill, action)
            return await method(params)
        return None