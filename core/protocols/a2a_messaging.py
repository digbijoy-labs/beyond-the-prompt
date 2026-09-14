"""
Agent-to-Agent (A2A) Messaging & Protocol Framing (Chapter 17)
Standardized inter-agent communication envelope with capability negotiation.
"""

from __future__ import annotations

import uuid
import time
from typing import Any
from pydantic import BaseModel, Field


class A2AMessageEnvelope(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_agent: str
    recipient_agent: str
    conversation_id: str
    intent: str
    payload: dict[str, Any]
    trace_id: str = ""
    timestamp: float = Field(default_factory=time.time)


class A2ARouter:
    """
    Dispatches typed envelopes between autonomous subagents while enforcing context isolation.
    """

    def __init__(self):
        self.inboxes: dict[str, list[A2AMessageEnvelope]] = {}

    def send(self, envelope: A2AMessageEnvelope) -> None:
        if envelope.recipient_agent not in self.inboxes:
            self.inboxes[envelope.recipient_agent] = []
        self.inboxes[envelope.recipient_agent].append(envelope)

    def receive(self, agent_name: str) -> list[A2AMessageEnvelope]:
        messages = self.inboxes.get(agent_name, [])
        self.inboxes[agent_name] = []
        return messages
