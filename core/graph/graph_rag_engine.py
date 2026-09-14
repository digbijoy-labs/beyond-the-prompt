"""
Knowledge Graph & GraphRAG Retrieval Engine (Chapter 7)
Traverses relational entities across multi-hop reasoning topologies.
"""

from __future__ import annotations

from collections import defaultdict
from pydantic import BaseModel, Field


class EntityNode(BaseModel):
    entity_id: str
    entity_type: str
    attributes: dict[str, str] = Field(default_factory=dict)


class RelationEdge(BaseModel):
    source: str
    target: str
    relation: str
    weight: float = 1.0


class GraphRAGEngine:
    """
    In-memory directed knowledge graph substrate for resolving multi-hop
    entity connections that traditional vector embeddings miss.
    """

    def __init__(self):
        self.nodes: dict[str, EntityNode] = {}
        self.adj: dict[str, list[RelationEdge]] = defaultdict(list)

    def add_entity(self, node: EntityNode) -> None:
        self.nodes[node.entity_id] = node

    def add_relation(self, edge: RelationEdge) -> None:
        self.adj[edge.source].append(edge)

    def traverse_subgraph(self, root_entity: str, max_hops: int = 2) -> list[str]:
        if root_entity not in self.nodes:
            return []

        visited = set()
        queue = [(root_entity, 0)]
        results = []

        while queue:
            curr, depth = queue.pop(0)
            if curr in visited or depth > max_hops:
                continue
            visited.add(curr)
            results.append(f"Entity: {curr} ({self.nodes[curr].entity_type})")

            for edge in self.adj[curr]:
                results.append(f"  --[{edge.relation}]--> {edge.target}")
                if edge.target not in visited and depth + 1 <= max_hops:
                    queue.append((edge.target, depth + 1))

        return results
