"""Core process utilities."""

from __future__ import annotations

import os
import sys

__all__ = ["NO_WINDOW_CREATIONFLAGS"]

# Windows-specific flag to prevent console window creation
if os.name == "nt":
    try:
        # CREATE_NO_WINDOW = 0x08000000
        NO_WINDOW_CREATIONFLAGS: int = 0x08000000
    except AttributeError:
        NO_WINDOW_CREATIONFLAGS = 0
else:
    NO_WINDOW_CREATIONFLAGS = 0