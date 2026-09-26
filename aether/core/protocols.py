"""Core communication protocols."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "ToolResult",
    "BrainMessage",
    "BrainRequest",
    "ImageBlock",
    "CodingSessionGateway",
    "Tool",
    "MarsStationExecutor",
]


@dataclass
class ToolResult:
    """Result of a tool execution."""
    ok: bool
    data: dict[str, Any] | None = None
    error: str | None = None
    trace_id: str = ""
    latency_ms: int = 0


@dataclass
class BrainMessage:
    """Message for brain communication."""
    role: str  # user, assistant, system, tool
    content: str
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None
    name: str | None = None


@dataclass
class BrainRequest:
    """Request to brain."""
    messages: list[BrainMessage]
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int | None = None
    tools: list[dict] | None = None
    tool_choice: str | dict | None = None


@dataclass
class ImageBlock:
    """Image block for multimodal messages."""
    type: str = "image"
    source: dict | None = None
    data: bytes | None = None
    mime_type: str = "image/png"


@dataclass
class CodingSessionGateway:
    """Gateway for coding sessions."""
    session_id: str
    workspace: str
    capabilities: list[str] = field(default_factory=list)


@dataclass
class Tool:
    """Tool definition."""
    name: str
    description: str
    parameters: dict[str, Any]
    required: list[str] = field(default_factory=list)


@dataclass
class MarsStationExecutor:
    """Executor for Mars station operations."""
    station_id: str
    capabilities: list[str] = field(default_factory=list)