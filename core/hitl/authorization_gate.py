"""
Human-in-the-Loop (HITL) & Policy Authorization Gate (Chapter 19)
Two-phase commit policy enforcement for destructive or high-impact operations.
"""

from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ActionIntent(BaseModel):
    action_id: str
    action_type: str
    target_resource: str
    blast_radius: str = Field(..., description="LOW, MEDIUM, HIGH, CRITICAL")
    parameters: dict = Field(default_factory=dict)


class AuthorizationGate:
    """
    Guards irreversible real-world side-effects behind asynchronous human approval gates.
    """

    def __init__(self, critical_thresholds: set[str] | None = None):
        self.critical_thresholds = critical_thresholds or {"HIGH", "CRITICAL"}
        self.pending_approvals: dict[str, ActionIntent] = {}

    def requires_approval(self, intent: ActionIntent) -> bool:
        return intent.blast_radius in self.critical_thresholds

    def submit_for_review(self, intent: ActionIntent) -> ApprovalStatus:
        if not self.requires_approval(intent):
            return ApprovalStatus.APPROVED
        self.pending_approvals[intent.action_id] = intent
        return ApprovalStatus.PENDING

    def resolve(self, action_id: str, approved: bool) -> ApprovalStatus:
        if action_id not in self.pending_approvals:
            raise KeyError(f"No pending approval found for action {action_id}")
        self.pending_approvals.pop(action_id)
        return ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
