"""
Hybrid Retrieval & Hierarchical Memory Substrate (Chapter 8)
Unifies episodic working memory, structured semantic facts, and dense vector stores.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    key: str
    content: str
    tags: list[str] = Field(default_factory=list)
    importance_score: float = 1.0


class HybridMemorySubstrate:
    """
    Tiered memory architecture managing short-term scratchpads,
    intermediate episodic traces, and long-term invariant facts.
    """

    def __init__(self):
        self.short_term: dict[str, str] = {}
        self.episodic_store: list[MemoryRecord] = []
        self.semantic_store: dict[str, MemoryRecord] = {}

    def set_working_memory(self, key: str, value: str) -> None:
        self.short_term[key] = value

    def commit_episodic(self, record: MemoryRecord) -> None:
        self.episodic_store.append(record)

    def store_fact(self, record: MemoryRecord) -> None:
        self.semantic_store[record.key] = record

    def retrieve(self, query: str) -> list[str]:
        matches = []
        q_lower = query.lower()
        # 1. Check working memory
        for k, v in self.short_term.items():
            if q_lower in k.lower() or q_lower in v.lower():
                matches.append(f"[Working] {k}: {v}")

        # 2. Check semantic invariant facts
        for k, rec in self.semantic_store.items():
            if q_lower in rec.key.lower() or q_lower in rec.content.lower():
                matches.append(f"[Semantic] {rec.key}: {rec.content}")

        # 3. Check episodic log
        for rec in self.episodic_store[-10:]:
            if any(q_lower in tag.lower() for tag in rec.tags) or q_lower in rec.content.lower():
                matches.append(f"[Episodic] {rec.key}: {rec.content}")

        return matches
