'use client';

import React, { useState, useEffect } from 'react';
import { Bot, Zap, ArrowRight, CheckCircle2, Clock, ShieldCheck, Terminal, Layers } from 'lucide-react';
import { api } from '@/lib/api';

const AGENTS = [
  {
    id: 'agent_orchestrator',
    name: 'Master Orchestrator',
    role: 'Multi-Agent Coordination & Workflow Management',
    desc: 'Understands user intent, classifies query type, delegates tasks to specialized agents, and merges evidence.',
    status: 'Ready',
    color: 'border-cyan-500/50 bg-cyan-950/20 text-cyan-400'
  },
  {
    id: 'agent_graph',
    name: 'Graph Reasoning Agent',
    role: 'FalkorDB Cypher Multi-Hop Reasoning',
    desc: 'Translates natural language questions into validated parameterized Cypher query templates and traverses dependencies.',
    status: 'Active',
    color: 'border-purple-500/50 bg-purple-950/20 text-purple-400'
  },
  {
    id: 'agent_knowledge',
    name: 'Company Knowledge Agent',
    role: 'Document Retrieval, Provenance & Conflict Checking',
    desc: 'Retrieves passages across company documents, detects policy supersession, and checks freshness timestamps.',
    status: 'Ready',
    color: 'border-blue-500/50 bg-blue-950/20 text-blue-400'
  },
  {
    id: 'agent_memory',
    name: 'Memory Agent',
    role: 'Episodic, Semantic & Procedural Memory Maintenance',
    desc: 'Maintains long-term persistent shared memory, isolates tenant records, and recalls previous investigation contexts.',
    status: 'Ready',
    color: 'border-emerald-500/50 bg-emerald-950/20 text-emerald-400'
  },
  {
    id: 'agent_coord',
    name: 'Coordination Agent',
    role: 'Task Leasing, Concurrency Locks & Handoffs',
    desc: 'Prevents duplicate executions via atomic lease locks, manages task dependency states, and logs handoffs.',
    status: 'Ready',
    color: 'border-amber-500/50 bg-amber-950/20 text-amber-400'
  },
  {
    id: 'agent_security',
    name: 'Security Investigation Agent',
    role: 'Anomaly Correlation & Attack Graph Analysis',
    desc: 'Correlates security telemetry events with tickets and projects to identify affected assets and containment actions.',
    status: 'Standby',
    color: 'border-rose-500/50 bg-rose-950/20 text-rose-400'
  },
  {
    id: 'agent_action',
    name: 'Action Agent',
    role: 'Authorized Tool Execution & Audit Stamping',
    desc: 'Executes allowlisted tools under human authorization gates and produces signed, verifiable audit receipts.',
    status: 'Ready',
    color: 'border-indigo-500/50 bg-indigo-950/20 text-indigo-400'
  },
  {
    id: 'agent_quality',
    name: 'Quality & Verification Agent',
    role: 'Factual Grounding & Hallucination Defense',
    desc: 'Audits LLM claims against authoritative FalkorDB nodes and flags unsupported assertions before user delivery.',
    status: 'Ready',
    color: 'border-teal-500/50 bg-teal-950/20 text-teal-400'
  }
];

export function AgentOrchestrationView() {
  const [runs, setRuns] = useState<any[]>([]);
  const [selectedRun, setSelectedRun] = useState<any | null>(null);

  useEffect(() => {
    api.getAgentRuns().then((data) => {
      setRuns(data);
      if (data.length > 0) setSelectedRun(data[0]);
    }).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>Autonomous Agent Orchestration Mesh</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-700">
              Track 02
            </span>
          </h1>
          <p className="text-xs text-slate-400">Specialized agents coordinated by Master Orchestrator with execution traces</p>
        </div>
      </div>

      {/* Agents Mesh Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5">
        {AGENTS.map((agent) => (
          <div
            key={agent.id}
            className={`p-4 rounded-xl border bg-slate-900/60 backdrop-blur-md space-y-2.5 transition-all ${agent.color}`}
          >
            <div className="flex items-center justify-between">
              <span className="font-semibold text-xs text-white flex items-center gap-1.5">
                <Bot className="w-4 h-4" />
                <span>{agent.name}</span>
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-950/80 border border-slate-800 text-emerald-400">
                {agent.status}
              </span>
            </div>
            <div className="text-[10px] font-mono text-cyan-300 font-medium">{agent.role}</div>
            <p className="text-[11px] text-slate-300 leading-relaxed">{agent.desc}</p>
          </div>
        ))}
      </div>

      {/* Handoff & Execution Pipeline Visualizer */}
      <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            <h2 className="text-sm font-semibold text-white">Execution Trace & Agent Handoff Stream</h2>
          </div>
          <span className="text-[10px] font-mono text-slate-400">Active Workflow: Scene 1 Blocker Triage</span>
        </div>

        {/* Steps Timeline */}
        <div className="space-y-3">
          {[
            {
              step: 1,
              agent: 'Master Orchestrator',
              action: 'Classified query intent as Project Blocker Analysis and checked episodic memories.',
              output: 'Found prior investigation record mem_init_01 in memory store.'
            },
            {
              step: 2,
              agent: 'Graph Reasoning Agent',
              action: 'Executed parameterized Cypher traversal: MATCH (p:Project)-[:BLOCKED_BY]->(d:Decision)',
              output: 'Discovered Project Atlas is blocked by AD-104 awaiting approval from Elena Vance.'
            },
            {
              step: 3,
              agent: 'Company Knowledge Agent',
              action: 'Cross-referenced AD-104 against active corporate policy documents.',
              output: 'Flagged conflict: Information Security Policy v2.0 mandates KMS, superseding v1.2.'
            },
            {
              step: 4,
              agent: 'Quality & Verification Agent',
              action: 'Audited factual claims against FalkorDB node attributes and document timestamps.',
              output: '100% of claims verified against ground-truth evidence.'
            }
          ].map((s) => (
            <div key={s.step} className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 space-y-1 text-xs">
              <div className="flex items-center justify-between text-[11px] font-mono">
                <span className="text-cyan-400 font-semibold flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Step {s.step}: {s.agent}</span>
                </span>
                <span className="text-slate-500">Latency: ~8ms</span>
              </div>
              <p className="text-slate-300 font-medium">{s.action}</p>
              <div className="p-2 rounded bg-slate-900 border border-slate-800/60 font-mono text-[10px] text-slate-400">
                <span className="text-purple-400 font-bold">Output:</span> {s.output}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
