"""Skill loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = ["load_skill", "parse_skill_frontmatter"]


def parse_skill_frontmatter(path: Path) -> dict[str, Any]:
    """Parse skill frontmatter from markdown file."""
    import yaml
    content = path.read_text(encoding="utf-8")
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}
    return {}


def load_skill(path: Path) -> dict[str, Any]:
    """Load skill from directory."""
    frontmatter = parse_skill_frontmatter(path / "skill.yaml") if (path / "skill.yaml").exists() else {}
    return {"path": path, "frontmatter": frontmatter}