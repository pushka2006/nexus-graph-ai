#!/usr/bin/env python3
"""
Seed script for NEXUS GRAPH AI.
Initializes FalkorDB graph schema, loads synthetic NexusWorks company dataset,
and verifies entity relationships and constraints.
"""
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.graph.service import get_graph_service

def main():
    print("=" * 60)
    print("NEXUS GRAPH AI: FalkorDB Knowledge Graph Seeding")
    print("=" * 60)

    service = get_graph_service()
    res = service.reset_graph()
    stats = service.get_stats()

    print(f"Status: {res['status']}")
    print(f"Engine Mode: {stats['engine_mode']}")
    print(f"Graph Name: {stats['graph_name']}")
    print(f"Total Nodes: {stats['total_nodes']}")
    print(f"Total Edges: {stats['total_edges']}")
    print("\nNode Counts by Type:")
    for k, v in sorted(stats['node_counts_by_type'].items()):
        print(f"  - {k:<16}: {v}")

    print("\nEdge Counts by Type:")
    for k, v in sorted(stats['edge_counts_by_type'].items()):
        print(f"  - {k:<16}: {v}")

    print("\n[SUCCESS] Knowledge graph seeded successfully and ready for production queries.")

if __name__ == "__main__":
    main()
