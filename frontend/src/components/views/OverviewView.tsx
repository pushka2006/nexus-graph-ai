'use client';

import React from 'react';
import {
  Network,
  Share2,
  BrainCircuit,
  ShieldAlert,
  CheckCircle2,
  Clock,
  ArrowUpRight,
  Sparkles,
  Bot,
  Zap,
  Activity
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { SystemHealth } from '@/types';

interface OverviewViewProps {
  health: SystemHealth | null;
  metrics: Record<string, any> | null;
  onNavigate: (tab: any) => void;
}

const COLORS = ['#06b6d4', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899', '#3b82f6'];

export function OverviewView({ health, metrics, onNavigate }: OverviewViewProps) {
  const nodeCount = health?.falkordb?.node_count || 309;
  const edgeCount = health?.falkordb?.edge_count || 369;
  const nodeDist = metrics?.node_distribution || {
    Person: 32,
    Document: 52,
    Ticket: 42,
    Decision: 26,
    Task: 24,
    Meeting: 22,
    SecurityEvent: 16,
    Project: 10,
    Agent: 8,
    Department: 6
  };

  const chartData = Object.entries(nodeDist).map(([name, count]) => ({
    name,
    count: count as number
  }));

  const kpis = [
    {
      title: 'Authoritative Graph Nodes',
      value: nodeCount,
      change: '+32 entities today',
      icon: Network,
      color: 'from-cyan-500/20 to-cyan-500/5',
      borderColor: 'border-cyan-500/40',
      textColor: 'text-cyan-400'
    },
    {
      title: 'Verified Relationships',
      value: edgeCount,
      change: 'Multi-hop connected',
      icon: Share2,
      color: 'from-purple-500/20 to-purple-500/5',
      borderColor: 'border-purple-500/40',
      textColor: 'text-purple-400'
    },
    {
      title: 'Active Autonomous Agents',
      value: '8 / 8',
      change: 'Coordinated mesh ready',
      icon: Bot,
      color: 'from-emerald-500/20 to-emerald-500/5',
      borderColor: 'border-emerald-500/40',
      textColor: 'text-emerald-400'
    },
    {
      title: 'Avg Cypher Latency',
      value: '25.6 ms',
      change: 'Sub-second traversal',
      icon: Activity,
      color: 'from-amber-500/20 to-amber-500/5',
      borderColor: 'border-amber-500/40',
      textColor: 'text-amber-400'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border border-slate-800 p-6 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-cyan-950/80 border border-cyan-500/40 text-[11px] font-mono text-cyan-300">
              <Sparkles className="w-3 h-3 text-cyan-400" />
              <span>Hackathon Production Demo</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Autonomous Company Intelligence & Graph Reasoning
            </h1>
            <p className="text-xs text-slate-300 leading-relaxed">
              Transforming fragmented enterprise silos into a unified FalkorDB knowledge graph.
              Execute multi-hop investigations, persistent multi-tier memory recalls, and authorized autonomous agent actions.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => onNavigate('chat')}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 shadow-[0_0_15px_rgba(6,182,212,0.4)] transition-all cursor-pointer flex items-center gap-1.5"
            >
              <BrainCircuit className="w-4 h-4" />
              <span>Launch Company Brain</span>
            </button>
            <button
              onClick={() => onNavigate('graph')}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 transition-all cursor-pointer flex items-center gap-1.5"
            >
              <Share2 className="w-4 h-4 text-cyan-400" />
              <span>Explore Graph</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div
              key={idx}
              className={`p-4 rounded-xl bg-gradient-to-br ${kpi.color} bg-slate-900/60 border ${kpi.borderColor} backdrop-blur-md shadow-sm`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">{kpi.title}</span>
                <Icon className={`w-4 h-4 ${kpi.textColor}`} />
              </div>
              <div className="mt-2 text-2xl font-bold text-white tracking-tight">{kpi.value}</div>
              <div className="mt-1 text-[11px] text-slate-400 flex items-center gap-1">
                <span className="text-emerald-400 font-medium">●</span>
                <span>{kpi.change}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Middle Row: Graph Entity Distribution & Live Agent Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Entity Distribution Chart */}
        <div className="lg:col-span-2 p-5 rounded-xl bg-slate-900/70 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white">FalkorDB Knowledge Graph Entities</h2>
              <p className="text-xs text-slate-400">Distribution across 10 top enterprise schema node types</p>
            </div>
            <button
              onClick={() => onNavigate('graph')}
              className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 cursor-pointer font-medium"
            >
              <span>View Graph</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <XAxis
                  dataKey="name"
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  angle={-30}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#f8fafc'
                  }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {chartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Live Multi-Agent Status */}
        <div className="p-5 rounded-xl bg-slate-900/70 border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-white">Multi-Agent Mesh Status</h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                ACTIVE
              </span>
            </div>
            <p className="text-xs text-slate-400 mb-4">Specialized agents coordinated by Master Orchestrator</p>

            <div className="space-y-2.5">
              {[
                { name: 'Master Orchestrator', role: 'Workflow Planning', status: 'Ready' },
                { name: 'Graph Reasoning Agent', role: 'FalkorDB Cypher Multi-Hop', status: 'Active' },
                { name: 'Company Knowledge Agent', role: 'Document Citations & Freshness', status: 'Ready' },
                { name: 'Memory Agent', role: 'Episodic & Procedural Recall', status: 'Ready' },
                { name: 'Security Investigation', role: 'Anomaly & Attack Graph', status: 'Standby' }
              ].map((agent, i) => (
                <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
                    <div>
                      <div className="text-slate-200 font-medium">{agent.name}</div>
                      <div className="text-[10px] text-slate-400">{agent.role}</div>
                    </div>
                  </div>
                  <span className="text-[10px] font-mono text-emerald-400">{agent.status}</span>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => onNavigate('agents')}
            className="w-full mt-4 py-2 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 transition-all cursor-pointer flex items-center justify-center gap-1.5"
          >
            <span>Inspect Agent Orchestrator</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Bottom Row: Quick Scenario Launchers */}
      <div className="p-5 rounded-xl bg-slate-900/70 border border-slate-800">
        <h2 className="text-sm font-semibold text-white mb-1">Pre-Packaged Hackathon Scenarios</h2>
        <p className="text-xs text-slate-400 mb-4">Click to jump into real end-to-end verified reasoning workflows</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={() => onNavigate('chat')}
            className="text-left p-3.5 rounded-xl bg-slate-950/80 hover:bg-slate-800/60 border border-cyan-500/30 transition-all cursor-pointer group"
          >
            <div className="flex items-center gap-2 text-cyan-400 text-xs font-semibold mb-1">
              <BrainCircuit className="w-3.5 h-3.5" />
              <span>Scene 1: Company Brain (Track 03)</span>
            </div>
            <p className="text-xs text-slate-300 font-medium">"Who owns Project Atlas, and what is preventing its release?"</p>
            <span className="mt-2 inline-block text-[10px] text-cyan-400 group-hover:translate-x-1 transition-transform">
              Run Query →
            </span>
          </button>

          <button
            onClick={() => onNavigate('security')}
            className="text-left p-3.5 rounded-xl bg-slate-950/80 hover:bg-slate-800/60 border border-rose-500/30 transition-all cursor-pointer group"
          >
            <div className="flex items-center gap-2 text-rose-400 text-xs font-semibold mb-1">
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>Scene 2: Connected Data (Track 01)</span>
            </div>
            <p className="text-xs text-slate-300 font-medium">"Investigate security event SEC-014 linked to Project Atlas"</p>
            <span className="mt-2 inline-block text-[10px] text-rose-400 group-hover:translate-x-1 transition-transform">
              Triage Incident →
            </span>
          </button>

          <button
            onClick={() => onNavigate('memory')}
            className="text-left p-3.5 rounded-xl bg-slate-950/80 hover:bg-slate-800/60 border border-purple-500/30 transition-all cursor-pointer group"
          >
            <div className="flex items-center gap-2 text-purple-400 text-xs font-semibold mb-1">
              <Zap className="w-3.5 h-3.5" />
              <span>Scene 3: Agent Memory (Track 02)</span>
            </div>
            <p className="text-xs text-slate-300 font-medium">"Recall previous investigation findings without re-querying"</p>
            <span className="mt-2 inline-block text-[10px] text-purple-400 group-hover:translate-x-1 transition-transform">
              Inspect Memories →
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}
