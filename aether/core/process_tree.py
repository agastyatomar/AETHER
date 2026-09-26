"""Process tree management."""

from __future__ import annotations

import os
import signal
import sys
import threading
import weakref
from typing import Any

__all__ = ["ProcessTree", "make_process_tree"]


class ProcessTree:
    """Track child processes for cleanup."""

    def __init__(self, name: str):
        self.name = name
        self.pids: set[int] = set()
        self._lock = threading.Lock()
        self._closed = False

    def assign(self, pid: int) -> None:
        """Assign a PID to this tree."""
        with self._lock:
            if not self._closed:
                self.pids.add(pid)

    def close(self) -> None:
        """Close the tree and optionally kill processes."""
        with self._lock:
            self._closed = True
            self.pids.clear()

    def kill_all(self, sig: int = signal.SIGTERM) -> None:
        """Kill all tracked processes."""
        with self._lock:
            for pid in self.pids:
                try:
                    os.kill(pid, sig)
                except ProcessLookupError:
                    pass
            self.pids.clear()


_TREES: dict[str, ProcessTree] = {}
_TREES_LOCK = threading.Lock()


def make_process_tree(name: str) -> ProcessTree:
    """Create or get a process tree."""
    with _TREES_LOCK:
        if name not in _TREES:
            _TREES[name] = ProcessTree(name)
        return _TREES[name]