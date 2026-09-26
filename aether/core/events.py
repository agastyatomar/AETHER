"""Core event system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

__all__ = ["Event", "EventBus", "LatencyPhase", "LatencySpan", "LatencyTurnComplete", "AgenticIdePaneActivity", "SocietyCheckpointChanged", "SocietyQuestChanged", "SocietyMessageSent", "SocietyRoomChanged", "AnnouncementRequested"]


@dataclass
class Event:
    """Base event class."""
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class EventBus:
    """Simple event bus for pub/sub."""

    _instance: EventBus | None = None
    _subscribers: dict[str, list[callable]] = {}

    def __new__(cls) -> EventBus:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get(cls) -> EventBus:
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def publish(self, event: Event) -> None:
        """Publish event to subscribers."""
        for callback in self._subscribers.get(event.kind, []):
            try:
                callback(event)
            except Exception:
                pass  # Silently ignore callback errors

    def subscribe(self, kind: str, callback: callable) -> None:
        """Subscribe to event kind."""
        if kind not in self._subscribers:
            self._subscribers[kind] = []
        self._subscribers[kind].append(callback)


class LatencyPhase:
    """Latency tracking phases."""
    QUEUE = "queue"
    EXEC = "exec"
    NETWORK = "network"
    MODEL = "model"
    BROWSER = "browser"


class LatencySpan:
    """Latency span for tracking operation timing."""

    def __init__(self, operation: str, phase: str):
        self.operation = operation
        self.phase = phase
        self.start_time: float = 0
        self.end_time: float = 0

    def __enter__(self):
        import time
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args):
        import time
        self.end_time = time.perf_counter()

    @property
    def latency_ms(self) -> int:
        return int((self.end_time - self.start_time) * 1000)


class LatencyTurnComplete(Event):
    """Event for completed turn latency."""
    def __init__(self, trace_id: str, total_ms: int, phases: dict[str, int]):
        super().__init__(
            kind="latency_turn_complete",
            payload={"trace_id": trace_id, "total_ms": total_ms, "phases": phases},
            trace_id=trace_id,
        )


class AgenticIdePaneActivity(Event):
    """Event for IDE pane activity."""
    def __init__(self, trace_id: str, pane: str, action: str):
        super().__init__(
            kind="agentic_ide_pane_activity",
            payload={"trace_id": trace_id, "pane": pane, "action": action},
            trace_id=trace_id,
        )


class SocietyCheckpointChanged(Event):
    """Event for society checkpoint changes."""
    def __init__(self, trace_id: str, agent_id: str, checkpoint: str):
        super().__init__(
            kind="society_checkpoint_changed",
            payload={"trace_id": trace_id, "agent_id": agent_id, "checkpoint": checkpoint},
            trace_id=trace_id,
        )


class SocietyQuestChanged(Event):
    """Event for society quest changes."""
    def __init__(self, trace_id: str, quest_id: str, status: str):
        super().__init__(
            kind="society_quest_changed",
            payload={"trace_id": trace_id, "quest_id": quest_id, "status": status},
            trace_id=trace_id,
        )


class SocietyMessageSent(Event):
    """Event for society messages."""
    def __init__(self, trace_id: str, from_agent: str, to_agent: str, msg_type: str):
        super().__init__(
            kind="society_message_sent",
            payload={"trace_id": trace_id, "from_agent": from_agent, "to_agent": to_agent, "msg_type": msg_type},
            trace_id=trace_id,
        )


class SocietyRoomChanged(Event):
    """Event for society room changes."""
    def __init__(self, trace_id: str, room_id: str, action: str):
        super().__init__(
            kind="society_room_changed",
            payload={"trace_id": trace_id, "room_id": room_id, "action": action},
            trace_id=trace_id,
        )


class AnnouncementRequested(Event):
    """Event for announcement requests."""
    def __init__(self, trace_id: str, message: str, level: str = "info"):
        super().__init__(
            kind="announcement_requested",
            payload={"trace_id": trace_id, "message": message, "level": level},
            trace_id=trace_id,
        )