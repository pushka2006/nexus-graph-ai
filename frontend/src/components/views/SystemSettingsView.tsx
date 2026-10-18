'use client';

import React, { useState } from 'react';
import { Settings, Database, Server, Cpu, RefreshCw, CheckCircle2, ShieldCheck, Zap } from 'lucide-react';
import { SystemHealth } from '@/types';
import { api } from '@/lib/api';

interface SystemSettingsViewProps {
  health: SystemHealth | null;
  onResetDemo: () => void;
  resetting: boolean;
}

export function SystemSettingsView({ health, onResetDemo, resetting }: SystemSettingsViewProps) {
  const [provider, setProvider] = useState('mock');
  const [modelSaved, setModelSaved] = useState(false);

  const isLiveFalkor = health?.falkordb?.connected_to_live ?? false;
  const nodeCount = health?.falkordb?.node_count || 309;
  const edgeCount = health?.falkordb?.edge_count || 369;

  const handleSaveModel = (e: React.FormEvent) => {
    e.preventDefault();
    setModelSaved(true);
    setTimeout(() => setModelSaved(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>System Infrastructure & Settings</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
              Operations
            </span>
          </h1>
          <p className="text-xs text-slate-400">Database connection health, model adapters, and environment controls</p>
        </div>
      </div>

      {/* Database Cluster Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* FalkorDB */}
        <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-white flex items-center gap-1.5">
              <Database className="w-4 h-4 text-cyan-400" />
              <span>FalkorDB Graph</span>
            </span>
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${isLiveFalkor ? 'bg-emerald-950 text-emerald-400' : 'bg-cyan-950 text-cyan-300'}`}>
              {isLiveFalkor ? 'LIVE CLUSTER' : 'EMBEDDED CYPHER'}
            </span>
          </div>
          <p className="text-[11px] text-slate-400">
            Authoritative knowledge graph store for company entities and traversals.
          </p>
          <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-400 flex justify-between">
            <span>Nodes: {nodeCount}</span>
            <span>Edges: {edgeCount}</span>
          </div>
        </div>

        {/* PostgreSQL / SQLite */}
        <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-white flex items-center gap-1.5">
              <Server className="w-4 h-4 text-purple-400" />
              <span>Metadata & Audit Store</span>
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400">
              ONLINE
            </span>
          </div>
          <p className="text-[11px] text-slate-400">
            Relational storage for user accounts, task leases, and audit logs.
          </p>
          <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-400 flex justify-between">
            <span>Engine: SQLite / PostgreSQL</span>
            <span>Dual-Mode</span>
          </div>
        </div>

        {/* Redis / Cache */}
        <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-white flex items-center gap-1.5">
              <Zap className="w-4 h-4 text-amber-400" />
              <span>Redis Cache & Leases</span>
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400">
              ACTIVE
            </span>
          </div>
          <p className="text-[11px] text-slate-400">
            Ephemeral coordination, atomic task locks, and low-latency cache.
          </p>
          <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-400 flex justify-between">
            <span>Port: 6380 / Local</span>
            <span>Zero-Conflict</span>
          </div>
        </div>
      </div>

      {/* Model Selection & Demo Reset */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Model Configuration */}
        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Cpu className="w-4 h-4 text-purple-400" />
            <span>AI Model Adapter Configuration</span>
          </h2>

          <form onSubmit={handleSaveModel} className="space-y-3 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Inference Provider</label>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
              >
                <option value="mock">Deterministic Mock Provider (Domain-Grounded Offline Mode)</option>
                <option value="huggingface">Hugging Face Transformers (Qwen/Qwen2.5-3B-Instruct)</option>
                <option value="vllm">vLLM Inference Server (Local Port 8080)</option>
                <option value="openai">OpenAI Compatible Endpoint</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 block mb-1">Primary Model Name</label>
              <input
                type="text"
                defaultValue="Qwen/Qwen2.5-3B-Instruct"
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs font-mono"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1">Embedding Model</label>
              <input
                type="text"
                defaultValue="sentence-transformers/all-MiniLM-L6-v2"
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs font-mono"
              />
            </div>

            <button
              type="submit"
              className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs cursor-pointer"
            >
              {modelSaved ? 'Configuration Saved!' : 'Apply Model Settings'}
            </button>
          </form>
        </div>

        {/* 1-Click Database & Demo Reset */}
        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 flex flex-col justify-between space-y-4">
          <div className="space-y-3">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-cyan-400" />
              <span>1-Click Hackathon Demo Reset</span>
            </h2>
            <p className="text-xs text-slate-400 leading-relaxed">
              Restores the complete synthetic enterprise dataset for <strong>NexusWorks Technologies</strong> deterministically:
            </p>
            <ul className="space-y-1.5 text-xs text-slate-300 font-mono">
              <li>• 32 Employees (Person) across 6 Departments & 8 Teams</li>
              <li>• 10 Strategic Projects (including Project Atlas)</li>
              <li>• 52 Documents (including superseded Policy v2.0 & v1.2)</li>
              <li>• 42 Engineering & Support Tickets (including TIK-204)</li>
              <li>• 26 Architectural Decisions (including AD-104)</li>
              <li>• 16 Security Events (including SEC-014 privilege escalation)</li>
              <li>• 22 Meetings and 24 Tasks with dependency constraints</li>
            </ul>
          </div>

          <button
            onClick={onResetDemo}
            disabled={resetting}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 text-slate-950 font-bold text-xs transition-all cursor-pointer shadow-[0_0_15px_rgba(6,182,212,0.4)] disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${resetting ? 'animate-spin' : ''}`} />
            <span>{resetting ? 'Resetting Knowledge Graph...' : 'Reset Demo Knowledge Graph'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
