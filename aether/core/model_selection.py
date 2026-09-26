"""Model selection utilities."""

from __future__ import annotations

__all__ = ["worker_selection"]


def worker_selection(task_type: str, available_models: list[str]) -> str:
    """Select appropriate model for task."""
    if available_models:
        return available_models[0]
    return "default"