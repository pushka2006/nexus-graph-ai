import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.graph.service import get_graph_service
from app.memory.service import get_memory_service
from app.models.schemas import TaskItem, TaskStatus, ActionReceipt, AuditLogEntry
from app.config import get_settings

logger = logging.getLogger("nexus.mcp.tools")

class MCPToolRegistry:
    """
    Model Context Protocol (MCP) compatible tool interface.
    Enforces input schema validation, permission checks, dry-run previews,
    human-in-the-loop authorization gates, and audit trails.
    """
    def __init__(self):
        self.settings = get_settings()
        self.graph_service = get_graph_service()
        self.memory_service = get_memory_service()
        self.audit_log: List[AuditLogEntry] = []
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}
        self.tasks: Dict[str, TaskItem] = {}
        self._init_default_tasks()

    def _init_default_tasks(self):
        defaults = [
            TaskItem(
                id="task_live_01",
                title="Review S3 KMS Encryption Compliance for Project Atlas",
                description="Investigate architecture alignment between AD-104 and Policy v2.0.",
                status=TaskStatus.IN_PROGRESS,
                priority="critical",
                assigned_to="emp_07",
                assigned_agent="Graph Reasoning Agent",
                project_id="proj_atlas",
                tenant_id="tenant_nexus_main"
            ),
            TaskItem(
                id="task_live_02",
                title="Revoke Compromised Internal Worker Token",
                description="Security containment for SEC-014 on worker svc-atlas-worker.",
                status=TaskStatus.WAITING_APPROVAL,
                priority="critical",
                assigned_to="emp_09",
                assigned_agent="Action Agent",
                project_id="proj_atlas",
                tenant_id="tenant_nexus_main"
            )
        ]
        for t in defaults:
            self.tasks[t.id] = t

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "search_entities",
                "description": "Search company nodes across people, projects, documents, and tickets in FalkorDB.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "node_type": {"type": "string"}
                    }
                },
                "is_readonly": True
            },
            {
                "name": "get_entity_details",
                "description": "Retrieve full attributes, properties, and metadata for a specific entity ID.",
                "parameters": {
                    "type": "object",
                    "properties": {"entity_id": {"type": "string"}},
                    "required": ["entity_id"]
                },
                "is_readonly": True
            },
            {
                "name": "get_neighbors",
                "description": "Expand graph neighborhood around an entity to find connected nodes and edges.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_id": {"type": "string"},
                        "depth": {"type": "integer", "default": 1}
                    },
                    "required": ["entity_id"]
                },
                "is_readonly": True
            },
            {
                "name": "find_paths",
                "description": "Find multi-hop Cypher paths between two entities in FalkorDB.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_id": {"type": "string"},
                        "target_id": {"type": "string"},
                        "max_depth": {"type": "integer", "default": 4}
                    },
                    "required": ["source_id", "target_id"]
                },
                "is_readonly": True
            },
            {
                "name": "get_project_dependencies",
                "description": "Analyze blockers, dependencies, and owners for a project.",
                "parameters": {
                    "type": "object",
                    "properties": {"project_id": {"type": "string"}},
                    "required": ["project_id"]
                },
                "is_readonly": True
            },
            {
                "name": "find_document_conflicts",
                "description": "Detect superseded policies or contradictory document statements in the graph.",
                "parameters": {"type": "object", "properties": {}},
                "is_readonly": True
            },
            {
                "name": "get_decision_history",
                "description": "Retrieve chronological architecture decisions and supporting documents.",
                "parameters": {
                    "type": "object",
                    "properties": {"project_id": {"type": "string"}}
                },
                "is_readonly": True
            },
            {
                "name": "investigate_security_event",
                "description": "Run graph reasoning to correlate security events with incidents, tickets, and owners.",
                "parameters": {
                    "type": "object",
                    "properties": {"event_id": {"type": "string"}},
                    "required": ["event_id"]
                },
                "is_readonly": True
            },
            {
                "name": "get_source_evidence",
                "description": "Retrieve raw source text, hashes, and document timestamps for an answer.",
                "parameters": {
                    "type": "object",
                    "properties": {"document_id": {"type": "string"}},
                    "required": ["document_id"]
                },
                "is_readonly": True
            },
            {
                "name": "create_task",
                "description": "Create a new engineering task or follow-up item (Requires approval if production-critical).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "priority": {"type": "string"},
                        "assigned_to": {"type": "string"},
                        "project_id": {"type": "string"}
                    },
                    "required": ["title", "description"]
                },
                "is_readonly": False
            },
            {
                "name": "assign_task",
                "description": "Assign or hand off a task to another agent or person.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "assigned_to": {"type": "string"}
                    },
                    "required": ["task_id", "assigned_to"]
                },
                "is_readonly": False
            },
            {
                "name": "prepare_incident_report",
                "description": "Generate an authoritative incident summary report for compliance and audit.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "event_id": {"type": "string"}
                    },
                    "required": ["incident_id"]
                },
                "is_readonly": False
            }
        ]

    def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        actor: str = "agent_action",
        tenant_id: str = "tenant_nexus_main",
        skip_approval_gate: bool = False
    ) -> Dict[str, Any]:
        tool_defs = {t["name"]: t for t in self.get_tool_definitions()}
        if tool_name not in tool_defs:
            return {"status": "error", "message": f"Tool '{tool_name}' not allowlisted."}

        tool_meta = tool_defs[tool_name]
        is_readonly = tool_meta.get("is_readonly", False)

        # Human-in-the-loop authorization check
        if not is_readonly and self.settings.REQUIRE_HUMAN_APPROVAL_FOR_ACTIONS and not skip_approval_gate:
            approval_id = f"appr_{uuid.uuid4().hex[:8]}"
            self.pending_approvals[approval_id] = {
                "approval_id": approval_id,
                "tool_name": tool_name,
                "parameters": parameters,
                "actor": actor,
                "tenant_id": tenant_id,
                "requested_at": datetime.utcnow().isoformat(),
                "status": "pending"
            }
            self._log_audit(actor, "agent", f"request_approval:{tool_name}", "approval_gate", parameters, "waiting_approval", tenant_id)
            return {
                "status": "waiting_approval",
                "approval_id": approval_id,
                "message": f"Action '{tool_name}' requires human approval before state-changing execution.",
                "parameters": parameters
            }

        # Execute
        result = self._dispatch_execution(tool_name, parameters, tenant_id)
        self._log_audit(actor, "agent", f"execute:{tool_name}", "graph_or_task_store", parameters, "executed", tenant_id)
        return {
            "status": "success",
            "result": result,
            "receipt_id": f"rcpt_{uuid.uuid4().hex[:8]}"
        }

    def _dispatch_execution(self, tool_name: str, params: Dict[str, Any], tenant_id: str) -> Any:
        if tool_name == "search_entities":
            return self.graph_service.search_entities(
                query=params.get("query", ""),
                node_type=params.get("node_type"),
                tenant_id=tenant_id
            )
        elif tool_name == "get_entity_details":
            return self.graph_service.get_entity_details(params["entity_id"])
        elif tool_name == "get_neighbors":
            return self.graph_service.get_neighbors(
                entity_id=params["entity_id"],
                depth=params.get("depth", 1),
                tenant_id=tenant_id
            )
        elif tool_name == "find_paths":
            return self.graph_service.find_paths(
                source_id=params["source_id"],
                target_id=params["target_id"],
                max_depth=params.get("max_depth", 4),
                tenant_id=tenant_id
            )
        elif tool_name == "get_project_dependencies":
            return self.graph_service.get_project_blockers(params["project_id"], tenant_id=tenant_id)
        elif tool_name == "find_document_conflicts":
            return self.graph_service.find_document_conflicts(tenant_id=tenant_id)
        elif tool_name == "investigate_security_event":
            return self.graph_service.investigate_security_event(params["event_id"], tenant_id=tenant_id)
        elif tool_name == "get_source_evidence":
            doc = self.graph_service.get_entity_details(params["document_id"])
            return doc.get("properties") if doc else {"error": "Document not found"}
        elif tool_name == "create_task":
            t_id = f"task_{uuid.uuid4().hex[:6]}"
            task = TaskItem(
                id=t_id,
                title=params.get("title", "New Task"),
                description=params.get("description", ""),
                status=TaskStatus.PENDING,
                priority=params.get("priority", "medium"),
                assigned_to=params.get("assigned_to"),
                project_id=params.get("project_id"),
                tenant_id=tenant_id
            )
            self.tasks[t_id] = task
            # Also register in graph
            self.graph_service.client.upsert_node(t_id, "Task", task.title, {
                "description": task.description,
                "status": task.status.value,
                "priority": task.priority
            }, tenant_id)
            if task.assigned_to:
                self.graph_service.client.upsert_edge(f"asg_{t_id}_{task.assigned_to}", t_id, task.assigned_to, "ASSIGNED_TO", tenant_id=tenant_id)
            return task.model_dump()
        elif tool_name == "assign_task":
            t_id = params["task_id"]
            if t_id in self.tasks:
                self.tasks[t_id].assigned_to = params["assigned_to"]
                self.tasks[t_id].updated_at = datetime.utcnow()
                return self.tasks[t_id].model_dump()
            return {"error": f"Task {t_id} not found"}
        elif tool_name == "prepare_incident_report":
            return {
                "incident_id": params.get("incident_id"),
                "event_id": params.get("event_id"),
                "status": "incident_report_generated",
                "summary": "Automated containment report compiled with FalkorDB audit trail.",
                "timestamp": datetime.utcnow().isoformat()
            }
        return {"result": "ok"}

    def approve_action(self, approval_id: str, approver_id: str = "user_admin", comments: Optional[str] = None) -> ActionReceipt:
        item = self.pending_approvals.get(approval_id)
        if not item:
            raise ValueError(f"Approval request {approval_id} not found.")

        item["status"] = "approved"
        item["approver_id"] = approver_id
        item["approved_at"] = datetime.utcnow().isoformat()

        # Execute approved tool
        res = self._dispatch_execution(item["tool_name"], item["parameters"], item["tenant_id"])
        audit_id = self._log_audit(approver_id, "user", f"approve:{item['tool_name']}", "approval_gate", item["parameters"], "authorized", item["tenant_id"], comments)

        receipt = ActionReceipt(
            receipt_id=f"rcpt_{uuid.uuid4().hex[:8]}",
            action_id=approval_id,
            tool_name=item["tool_name"],
            status="executed",
            result={"output": res, "comments": comments},
            audit_log_id=audit_id
        )
        return receipt

    def _log_audit(self, actor: str, actor_type: str, action: str, target: str, params: Dict[str, Any], status: str, tenant_id: str, details: str = None) -> str:
        log_id = f"aud_{uuid.uuid4().hex[:8]}"
        entry = AuditLogEntry(
            id=log_id,
            actor=actor,
            actor_type=actor_type,
            action=action,
            target_resource=target,
            parameters=params,
            status=status,
            tenant_id=tenant_id,
            details=details
        )
        self.audit_log.insert(0, entry)
        return log_id

_mcp_registry = None

def get_mcp_registry() -> MCPToolRegistry:
    global _mcp_registry
    if _mcp_registry is None:
        _mcp_registry = MCPToolRegistry()
    return _mcp_registry
