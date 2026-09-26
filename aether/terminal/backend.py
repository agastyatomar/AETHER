"""Terminal backend."""

from __future__ import annotations

__all__ = ["make_pty_backend"]


def make_pty_backend() -> str:
    """Make PTY backend."""
    return "pty"