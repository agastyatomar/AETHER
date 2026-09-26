"""Core path augmentation."""

from __future__ import annotations

import os
import sys
from pathlib import Path

__all__ = ["ensure_cli_paths", "default_doc_roots"]


def ensure_cli_paths() -> None:
    """Ensure CLI paths are in sys.path."""
    # Add user scripts directory
    user_scripts = Path.home() / ".local" / "share" / "aether" / "scripts"
    if user_scripts.exists() and str(user_scripts) not in sys.path:
        sys.path.insert(0, str(user_scripts))


def default_doc_roots() -> list[Path]:
    """Get default documentation roots."""
    roots = [
        Path.cwd() / "docs",
        Path.home() / ".local" / "share" / "aether" / "docs",
    ]
    return [r for r in roots if r.exists()]