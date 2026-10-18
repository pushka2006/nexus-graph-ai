import pytest
from app.graph.service import GraphService
from app.graph.falkor_client import FalkorDBClient

def test_falkordb_client_initialization():
    client = FalkorDBClient(graph_name="test_graph")
    client.clear()
    
    # Create nodes
    client.upsert_node("p1", "Person", "Alice", {"role": "Engineer"})
    client.upsert_node("p2", "Project", "Project Alpha", {"status": "active"})
    client.upsert_edge("e1", "p1", "p2", "WORKS_ON", {"since": "2026"})

    stats = client.get_stats()
    assert stats["total_nodes"] == 2
    assert stats["total_edges"] == 1

    # Verify neighbors
    neighbors = client.get_neighbors("p1", depth=1)
    assert len(neighbors["nodes"]) == 2
    assert len(neighbors["edges"]) == 1

def test_synthetic_company_seeding():
    service = GraphService()
    service.reset_graph()
    stats = service.get_stats()

    # Verify required minimums from prompt:
    # >= 30 employees, >= 6 depts, >= 10 projects, >= 50 docs, >= 40 tickets, >= 20 meetings, >= 25 decisions, >= 20 tasks, >= 15 security events
    node_counts = stats["node_counts_by_type"]
    assert node_counts.get("Person", 0) >= 30, f"Expected >= 30 persons, got {node_counts.get('Person')}"
    assert node_counts.get("Department", 0) >= 6, f"Expected >= 6 departments, got {node_counts.get('Department')}"
    assert node_counts.get("Project", 0) >= 10, f"Expected >= 10 projects, got {node_counts.get('Project')}"
    assert node_counts.get("Document", 0) >= 50, f"Expected >= 50 documents, got {node_counts.get('Document')}"
    assert node_counts.get("Ticket", 0) >= 40, f"Expected >= 40 tickets, got {node_counts.get('Ticket')}"
    assert node_counts.get("Meeting", 0) >= 20, f"Expected >= 20 meetings, got {node_counts.get('Meeting')}"
    assert node_counts.get("Decision", 0) >= 25, f"Expected >= 25 decisions, got {node_counts.get('Decision')}"
    assert node_counts.get("Task", 0) >= 20, f"Expected >= 20 tasks, got {node_counts.get('Task')}"
    assert node_counts.get("SecurityEvent", 0) >= 15, f"Expected >= 15 security events, got {node_counts.get('SecurityEvent')}"

def test_project_atlas_multi_hop_blocker():
    service = GraphService()
    blockers = service.get_project_blockers("proj_atlas")
    assert len(blockers) > 0
    # Blocker should be AD-104
    b = blockers[0]
    assert b["blocker_entity"]["id"] == "dec_104"
    assert "Cloud Storage" in b["blocker_entity"]["label"]

def test_document_supersession_conflict():
    service = GraphService()
    conflicts = service.find_document_conflicts()
    assert len(conflicts) > 0
    c = conflicts[0]
    assert c["active_document"]["id"] == "doc_sec_pol_v20"
    assert c["superseded_document"]["id"] == "doc_sec_pol_v12"

def test_multi_hop_path_finder():
    service = GraphService()
    # Find path from SEC-014 to Project Atlas
    paths = service.find_paths("sec_014", "proj_atlas", max_depth=3)
    assert len(paths) > 0
    assert paths[0]["hop_count"] >= 1
