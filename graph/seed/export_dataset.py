#!/usr/bin/env python3
"""
Exports the full NexusWorks synthetic dataset (nodes & edges) to JSON.
"""
import json
import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.graph.synthetic_company import generate_nexusworks_data

def main():
    nodes, edges = generate_nexusworks_data()
    out_dir = Path(__file__).resolve().parent.parent.parent / "datasets" / "synthetic"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "nexusworks.json"

    data = {
        "version": "1.0.0",
        "company": "NexusWorks Technologies Inc.",
        "nodes_count": len(nodes),
        "edges_count": len(edges),
        "nodes": nodes,
        "edges": edges
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[SUCCESS] Exported {len(nodes)} nodes and {len(edges)} edges to {out_file}")

if __name__ == "__main__":
    main()
