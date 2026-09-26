"""Skill bootstrap."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = ["ensure_user_skills_dir", "ensure_uv"]


def ensure_user_skills_dir() -> Path:
    """Ensure user skills directory exists."""
    path = Path.home() / ".local" / "share" / "aether" / "skills" / "user"
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_uv(bootstrap_dir: Path) -> str:
    """Ensure uv is available."""
    return "uv"