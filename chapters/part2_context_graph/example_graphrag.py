"""
Part 2 Demonstration: GraphRAG & Relational Subgraph Traversal
"""

from core.graph.graph_rag_engine import GraphRAGEngine, EntityNode, RelationEdge


def main():
    print("=== Beyond the Prompt: Part 2 GraphRAG Demonstration ===")
    engine = GraphRAGEngine()

    # Build ontological knowledge graph
    engine.add_entity(EntityNode(entity_id="CognitiveRuntime", entity_type="System"))
    engine.add_entity(EntityNode(entity_id="AIHarness", entity_type="ControlPlane"))
    engine.add_entity(EntityNode(entity_id="MicroVM", entity_type="ExecutionPlane"))
    engine.add_entity(EntityNode(entity_id="PrefixCache", entity_type="ContextPlane"))

    engine.add_relation(RelationEdge(source="CognitiveRuntime", target="AIHarness", relation="ENFORCES_BOUNDARY"))
    engine.add_relation(RelationEdge(source="AIHarness", target="MicroVM", relation="SPAWNS_CONTAINER"))
    engine.add_relation(RelationEdge(source="AIHarness", target="PrefixCache", relation="COMPACTS_TOKENS"))

    print("\nTraversing multi-hop relationships from 'CognitiveRuntime':")
    subgraph = engine.traverse_subgraph("CognitiveRuntime", max_hops=2)
    for line in subgraph:
        print(" ", line)

    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    main()
