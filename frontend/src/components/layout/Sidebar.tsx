'use client';

import React from 'react';
import {
  LayoutDashboard,
  BrainCircuit,
  Share2,
  Bot,
  Layers,
  CheckSquare,
  ShieldAlert,
  FileUp,
  FileSearch,
  Gauge,
  ClipboardList,
  Settings,
  Sparkles,
  LucideIcon
} from 'lucide-react';

export type ActiveTab =
  | 'overview'
  | 'chat'
  | 'graph'
  | 'agents'
  | 'memory'
  | 'tasks'
  | 'security'
  | 'ingestion'
  | 'sources'
  | 'evaluation'
  | 'audit'
  | 'settings';

interface MenuItem {
  id: string;
  label: string;
  icon: LucideIcon;
  track: string;
  badge?: string;
  count?: number;
}

interface MenuGroup {
  group: string;
  items: MenuItem[];
}

interface SidebarProps {
  activeTab: ActiveTab;
  onSelectTab: (tab: ActiveTab) => void;
  pendingApprovalsCount: number;
}

export function Sidebar({ activeTab, onSelectTab, pendingApprovalsCount }: SidebarProps) {
  const menuGroups: MenuGroup[] = [
    {
      group: 'Core Intelligence',
      items: [
        { id: 'overview', label: 'Overview', icon: LayoutDashboard, track: 'All Tracks' },
        { id: 'chat', label: 'Company Brain', icon: BrainCircuit, track: 'Track 03', badge: 'AI Chat' },
        { id: 'graph', label: 'Graph Explorer', icon: Share2, track: 'Track 01', badge: 'React Flow' }
      ]
    },
    {
      group: 'Multi-Agent Mesh',
      items: [
        { id: 'agents', label: 'Agent Center', icon: Bot, track: 'Track 02' },
        { id: 'memory', label: 'Memory Inspector', icon: Layers, track: 'Track 02' },
        { id: 'tasks', label: 'Tasks & Handoffs', icon: CheckSquare, track: 'Track 02', count: pendingApprovalsCount }
      ]
    },
    {
      group: 'Trust & Investigations',
      items: [
        { id: 'security', label: 'Security Center', icon: ShieldAlert, track: 'Track 01' },
        { id: 'ingestion', label: 'Docs & Ingestion', icon: FileUp, track: 'Track 03' },
        { id: 'sources', label: 'Sources & Provenance', icon: FileSearch, track: 'Track 03' }
      ]
    },
    {
      group: 'Platform & Operations',
      items: [
        { id: 'evaluation', label: 'Evaluation & Benchmarks', icon: Gauge, track: 'Acceptance' },
        { id: 'audit', label: 'Audit Trail', icon: ClipboardList, track: 'Compliance' },
        { id: 'settings', label: 'System & Health', icon: Settings, track: 'Infra' }
      ]
    }
  ];

  return (
    <aside className="w-64 shrink-0 border-r border-slate-800 bg-[#090d16] flex flex-col justify-between py-4 px-3 min-h-[calc(100vh-65px)]">
      <div className="space-y-6">
        {menuGroups.map((group, idx) => (
          <div key={idx} className="space-y-1">
            <h3 className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              {group.group}
            </h3>
            <div className="space-y-1 mt-1">
              {group.items.map((item) => {
                const Icon = item.icon;
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => onSelectTab(item.id as ActiveTab)}
                    className={`w-full flex items-center justify-between px-3 py-2 text-xs font-medium rounded-lg transition-all cursor-pointer ${
                      isActive
                        ? 'bg-gradient-to-r from-cyan-950/80 to-purple-950/50 text-cyan-300 border border-cyan-500/40 shadow-[0_0_12px_rgba(6,182,212,0.15)] font-semibold'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                      <span>{item.label}</span>
                    </div>

                    {item.badge && (
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
                        {item.badge}
                      </span>
                    )}

                    {item.count !== undefined && item.count > 0 && (
                      <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold">
                        {item.count}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Hackathon Track Indicator */}
      <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2 text-xs">
        <div className="flex items-center gap-2 text-cyan-400 font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Hackathon Ready</span>
        </div>
        <p className="text-[11px] text-slate-400 leading-tight">
          Unified Track 01, Track 02 & Track 03 powered by FalkorDB Graph AI.
        </p>
      </div>
    </aside>
  );
}
