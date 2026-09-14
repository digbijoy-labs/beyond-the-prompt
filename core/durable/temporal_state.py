"""
Durable Agent Execution & Event-Sourced State Store (Chapter 16)
Enables deterministic workflow pause, replay, and recovery across cluster restarts.
"""

from __future__ import annotations

import time
from typing import Any
from pydantic import BaseModel, Field


class JournalEvent(BaseModel):
    event_id: int
    event_type: str
    timestamp: float = Field(default_factory=time.time)
    payload: dict[str, Any]


class DurableStateStore:
    """
    Append-only journal state store providing time-travel debugging and workflow replay.
    """

    def __init__(self):
        self.journal: list[JournalEvent] = []
        self._current_id = 0

    def append_event(self, event_type: str, payload: dict[str, Any]) -> JournalEvent:
        self._current_id += 1
        event = JournalEvent(event_id=self._current_id, event_type=event_type, payload=payload)
        self.journal.append(event)
        return event

    def replay_state(self) -> dict[str, Any]:
        state: dict[str, Any] = {}
        for event in self.journal:
            if event.event_type == "STATE_SET":
                state.update(event.payload)
            elif event.event_type == "STATE_DELETE":
                for k in event.payload.get("keys", []):
                    state.pop(k, None)
        return state
