'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { Sidebar, ActiveTab } from '@/components/layout/Sidebar';
import { OverviewView } from '@/components/views/OverviewView';
import { CompanyBrainView } from '@/components/views/CompanyBrainView';
import { KnowledgeGraphView } from '@/components/views/KnowledgeGraphView';
import { AgentOrchestrationView } from '@/components/views/AgentOrchestrationView';
import { MemoryInspectorView } from '@/components/views/MemoryInspectorView';
import { TaskBoardView } from '@/components/views/TaskBoardView';
import { SecurityCenterView } from '@/components/views/SecurityCenterView';
import { IngestionCenterView } from '@/components/views/IngestionCenterView';
import { SourcesView } from '@/components/views/SourcesView';
import { EvaluationView } from '@/components/views/EvaluationView';
import { AuditLogView } from '@/components/views/AuditLogView';
import { SystemSettingsView } from '@/components/views/SystemSettingsView';
import { api } from '@/lib/api';
import { SystemHealth } from '@/types';

export default function Home() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('overview');
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [metrics, setMetrics] = useState<Record<string, any> | null>(null);
  const [pendingApprovalsCount, setPendingApprovalsCount] = useState<number>(0);
  const [resetting, setResetting] = useState(false);

  const refreshTelemetry = async () => {
    try {
      const h = await api.getHealth();
      setHealth(h);
      const m = await api.getMetrics();
      setMetrics(m);
      if (m?.pending_approvals) {
        setPendingApprovalsCount(m.pending_approvals);
      }
    } catch (err) {
      console.warn('API health check error (backend may still be starting):', err);
    }
  };

  useEffect(() => {
    refreshTelemetry();
    const interval = setInterval(refreshTelemetry, 8000);
    return () => clearInterval(interval);
  }, []);

  const handleResetDemo = async () => {
    setResetting(true);
    try {
      await api.resetGraph();
      await refreshTelemetry();
      alert('Knowledge graph successfully reset with 309 nodes and 369 relationships!');
    } catch (err: any) {
      alert(`Reset error: ${err.message}`);
    } finally {
      setResetting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      <Navbar health={health} onResetDemo={handleResetDemo} resetting={resetting} />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          activeTab={activeTab}
          onSelectTab={setActiveTab}
          pendingApprovalsCount={pendingApprovalsCount}
        />

        <main className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-[#090d16] via-[#080c14] to-[#080c14]">
          {activeTab === 'overview' && (
            <OverviewView health={health} metrics={metrics} onNavigate={setActiveTab} />
          )}
          {activeTab === 'chat' && <CompanyBrainView />}
          {activeTab === 'graph' && <KnowledgeGraphView />}
          {activeTab === 'agents' && <AgentOrchestrationView />}
          {activeTab === 'memory' && <MemoryInspectorView />}
          {activeTab === 'tasks' && <TaskBoardView />}
          {activeTab === 'security' && <SecurityCenterView />}
          {activeTab === 'ingestion' && <IngestionCenterView />}
          {activeTab === 'sources' && <SourcesView />}
          {activeTab === 'evaluation' && <EvaluationView />}
          {activeTab === 'audit' && <AuditLogView />}
          {activeTab === 'settings' && (
            <SystemSettingsView health={health} onResetDemo={handleResetDemo} resetting={resetting} />
          )}
        </main>
      </div>
    </div>
  );
}
