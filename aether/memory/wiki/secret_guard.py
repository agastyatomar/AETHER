"""Secret guard for wiki."""

from __future__ import annotations

__all__ = ["contains_secret"]


def contains_secret(text: str) -> bool:
    """Check if text contains secrets."""
    secret_patterns = ["api_key", "password", "secret", "token"]
    return any(p in text.lower() for p in secret_patterns)