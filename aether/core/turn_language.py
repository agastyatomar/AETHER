"""Turn language detection."""

from __future__ import annotations

__all__ = ["detect_language_request", "resolve_output_language"]


def detect_language_request(text: str) -> str | None:
    """Detect if user is requesting a specific language."""
    # Simple detection - could be enhanced
    return None


def resolve_output_language(requested: str | None, default: str = "en") -> str:
    """Resolve output language."""
    return requested or default