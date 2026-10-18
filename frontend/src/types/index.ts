export type NodeType =
  | 'Company'
  | 'Department'
  | 'Team'
  | 'Person'
  | 'Project'
  | 'Document'
  | 'Ticket'
  | 'Meeting'
  | 'Decision'
  | 'Task'
  | 'Incident'
  | 'SecurityEvent'
  | 'Agent'
  | 'Memory'
  | 'Source';

export type RelationType =
  | 'MEMBER_OF'
  | 'MANAGES'
  | 'OWNS'
  | 'ASSIGNED_TO'
  | 'WORKS_ON'
  | 'DEPENDS_ON'
  | 'BLOCKED_BY'
  | 'MENTIONS'
  | 'DISCUSSED_IN'
  | 'DECIDED_IN'
  | 'SUPPORTED_BY'
  | 'SUPERSEDES'
  | 'RELATED_TO'
  | 'REPORTED_BY'
  | 'LINKED_TO'
  | 'CREATED_BY'
  | 'DERIVED_FROM'
  | 'REMEMBERS'
  | 'HANDOFF_TO';

export interface GraphNodeData {
  id: string;
  label: string;
  type: NodeType;
  properties: Record<string, any>;
  tenant_id?: string;
  created_at?: string;
}

export interface GraphEdgeData {
  id: string;
  source: string;
  target: string;
  type: RelationType;
  properties?: Record<string, any>;
  tenant_id?: string;
}

export interface GraphData {
  nodes: GraphNodeData[];
  edges: GraphEdgeData[];
}

export interface Citation {
  source_id: string;
  source_title: string;
  document_id?: string;
  record_id?: string;
  passage: string;
  timestamp?: string;
  confidence: number;
  freshness_status: 'current' | 'superseded' | 'disputed';
  superseded_by?: string;
}

export interface EvidenceGraphPath {
  path_description: string;
  node_ids: string[];
  relationship_types: string[];
}

export interface SuggestedAction {
  action_id: string;
  tool_name: string;
  title: string;
  parameters: Record<string, any>;
  requires_approval: boolean;
  dry_run_summary: string;
}

export interface ChatResponse {
  answer: string;
  conversation_id: string;
  direct_facts: string[];
  citations: Citation[];
  evidence_paths: EvidenceGraphPath[];
  graph_data?: GraphData;
  conflicting_evidence: string[];
  suggested_actions: SuggestedAction[];
  confidence: number;
  model_used: string;
  latency_ms: number;
}

export interface ToolCallRecord {
  tool_name: string;
  parameters: Record<string, any>;
  output: any;
  timestamp: string;
  status: string;
}

export interface AgentExecutionStep {
  step_number: number;
  agent_name: string;
  thought: string;
  action_taken: string;
  tool_calls: ToolCallRecord[];
  result_summary: string;
  timestamp: string;
}

export interface AgentRun {
  id: string;
  user_id: string;
  tenant_id: string;
  initial_prompt: string;
  status: 'running' | 'completed' | 'waiting_approval' | 'failed';
  steps: AgentExecutionStep[];
  current_agent: string;
  created_at: string;
  completed_at?: string;
}

export interface MemoryItem {
  id: string;
  tenant_id: string;
  user_id?: string;
  memory_type: 'episodic' | 'semantic' | 'procedural';
  summary: string;
  details: Record<string, any>;
  confidence: number;
  source_ref?: string;
  related_entities: string[];
  verified: boolean;
  created_at: string;
  access_count: number;
}

export interface TaskItem {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'blocked' | 'waiting_approval' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  assigned_to?: string;
  assigned_agent?: string;
  project_id?: string;
  ticket_id?: string;
  blocked_by: string[];
  depends_on: string[];
  tenant_id: string;
  created_at: string;
  updated_at: string;
}

export interface SecurityInvestigationReport {
  investigation_id: string;
  event_id: string;
  affected_projects: string[];
  related_tickets: string[];
  responsible_owners: Array<{ name: string; role: string }>;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  evidence_chain: string[];
  recommended_containment: string[];
  requires_approval: boolean;
  status: string;
}

export interface AuditLogEntry {
  id: string;
  timestamp: string;
  actor: string;
  actor_type: 'user' | 'agent' | 'system';
  action: string;
  target_resource: string;
  parameters: Record<string, any>;
  status: 'authorized' | 'denied' | 'executed' | 'failed';
  tenant_id: string;
  details?: string;
}

export interface SystemHealth {
  status: string;
  service: string;
  environment: string;
  timestamp: string;
  falkordb: {
    connected_to_live: boolean;
    engine_mode: string;
    graph_name: string;
    node_count: number;
    edge_count: number;
  };
  llm_provider: string;
  primary_model: string;
}
