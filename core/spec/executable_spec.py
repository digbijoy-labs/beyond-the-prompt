"""
Spec-Driven Agent Engineering & Executable Prompts (Chapter 20)
Treats system prompts as formal, machine-executable contracts with schema assertions.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class OperationalContract(BaseModel):
    role_name: str
    allowed_tools: list[str]
    invariants: list[str]
    denied_actions: list[str] = Field(default_factory=list)


class ExecutableSpecEngine:
    """
    Compiles formal operational contracts into prompt constitutions and runtime assertions.
    """

    def __init__(self, contract: OperationalContract):
        self.contract = contract

    def render_system_constitution(self) -> str:
        lines = [
            f"# Operational Role: {self.contract.role_name}",
            "## Invariant Constraints (Non-Negotiable):",
        ]
        for inv in self.contract.invariants:
            lines.append(f"- [INVARIANT] {inv}")
        lines.append("## Permitted Tool Contracts:")
        for tool in self.contract.allowed_tools:
            lines.append(f"- ALLOW: {tool}")
        if self.contract.denied_actions:
            lines.append("## Strictly Prohibited Actions:")
            for denied in self.contract.denied_actions:
                lines.append(f"- DENY: {denied}")
        return "\n".join(lines)

    def assert_action_permitted(self, action_name: str) -> bool:
        if action_name in self.contract.denied_actions:
            return False
        return action_name in self.contract.allowed_tools
