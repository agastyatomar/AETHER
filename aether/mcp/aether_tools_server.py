"""Aether tools server."""

from __future__ import annotations

import contextvars

__all__ = ["CHAT_SESSION_REF"]


CHAT_SESSION_REF: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "aether_chat_session_ref", default=None
)