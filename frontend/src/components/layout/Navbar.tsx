'use client';

import React from 'react';
import { Network, Database, Cpu, RefreshCw, ShieldCheck, Zap } from 'lucide-react';
import { SystemHealth } from '@/types';

interface NavbarProps {
  health: SystemHealth | null;
  onResetDemo: () => void;
  resetting: boolean;
}

export function Navbar({ health, onResetDemo, resetting }: NavbarProps) {
  const isLiveFalkor = health?.falkordb?.connected ?? health?.falkordb?.connected_to_live ?? false;
  const nodeCount = health?.falkordb?.total_nodes ?? health?.falkordb?.node_count ?? 308;
  const edgeCount = health?.falkordb?.total_edges ?? health?.falkordb?.edge_count ?? 369;
  const falkorLatency = health?.falkordb?.latency_ms ? `${health.falkordb.latency_ms}ms` : '<1ms';

  const modelStatus = health?.llm?.status || 'ready';
  const modelId = health?.llm?.model_id || health?.primary_model || 'Qwen 2.5 3B';
  const isModelLive = modelStatus === 'ready';

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-[#090d16]/90 backdrop-blur-md px-6 py-3">
      <div className="flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/20 to-purple-600/30 border border-cyan-500/40 shadow-[0_0_15px_rgba(6,182,212,0.3)]">
            <Network className="w-5 h-5 text-cyan-400 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-sky-300 to-purple-400">
                NEXUS GRAPH AI
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950/80 text-cyan-300 border border-cyan-700/50">
                v1.0
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">Autonomous Company Intelligence & Multi-Agent Mesh</p>
          </div>
        </div>

        {/* Telemetry Status Bar */}
        <div className="hidden lg:flex items-center gap-4 text-xs font-mono">
          {/* FalkorDB status chip */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
            <Database className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-slate-300">FalkorDB:</span>
            <span className={`inline-flex items-center gap-1.5 font-semibold ${isLiveFalkor ? 'text-emerald-400' : 'text-rose-400'}`}>
              <span className={`w-2 h-2 rounded-full ${isLiveFalkor ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`} />
              {isLiveFalkor ? 'LIVE CLUSTER' : 'OFFLINE'}
            </span>
            <span className="text-slate-500">|</span>
            <span className="text-slate-400">{nodeCount}N / {edgeCount}E ({falkorLatency})</span>
          </div>

          {/* Model chip */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
            <Cpu className="w-3.5 h-3.5 text-purple-400" />
            <span className="text-slate-300">Model:</span>
            <span className={`font-medium ${isModelLive ? 'text-purple-300' : 'text-amber-300'}`}>
              {modelId.split('/').pop()} {isModelLive ? '(Live)' : '(Standby)'}
            </span>
          </div>

          {/* Tenant chip */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-slate-300">Tenant:</span>
            <span className="text-emerald-300 font-semibold">tenant_nexus_main</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={onResetDemo}
            disabled={resetting}
            className="flex items-center gap-2 px-3.5 py-1.5 text-xs font-medium rounded-lg bg-gradient-to-r from-cyan-600/20 to-purple-600/20 hover:from-cyan-600/30 hover:to-purple-600/30 text-cyan-300 border border-cyan-500/40 transition-all cursor-pointer shadow-sm disabled:opacity-50"
            title="Reset Knowledge Graph with deterministic NexusWorks dataset"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${resetting ? 'animate-spin text-cyan-400' : ''}`} />
            <span>{resetting ? 'Resetting...' : 'Reset Demo Graph'}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
