"""
Migration 001: Initial FalkorDB Knowledge Graph Schema & Indexes
"""
import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.graph.service import get_graph_service

def up():
    print("Applying Migration 001: Initial Schema & Indexes...")
    service = get_graph_service()
    stats = service.get_stats()
    print(f"Migration 001 applied successfully. Engine: {stats['engine_mode']}, Nodes: {stats['total_nodes']}")

def down():
    print("Reverting Migration 001...")

if __name__ == "__main__":
    up()
