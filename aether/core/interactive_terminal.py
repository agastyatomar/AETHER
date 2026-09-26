"""Interactive terminal management."""

from __future__ import annotations

import os
import sys
from typing import Any

__all__ = ["InteractiveTerminal", "get_interactive_terminal"]


class InteractiveTerminal:
    """Manage interactive terminal sessions."""

    def __init__(self, name: str = "aether"):
        self.name = name
        self._active = False

    def start(self) -> None:
        """Start interactive session."""
        self._active = True

    def stop(self) -> None:
        """Stop interactive session."""
        self._active = False

    @property
    def is_active(self) -> bool:
        return self._active


_TERMINAL: InteractiveTerminal | None = None


def get_interactive_terminal(name: str = "aether") -> InteractiveTerminal:
    """Get or create interactive terminal."""
    global _TERMINAL
    if _TERMINAL is None:
        _TERMINAL = InteractiveTerminal(name)
    return _TERMINAL