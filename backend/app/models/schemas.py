from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

# ==================== ENUMS ====================

class NodeType(str, Enum):
    COMPANY = "Company"
    DEPARTMENT = "Department"
    TEAM = "Team"
    PERSON = "Person"
    PROJECT = "Project"
    DOCUMENT = "Document"
    TICKET = "Ticket"
    MEETING = "Meeting"
    DECISION = "Decision"
    TASK = "Task"
    INCIDENT = "Incident"
    SECURITY_EVENT = "SecurityEvent"
    AGENT = "Agent"
    MEMORY = "Memory"
    SOURCE = "Source"

class RelationType(str, Enum):
    MEMBER_OF = "MEMBER_OF"
    MANAGES = "MANAGES"
    OWNS = "OWNS"
    ASSIGNED_TO = "ASSIGNED_TO"
    WORKS_ON = "WORKS_ON"
    DEPENDS_ON = "DEPENDS_ON"
    BLOCKED_BY = "BLOCKED_BY"
    MENTIONS = "MENTIONS"
    DISCUSSED_IN = "DISCUSSED_IN"
    DECIDED_IN = "DECIDED_IN"
    SUPPORTED_BY = "SUPPORTED_BY"
    SUPERSEDES = "SUPERSEDES"
    RELATED_TO = "RELATED_TO"
    REPORTED_BY = "REPORTED_BY"
    LINKED_TO = "LINKED_TO"
    CREATED_BY = "CREATED_BY"
    DERIVED_FROM = "DERIVED_FROM"
    REMEMBERS = "REMEMBERS"
    HANDOFF_TO = "HANDOFF_TO"

class MemoryType(str, Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentRole(str, Enum):
    ORCHESTRATOR = "Master Orchestrator"
    GRAPH_REASONING = "Graph Reasoning Agent"
    COMPANY_KNOWLEDGE = "Company Knowledge Agent"
    MEMORY_AGENT = "Memory Agent"
    COORDINATION_AGENT = "Coordination Agent"
    SECURITY_INVESTIGATION = "Security Investigation Agent"
    ACTION_AGENT = "Action Agent"
    QUALITY_VERIFICATION = "Quality & Verification Agent"

# ==================== GRAPH SCHEMAS ====================

class GraphNode(BaseModel):
    id: str
    label: str
    type: NodeType
    properties: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: str = "tenant_nexus_main"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: RelationType
    properties: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: str = "tenant_nexus_main"
    created_at: Optional[datetime] = None

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class PathResult(BaseModel):
    source_id: str
    target_id: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    hop_count: int
    explanation: str

# ==================== EVIDENCE & CITATIONS ====================

class Citation(BaseModel):
    source_id: str
    source_title: str
    document_id: Optional[str] = None
    record_id: Optional[str] = None
    passage: str
    timestamp: Optional[str] = None
    confidence: float = 1.0
    freshness_status: str = "current"  # 'current', 'superseded', 'disputed'
    superseded_by: Optional[str] = None

class EvidenceGraphPath(BaseModel):
    path_description: str
    node_ids: List[str]
    relationship_types: List[str]

# ==================== CHAT & QUESTION ANSWERING ====================

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    tenant_id: str = "tenant_nexus_main"
    user_id: str = "user_admin"
    enable_graph_traversal: bool = True
    enable_memory_recall: bool = True
    stream: bool = False

class SuggestedAction(BaseModel):
    action_id: str
    tool_name: str
    title: str
    parameters: Dict[str, Any]
    requires_approval: bool = True
    dry_run_summary: str

class ChatResponse(BaseModel):
    answer: str
    conversation_id: str
    direct_facts: List[str] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    evidence_paths: List[EvidenceGraphPath] = Field(default_factory=list)
    graph_data: Optional[GraphData] = None
    conflicting_evidence: List[str] = Field(default_factory=list)
    suggested_actions: List[SuggestedAction] = Field(default_factory=list)
    confidence: float = 0.95
    model_used: str = "Qwen/Qwen2.5-3B-Instruct (Mock Provider)"
    latency_ms: float = 0.0

# ==================== AGENTS & COORDINATION ====================

class ToolCallRecord(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    output: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "success"

class AgentExecutionStep(BaseModel):
    step_number: int
    agent_name: str
    thought: str
    action_taken: str
    tool_calls: List[ToolCallRecord] = Field(default_factory=list)
    result_summary: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AgentRun(BaseModel):
    id: str
    user_id: str
    tenant_id: str
    initial_prompt: str
    status: str  # 'running', 'completed', 'waiting_approval', 'failed'
    steps: List[AgentExecutionStep] = Field(default_factory=list)
    current_agent: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    audit_receipt_id: Optional[str] = None

class TaskItem(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: str = "medium"  # 'low', 'medium', 'high', 'critical'
    assigned_to: Optional[str] = None
    assigned_agent: Optional[str] = None
    project_id: Optional[str] = None
    ticket_id: Optional[str] = None
    blocked_by: List[str] = Field(default_factory=list)
    depends_on: List[str] = Field(default_factory=list)
    tenant_id: str = "tenant_nexus_main"
    lease_holder: Optional[str] = None
    lease_expires_at: Optional[datetime] = None
    idempotency_key: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# ==================== MEMORY SCHEMAS ====================

class MemoryItem(BaseModel):
    id: str
    tenant_id: str = "tenant_nexus_main"
    user_id: Optional[str] = None
    memory_type: MemoryType
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    source_ref: Optional[str] = None
    related_entities: List[str] = Field(default_factory=list)
    verified: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    access_count: int = 0

# ==================== SECURITY & AUDIT ====================

class SecurityInvestigationRequest(BaseModel):
    event_id: str
    target_project_id: Optional[str] = None
    tenant_id: str = "tenant_nexus_main"

class SecurityInvestigationReport(BaseModel):
    investigation_id: str
    event_id: str
    affected_projects: List[str]
    related_tickets: List[str]
    responsible_owners: List[Dict[str, str]]
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    evidence_chain: List[str]
    recommended_containment: List[str]
    requires_approval: bool = True
    status: str = "action_required"

class AuditLogEntry(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    actor: str
    actor_type: str  # 'user', 'agent', 'system'
    action: str
    target_resource: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str  # 'authorized', 'denied', 'executed', 'failed'
    tenant_id: str = "tenant_nexus_main"
    details: Optional[str] = None

# ==================== MCP ACTION SCHEMAS ====================

class ActionApprovalRequest(BaseModel):
    action_id: str
    approved: bool
    approver_id: str
    comments: Optional[str] = None

class ActionReceipt(BaseModel):
    receipt_id: str
    action_id: str
    tool_name: str
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    status: str
    result: Dict[str, Any]
    audit_log_id: str
