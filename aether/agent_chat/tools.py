"""Agent chat tools."""

from __future__ import annotations

__all__ = ["shell_argv"]


def shell_argv(args: list[str]) -> list[str]:
    """Process shell argv."""
    return args