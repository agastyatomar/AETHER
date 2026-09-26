"""Brain streaming."""

from __future__ import annotations

__all__ = ["aggregate"]


def aggregate(chunks: list) -> str:
    """Aggregate streaming chunks."""
    return "".join(str(c) for c in chunks)