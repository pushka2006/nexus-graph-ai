import {
  ChatResponse,
  GraphNodeData,
  GraphData,
  MemoryItem,
  TaskItem,
  SecurityInvestigationReport,
  AuditLogEntry,
  SystemHealth
} from '@/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {})
      }
    });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`API error ${res.status}: ${errText}`);
    }
    return (await res.json()) as T;
  } catch (err: any) {
    console.error(`Failed to fetch ${url}:`, err);
    throw err;
  }
}

export const api = {
  // System Health & Telemetry
  getHealth: () => fetchJson<SystemHealth>('/api/v1/health'),
  getMetrics: () => fetchJson<Record<string, any>>('/api/v1/metrics'),

  // Company Brain Chat
  sendChat: (message: string, conversationId?: string, tenantId = 'tenant_nexus_main') =>
    fetchJson<ChatResponse>('/api/v1/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        tenant_id: tenantId,
        user_id: 'user_admin'
      })
    }),

  // FalkorDB Knowledge Graph
  searchGraph: (query = '', nodeType?: string, tenantId = 'tenant_nexus_main') => {
    const params = new URLSearchParams({ query, tenant_id: tenantId });
    if (nodeType) params.append('node_type', nodeType);
    return fetchJson<GraphNodeData[]>(`/api/v1/graph/search?${params.toString()}`);
  },
  getEntity: (entityId: string) => fetchJson<GraphNodeData>(`/api/v1/graph/entities/${entityId}`),
  getNeighbors: (entityId: string, depth = 1, tenantId = 'tenant_nexus_main') =>
    fetchJson<GraphData>(`/api/v1/graph/entities/${entityId}/neighbors?depth=${depth}&tenant_id=${tenantId}`),
  findPaths: (sourceId: string, targetId: string, maxDepth = 4, tenantId = 'tenant_nexus_main') =>
    fetchJson<any[]>(`/api/v1/graph/paths?source_id=${sourceId}&target_id=${targetId}&max_depth=${maxDepth}&tenant_id=${tenantId}`, {
      method: 'POST'
    }),
  getConflicts: (tenantId = 'tenant_nexus_main') =>
    fetchJson<any[]>(`/api/v1/graph/conflicts?tenant_id=${tenantId}`),
  resetGraph: () => fetchJson<{ status: string; nodes_count: number; edges_count: number }>('/api/v1/graph/reset', { method: 'POST' }),

  // Multi-Agent Orchestration
  getAgents: () => fetchJson<GraphNodeData[]>('/api/v1/agents'),
  getAgentRuns: () => fetchJson<any[]>('/api/v1/agents/runs'),
  getAgentRun: (runId: string) => fetchJson<any>(`/api/v1/agents/runs/${runId}`),

  // Persistent Memory (Episodic, Semantic, Procedural)
  searchMemories: (query = '', memoryType?: string, tenantId = 'tenant_nexus_main') => {
    const params = new URLSearchParams({ query, tenant_id: tenantId });
    if (memoryType) params.append('memory_type', memoryType);
    return fetchJson<MemoryItem[]>(`/api/v1/memory/search?${params.toString()}`);
  },
  createMemory: (memory: Partial<MemoryItem>) =>
    fetchJson<MemoryItem>('/api/v1/memory', {
      method: 'POST',
      body: JSON.stringify(memory)
    }),

  // Tasks & Action Execution
  getTasks: () => fetchJson<TaskItem[]>('/api/v1/tasks'),
  createTask: (task: Record<string, any>) =>
    fetchJson<TaskItem>('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(task)
    }),
  getPendingApprovals: () => fetchJson<any[]>('/api/v1/tasks/approvals'),
  approveAction: (approvalId: string, approverId = 'user_admin', comments?: string) =>
    fetchJson<any>(`/api/v1/tasks/${approvalId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ action_id: approvalId, approved: true, approver_id: approverId, comments })
    }),

  // Security Investigation Center
  investigateSecurity: (eventId: string, tenantId = 'tenant_nexus_main') =>
    fetchJson<SecurityInvestigationReport>('/api/v1/investigations', {
      method: 'POST',
      body: JSON.stringify({ event_id: eventId, tenant_id: tenantId })
    }),

  // Audit Logs
  getAuditLogs: () => fetchJson<AuditLogEntry[]>('/api/v1/audit'),

  // Documents & Ingestion
  getDocuments: () => fetchJson<GraphNodeData[]>('/api/v1/documents'),
  getIngestionJobs: () => fetchJson<any[]>('/api/v1/ingestion/jobs'),
  triggerIngestionJob: (name: string) => {
    const fd = new FormData();
    fd.append('name', name);
    return fetch(`${API_BASE}/api/v1/ingestion/jobs`, {
      method: 'POST',
      body: fd
    }).then(r => r.json());
  }
};
