"""
Loop Governance: Halting Problems & Oscillation Damping (Chapter 12)
Prevents runaway model iterations and detects cyclical repetition traps.
"""

from __future__ import annotations

import hashlib
from pydantic import BaseModel


class GovernorStatus(BaseModel):
    can_continue: bool
    reason: str = "OK"


class LoopGovernor:
    """
    Guards autonomous reasoning loops from infinite repetition, cost runaway,
    and cyclical tool invocations.
    """

    def __init__(self, max_steps: int = 10, oscillation_window: int = 3):
        self.max_steps = max_steps
        self.oscillation_window = oscillation_window
        self.step_count = 0
        self.history_hashes: list[str] = []

    def record_and_verify(self, action_payload: str) -> GovernorStatus:
        self.step_count += 1
        if self.step_count > self.max_steps:
            return GovernorStatus(can_continue=False, reason=f"Max iteration step limit reached ({self.max_steps})")

        h = hashlib.sha256(action_payload.encode()).hexdigest()
        window = self.history_hashes[-self.oscillation_window:]
        if window.count(h) >= 2:
            return GovernorStatus(can_continue=False, reason="Oscillation loop detected: identical actions repeated")

        self.history_hashes.append(h)
        return GovernorStatus(can_continue=True, reason="OK")
