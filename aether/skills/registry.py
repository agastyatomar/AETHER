"""Skill registry."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = ["SkillRegistry"]


class SkillRegistry:
    """Registry for skills."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self._skills: dict[str, Any] = {}

    def load_all(self) -> None:
        """Load all skills from directory."""
        pass

    def get_skill(self, name: str) -> Any:
        """Get skill by name."""
        return self._skills.get(name)

    def register_skill(self, name: str, skill: Any) -> None:
        """Register a skill."""
        self._skills[name] = skill