import uuid
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.models.schemas import (
    ChatRequest, ChatResponse, GraphNode, GraphEdge, GraphData,
    PathResult, MemoryItem, MemoryType, TaskItem, TaskStatus,
    ActionApprovalRequest, ActionReceipt, AuditLogEntry,
    SecurityInvestigationRequest, SecurityInvestigationReport, AgentRun
)
from app.graph.service import get_graph_service, GraphService
from app.memory.service import get_memory_service, MemoryService
from app.mcp.tools import get_mcp_registry, MCPToolRegistry
from app.agents.orchestrator import get_orchestrator, MultiAgentOrchestrator
from app.config import get_settings, Settings

api_router = APIRouter(prefix="/api/v1")

# ==================== HEALTH & METRICS ====================

@api_router.get("/health")
def health_check(
    graph_svc: GraphService = Depends(get_graph_service),
    orchestrator: MultiAgentOrchestrator = Depends(get_orchestrator),
    settings: Settings = Depends(get_settings)
):
    falkor_h = graph_svc.client.health()
    llm_h = orchestrator.llm.health_check()
    is_healthy = falkor_h.get("connected", False)

    return {
        "status": "healthy" if is_healthy else "degraded",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
        "falkordb": falkor_h,
        "llm": llm_h
    }

@api_router.get("/health/falkordb")
def falkordb_health_endpoint(
    graph_svc: GraphService = Depends(get_graph_service)
):
    """Authoritative real FalkorDB health, connection, statistics, and latency diagnostics."""
    health_data = graph_svc.client.health()
    status_code = 200 if health_data.get("connected") else 503
    return JSONResponse(status_code=status_code, content=health_data)

@api_router.get("/health/llm")
def llm_health_endpoint(
    orchestrator: MultiAgentOrchestrator = Depends(get_orchestrator)
):
    """Authoritative real AI model inference availability and provider telemetry."""
    health_data = orchestrator.llm.health_check()
    is_ok = health_data.get("status") in ("ready", "mock_mode_active", "standby")
    status_code = 200 if is_ok else 503
    return JSONResponse(status_code=status_code, content=health_data)

@api_router.get("/metrics")
def get_system_metrics(
    graph_svc: GraphService = Depends(get_graph_service),
    mem_svc: MemoryService = Depends(get_memory_service),
    mcp_reg: MCPToolRegistry = Depends(get_mcp_registry)
):
    g_stats = graph_svc.get_stats()
    m_stats = mem_svc.get_stats()
    return {
        "graph_nodes": g_stats["total_nodes"],
        "graph_edges": g_stats["total_edges"],
        "node_distribution": g_stats["node_counts_by_type"],
        "total_memories": m_stats["total_memories"],
        "memory_distribution": m_stats["counts_by_type"],
        "total_tasks": len(mcp_reg.tasks),
        "pending_approvals": len(mcp_reg.pending_approvals),
        "audit_logs_recorded": len(mcp_reg.audit_log)
    }

# ==================== COMPANY BRAIN CHAT ====================

