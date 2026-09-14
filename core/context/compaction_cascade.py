"""
Context Pager & Cascade Engine (Chapter 6 Reference Blueprint)
Hierarchical token compression preventing attention degradation and context overflow.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str
    tokens: int


class CompactionCascadeEngine:
    """
    Dynamically compacts long conversational histories into progressive hierarchical summaries
    while preserving the immediate high-resolution working memory window.
    """

    def __init__(self, max_token_budget: int = 8192, working_window_size: int = 5):
        self.max_token_budget = max_token_budget
        self.working_window_size = working_window_size
        self.archived_summary: str = ""

    def compact(self, messages: list[Message]) -> list[Message]:
        total_tokens = sum(m.tokens for m in messages)
        if total_tokens <= self.max_token_budget or len(messages) <= self.working_window_size:
            return messages

        # Preserve recent working window messages in high fidelity
        working_window = messages[-self.working_window_size:]
        messages_to_compact = messages[:-self.working_window_size]

        # Deterministic recursive synthesis
        summary_bullets = [
            f"- [{m.role.upper()}]: {m.content[:80]}..."
            for m in messages_to_compact
        ]
        compacted_block = "\n".join(summary_bullets)
        if self.archived_summary:
            self.archived_summary += "\n" + compacted_block
        else:
            self.archived_summary = compacted_block

        summary_msg = Message(
            role="system",
            content=f"<archived_context_summary>\n{self.archived_summary}\n</archived_context_summary>",
            tokens=len(self.archived_summary.split()),
        )

        return [summary_msg] + working_window
