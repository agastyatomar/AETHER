"""Skill origin tracking."""

from __future__ import annotations

from enum import Enum
from typing import Any

__all__ = ["SkillOrigin", "write_origin"]


class SkillOrigin(str, Enum):
    """Origin of a skill."""
    BUILTIN = "builtin"
    USER = "user"
    MARKETPLACE = "marketplace"


def write_origin(skill_dir: Any, origin: SkillOrigin) -> None:
    """Write origin marker file."""
    pass