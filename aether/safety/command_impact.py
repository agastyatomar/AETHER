"""Command impact classification."""

from __future__ import annotations

from enum import Enum

__all__ = ["DESTRUCTIVE", "classify_command"]


class CommandImpact(str, Enum):
    """Command impact levels."""
    SAFE = "safe"
    READ_ONLY = "read_only"
    WRITE = "write"
    DESTRUCTIVE = "destructive"


DESTRUCTIVE = CommandImpact.DESTRUCTIVE


def classify_command(command: str) -> CommandImpact:
    """Classify command impact."""
    destructive_patterns = ["rm ", "del ", "format", "mkfs", "dd ", "> /dev/"]
    if any(p in command.lower() for p in destructive_patterns):
        return CommandImpact.DESTRUCTIVE
    return CommandImpact.SAFE