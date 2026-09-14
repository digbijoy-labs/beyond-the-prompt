"""
Deterministic Prefix Context Compiler & Cache Governor (Chapter 5)
Enforces static prompt prefix invariants to achieve 90%+ KV-cache hit rates.
"""

from __future__ import annotations

import hashlib
from pydantic import BaseModel, Field


class CacheSegment(BaseModel):
    name: str
    content: str
    is_static: bool
    token_estimate: int
    content_hash: str = ""

    def compute_hash(self) -> str:
        self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()[:16]
        return self.content_hash


class PrefixContextCompiler:
    """
    Assembles prompt context windows with invariant static prefix anchors.
    Ensures that volatile user tokens or dynamic tool observations never invalidate
    upstream system prompt and schema KV-caches.
    """

    def __init__(self, system_constitution: str):
        self.system_constitution = CacheSegment(
            name="system_constitution",
            content=system_constitution,
            is_static=True,
            token_estimate=len(system_constitution.split()),
        )
        self.system_constitution.compute_hash()
        self.static_tools: list[CacheSegment] = []

    def register_tool_schema(self, tool_name: str, schema_json: str) -> None:
        seg = CacheSegment(
            name=f"tool_{tool_name}",
            content=schema_json,
            is_static=True,
            token_estimate=len(schema_json.split()),
        )
        seg.compute_hash()
        self.static_tools.append(seg)

    def compile(self, dynamic_history: list[str], current_turn: str) -> str:
        # Static Invariant Tier (Prefix Cache Anchor)
        prefix_blocks = [self.system_constitution.content]
        for tool in sorted(self.static_tools, key=lambda x: x.name):
            prefix_blocks.append(f"<tool_schema name='{tool.name}'>\n{tool.content}\n</tool_schema>")

        # Dynamic Volatile Tier
        dynamic_blocks = ["<conversation_history>"]
        for msg in dynamic_history:
            dynamic_blocks.append(f"  {msg}")
        dynamic_blocks.append("</conversation_history>")
        dynamic_blocks.append(f"<current_turn>\n{current_turn}\n</current_turn>")

        return "\n\n".join(prefix_blocks + dynamic_blocks)