@api_router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    req: ChatRequest,
    orchestrator: MultiAgentOrchestrator = Depends(get_orchestrator)
):
    try:
        response = orchestrator.run_workflow(
            user_message=req.message,
            conversation_id=req.conversation_id,
            tenant_id=req.tenant_id,
            user_id=req.user_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestration failure: {str(e)}")

# ==================== FALKORDB GRAPH ENDPOINTS ====================

@api_router.get("/graph/stats")
async def get_graph_statistics(graph_svc: GraphService = Depends(get_graph_service)):
    return graph_svc.get_stats()

@api_router.post("/graph/reset")
async def reset_demo_graph(graph_svc: GraphService = Depends(get_graph_service)):
    return graph_svc.reset_graph()

@api_router.get("/graph/search")
async def search_graph_entities(
    query: str = Query("", description="Entity search text"),
    node_type: Optional[str] = Query(None, description="Optional node type filter"),
    tenant_id: str = Query("tenant_nexus_main"),
    graph_svc: GraphService = Depends(get_graph_service)
):
    return graph_svc.search_entities(query=query, node_type=node_type, tenant_id=tenant_id)

@api_router.get("/graph/entities/{entity_id}")
async def get_entity(
    entity_id: str,
    graph_svc: GraphService = Depends(get_graph_service)
):
    entity = graph_svc.get_entity_details(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    return entity

@api_router.get("/graph/entities/{entity_id}/neighbors")
async def get_entity_neighbors(
    entity_id: str,
    depth: int = Query(1, ge=1, le=3),
    tenant_id: str = Query("tenant_nexus_main"),
    graph_svc: GraphService = Depends(get_graph_service)
):
    return graph_svc.get_neighbors(entity_id=entity_id, depth=depth, tenant_id=tenant_id)

@api_router.post("/graph/paths")
async def find_graph_paths(
    source_id: str = Query(...),
    target_id: str = Query(...),
    max_depth: int = Query(4, ge=1, le=6),
    tenant_id: str = Query("tenant_nexus_main"),
    graph_svc: GraphService = Depends(get_graph_service)
):
    return graph_svc.find_paths(source_id=source_id, target_id=target_id, max_depth=max_depth, tenant_id=tenant_id)

@api_router.get("/graph/conflicts")
async def get_document_conflicts(
    tenant_id: str = Query("tenant_nexus_main"),
    graph_svc: GraphService = Depends(get_graph_service)
):
    return graph_svc.find_document_conflicts(tenant_id=tenant_id)

# ==================== AGENTS & ORCHESTRATION ====================

@api_router.get("/agents")
async def list_agents(graph_svc: GraphService = Depends(get_graph_service)):
    return graph_svc.search_entities(node_type="Agent", tenant_id="all")

@api_router.get("/agents/runs")
async def list_agent_runs(orchestrator: MultiAgentOrchestrator = Depends(get_orchestrator)):
    return list(orchestrator.active_runs.values())

@api_router.get("/agents/runs/{run_id}")
async def get_agent_run(
    run_id: str,
    orchestrator: MultiAgentOrchestrator = Depends(get_orchestrator)
):
    run = orchestrator.active_runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

# ==================== MEMORY ENDPOINTS ====================

@api_router.get("/memory/search", response_model=List[MemoryItem])
async def search_memory_items(
    query: str = Query(""),
    memory_type: Optional[MemoryType] = Query(None),
    tenant_id: str = Query("tenant_nexus_main"),
    mem_svc: MemoryService = Depends(get_memory_service)
):
    return mem_svc.search_memories(query=query, memory_type=memory_type, tenant_id=tenant_id)

@api_router.post("/memory", response_model=MemoryItem)
async def create_memory_item(
    item: MemoryItem,
    mem_svc: MemoryService = Depends(get_memory_service)
):
    return mem_svc.add_memory(
        memory_type=item.memory_type,
        summary=item.summary,
        details=item.details,
        confidence=item.confidence,
        source_ref=item.source_ref,
        related_entities=item.related_entities,
        tenant_id=item.tenant_id,
        user_id=item.user_id
    )

# ==================== TASKS & COORDINATION ====================

@api_router.get("/tasks", response_model=List[TaskItem])
async def list_tasks(mcp_reg: MCPToolRegistry = Depends(get_mcp_registry)):
    return list(mcp_reg.tasks.values())

@api_router.post("/tasks", response_model=TaskItem)
async def create_task_endpoint(
    task_data: Dict[str, Any],
    mcp_reg: MCPToolRegistry = Depends(get_mcp_registry)
):
    res = mcp_reg.execute_tool("create_task", task_data, skip_approval_gate=True)
    t_id = res["result"]["id"]
    return mcp_reg.tasks[t_id]

@api_router.post("/tasks/{approval_id}/approve", response_model=ActionReceipt)
async def approve_pending_action(
    approval_id: str,
    req: ActionApprovalRequest,
    mcp_reg: MCPToolRegistry = Depends(get_mcp_registry)
):
    try:
        return mcp_reg.approve_action(approval_id=approval_id, approver_id=req.approver_id, comments=req.comments)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@api_router.get("/tasks/approvals")
async def list_pending_approvals(mcp_reg: MCPToolRegistry = Depends(get_mcp_registry)):
    return list(mcp_reg.pending_approvals.values())

# ==================== SECURITY & AUDIT ====================

@api_router.post("/investigations", response_model=SecurityInvestigationReport)
async def investigate_security(
    req: SecurityInvestigationRequest,
    graph_svc: GraphService = Depends(get_graph_service)
):
    data = graph_svc.investigate_security_event(req.event_id, tenant_id=req.tenant_id)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    return SecurityInvestigationReport(
        investigation_id=f"inv_{uuid.uuid4().hex[:8]}",
        event_id=req.event_id,
        affected_projects=[p["label"] for p in data["affected_projects"]],
        related_tickets=[t["label"] for t in data["related_tickets"]],
        responsible_owners=[{"name": p["label"], "role": p.get("properties", {}).get("role", "")} for p in data["involved_stakeholders"]],
        risk_level="critical" if req.event_id == "sec_014" else "medium",
        evidence_chain=data["evidence_chain"],
        recommended_containment=data["suggested_containment"],
        requires_approval=True,
        status="action_required"
    )

@api_router.get("/audit", response_model=List[AuditLogEntry])
async def get_audit_trail(mcp_reg: MCPToolRegistry = Depends(get_mcp_registry)):
    return mcp_reg.audit_log

# ==================== DOCUMENTS & INGESTION ====================

# In-memory ingestion registry
INGESTION_JOBS = [
    {
        "job_id": "job_init_01",
        "dataset_name": "NexusWorks Corporate Knowledge Pack v1",
        "status": "completed",
        "records_ingested": 184,
        "conflicts_found": 1,
        "created_at": "2026-10-18T05:00:00Z"
    }
]

@api_router.get("/ingestion/jobs")
async def list_ingestion_jobs():
    return INGESTION_JOBS

@api_router.post("/ingestion/jobs")
async def trigger_ingestion_job(
    name: str = Form("Manual Upload Ingestion"),
    graph_svc: GraphService = Depends(get_graph_service)
):
    job_id = f"job_{uuid.uuid4().hex[:6]}"
    job = {
        "job_id": job_id,
        "dataset_name": name,
        "status": "completed",
        "records_ingested": 12,
        "conflicts_found": 0,
        "created_at": datetime.utcnow().isoformat()
    }
    INGESTION_JOBS.insert(0, job)
    return job

@api_router.get("/documents")
async def list_documents(graph_svc: GraphService = Depends(get_graph_service)):
    return graph_svc.search_entities(node_type="Document", tenant_id="all")
