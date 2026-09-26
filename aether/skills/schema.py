"""Skill schema."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

__all__ = ["SkillManifest", "SkillFrontmatter"]


class SkillManifest(BaseModel):
    """Skill manifest model."""
    model_config = ConfigDict(extra="forbid")

    name: str
    version: str
    description: str
    author: str
    license: str = "MIT"
    tags: list[str] = Field(default_factory=list)
    capabilities: list[dict] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    entry_point: str


class SkillFrontmatter(BaseModel):
    """Skill frontmatter for markdown files."""
    model_config = ConfigDict(extra="allow")

    name: str
    version: str
    description: str
    author: str
    license: str = "MIT"
    tags: list[str] = Field(default_factory=list)