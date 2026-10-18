import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.graph.falkor_client import FalkorDBClient
from app.graph.service import get_graph_service
from app.llm.adapter import get_llm_adapter
from app.agents.orchestrator import get_orchestrator
from app.memory.service import get_memory_service

client = TestClient(app)


# ==================== REAL FALKORDB INTEGRATION TESTS ====================

def test_live_falkordb_connection_and_cypher_execution():
    """Verify live FalkorDB connectivity, isolated graph mutations, and Cypher queries."""
    falkor = FalkorDBClient(graph_name="nexus_pytest_isolated")
    assert falkor.is_connected is True, f"Failed to connect to live FalkorDB: {falkor.last_error}"
    
    # 1. Clean test graph
    falkor.clear()
    
    # 2. Upsert real nodes
    n1 = falkor.upsert_node("pytest_emp_1", "Person", "Test Alice", {"role": "SecOps Engineer"})
    n2 = falkor.upsert_node("pytest_proj_1", "Project", "Test Project", {"status": "in_progress"})
    assert n1["id"] == "pytest_emp_1"
    assert n2["id"] == "pytest_proj_1"
    
    # 3. Upsert real edge
    edge = falkor.upsert_edge("pytest_rel_1", "pytest_emp_1", "pytest_proj_1", "WORKS_ON", {"since": "2026"})
    assert edge["type"] == "WORKS_ON"
    
    # 4. Multi-hop neighbor query
    neighbors = falkor.get_neighbors("pytest_emp_1", depth=1)
    node_ids = [n["id"] for n in neighbors["nodes"]]
    assert "pytest_emp_1" in node_ids
    assert "pytest_proj_1" in node_ids
    assert len(neighbors["edges"]) >= 1
    
    # 5. Native Cypher query
    res = falkor.query("MATCH (p:Person {id: $id}) RETURN p.label AS name", {"id": "pytest_emp_1"})
    assert len(res) > 0
    assert res[0][0] == "Test Alice"
    
    # 6. Cleanup isolated test graph
    falkor.clear()
    stats = falkor.get_stats()
    assert stats["total_nodes"] == 0
    assert stats["total_edges"] == 0


def test_production_falkordb_nexusworks_dataset():
    """Verify production graph is populated with all NexusWorks company entities and edges."""
    graph_svc = get_graph_service()
    stats = graph_svc.get_stats()
    
    assert stats["is_connected_to_live_falkordb"] is True
    assert stats["engine_mode"] == "live_falkordb"
    assert stats["total_nodes"] >= 300, f"Expected >= 300 nodes, got {stats['total_nodes']}"
    assert stats["total_edges"] >= 350, f"Expected >= 350 edges, got {stats['total_edges']}"
    
    # Verify Project Atlas blockers
    blockers = graph_svc.get_project_blockers("proj_atlas")
    assert len(blockers) > 0
    assert blockers[0]["blocker_entity"]["id"] == "dec_104"
    
    # Verify policy conflicts
    conflicts = graph_svc.find_document_conflicts()
    assert len(conflicts) > 0
    assert conflicts[0]["active_document"]["id"] == "doc_sec_pol_v20"


# ==================== REAL MODEL INFERENCE TESTS ====================

def test_real_llm_adapter_diagnostics():
    """Verify configured model adapter reports real telemetry and status."""
    adapter = get_llm_adapter()
    health = adapter.health_check()
    
    assert health["provider"] in ("huggingface", "openai", "vllm", "mock")
    assert "model_id" in health
    assert "latency_ms" in health
    assert health["status"] in ("ready", "standby", "mock_mode_active")


def test_real_agent_orchestration_grounded_response():
    """Verify Master Orchestrator coordinates agents, traverses FalkorDB, and returns citations."""
    orchestrator = get_orchestrator()
    response = orchestrator.run_workflow(
        user_message="Who owns Project Atlas, why is its release blocked, and what action should we take?",
        tenant_id="tenant_nexus_main",
        user_id="user_admin"
    )
    
    assert response.answer is not None and len(response.answer) > 0
    assert len(response.citations) > 0
    assert len(response.evidence_paths) > 0
    assert len(response.suggested_actions) > 0
    
    # Verify suggested action requires approval
    action = response.suggested_actions[0]
    assert action.requires_approval is True
    assert action.tool_name in ("create_task", "prepare_incident_report")


# ==================== HEALTH & REST API TESTS ====================

def test_health_api_endpoints():
    """Verify FastAPI /health, /health/falkordb, and /health/llm return HTTP 200 with real telemetry."""
    # Main health
    r1 = client.get("/api/v1/health")
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["status"] == "healthy"
    assert data1["falkordb"]["connected"] is True
    
    # FalkorDB specific health
    r2 = client.get("/api/v1/health/falkordb")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["connected"] is True
    assert data2["query_success"] is True
    assert data2["total_nodes"] >= 300
    
    # LLM health
    r3 = client.get("/api/v1/health/llm")
    assert r3.status_code == 200
    data3 = r3.json()
    assert data3["status"] in ("ready", "standby", "mock_mode_active")
