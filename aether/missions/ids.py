"""Mission ID generation."""

from __future__ import annotations

import time
import uuid

__all__ = ["uuid7_str"]


def uuid7_str() -> str:
    """Generate UUIDv7-like string (timestamp + random)."""
    # Simplified UUIDv7 - timestamp in ms + random
    ts = int(time.time() * 1000)
    random_part = uuid.uuid4().bytes[-10:]
    return f"{ts:012x}-{random_part.hex()}"