'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  Lock,
  Terminal,
  Activity,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  Zap,
  Check
} from 'lucide-react';
import { api } from '@/lib/api';
import { SecurityInvestigationReport } from '@/types';

export function SecurityCenterView() {
  const [report, setReport] = useState<SecurityInvestigationReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [authorized, setAuthorized] = useState(false);

  const runInvestigation = async () => {
    setLoading(true);
    try {
      const data = await api.investigateSecurity('sec_014');
      setReport(data);
    } catch (err: any) {
      console.error('Security investigation failed:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runInvestigation();
  }, []);

  const handleAuthorizeContainment = async () => {
    try {
      await api.createTask({
        title: 'EXECUTE CONTAINMENT: Revoke svc-atlas-worker Token & Quarantine IP',
        description: 'Authorized SecOps containment for SEC-014 / INC-08 anomaly.',
        priority: 'critical',
        assigned_to: 'emp_09',
        project_id: 'proj_atlas'
      });
      setAuthorized(true);
    } catch (err: any) {
      alert(`Authorization failed: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>Security Investigation & Incident Triage Center</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-700">
              Track 01
            </span>
          </h1>
          <p className="text-xs text-slate-400">Multi-hop graph correlation of telemetry anomalies and suspicious activity</p>
        </div>

        <button
          onClick={runInvestigation}
          disabled={loading}
          className="px-3.5 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs transition-all cursor-pointer flex items-center gap-1.5 shadow-md disabled:opacity-50"
        >
          <Activity className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>{loading ? 'Correlating...' : 'Re-Run Graph Correlation'}</span>
        </button>
      </div>

      {/* Incident Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-rose-950/40 via-slate-900 to-slate-950 border border-rose-500/50 shadow-xl space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="p-2 rounded-xl bg-rose-900/60 border border-rose-600 text-rose-300">
              <ShieldAlert className="w-5 h-5 text-rose-400 animate-pulse" />
            </span>
            <div>
              <div className="text-[11px] font-mono text-rose-400 font-bold uppercase tracking-wider">
                ACTIVE P1 INCIDENT: INC-08
              </div>
              <h2 className="text-lg font-bold text-white">
                Suspicious Service Account Token Escalation on Project Atlas
              </h2>
            </div>
          </div>
          <span className="text-xs font-mono font-bold px-3 py-1 rounded-full bg-rose-950 text-rose-300 border border-rose-600 shadow-[0_0_15px_rgba(244,63,94,0.3)]">
            CRITICAL RISK (CVSS 9.2)
          </span>
        </div>
      </div>

      {/* Correlation Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Evidence Chain & Relationships */}
        <div className="lg:col-span-2 space-y-4">
          <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-3">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Terminal className="w-4 h-4 text-cyan-400" />
              <span>FalkorDB Multi-Hop Attack Graph Traversal</span>
            </h3>

            {report && (
              <div className="space-y-2">
                {report.evidence_chain.map((chain, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-slate-300 flex items-center gap-2"
                  >
                    <span className="text-cyan-400 font-bold">{i + 1}.</span>
                    <span>{chain}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Connected Entities */}
          {report && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Affected Project</span>
                <div className="text-sm font-bold text-white mt-1">Project Atlas</div>
                <span className="text-[10px] text-cyan-400 font-mono">proj_atlas</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Related Ticket</span>
                <div className="text-sm font-bold text-white mt-1">TIK-204 (Token Anomaly)</div>
                <span className="text-[10px] text-amber-400 font-mono">Status: Open</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-[10px] font-mono text-slate-400 uppercase">Assigned Responder</span>
                <div className="text-sm font-bold text-white mt-1">Zack Brody</div>
                <span className="text-[10px] text-emerald-400 font-mono">SecOps Incident Handler</span>
              </div>
            </div>
          )}
        </div>

        {/* Right Col: Containment Plan & Approval Gate */}
        <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-800 flex flex-col justify-between space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <span className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5 text-purple-400" />
                <span>Containment Playbook</span>
              </span>
              <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-700">
                PB-SEC-01
              </span>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              Recommended actions generated by Security Investigation Agent:
            </p>

            <ul className="space-y-2 text-xs">
              {[
                'Immediately revoke internal token for worker svc-atlas-worker',
                'Quarantine rogue IP 10.0.4.152 on internal VPC gateway',
                'Rotate Atlas worker IAM credentials in Secrets Manager',
                'Assign critical triage task to Zack Brody'
              ].map((step, idx) => (
                <li key={idx} className="flex items-start gap-2 p-2 rounded-lg bg-slate-950 border border-slate-800/80">
                  <CheckCircle2 className="w-3.5 h-3.5 text-rose-400 shrink-0 mt-0.5" />
                  <span className="text-slate-300 text-[11px]">{step}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Action Approval Gate */}
          <div className="pt-3 border-t border-slate-800 space-y-2">
            <div className="text-[11px] text-amber-300 font-mono flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
              <span>Requires Explicit Human Authorization</span>
            </div>
            <button
              onClick={handleAuthorizeContainment}
              disabled={authorized}
              className={`w-full py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center justify-center gap-2 ${
                authorized
                  ? 'bg-emerald-950 text-emerald-300 border border-emerald-600'
                  : 'bg-rose-600 hover:bg-rose-500 text-white shadow-[0_0_15px_rgba(244,63,94,0.4)]'
              }`}
            >
              {authorized ? (
                <>
                  <Check className="w-4 h-4 text-emerald-400" />
                  <span>Containment Plan Authorized</span>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-4 h-4" />
                  <span>Authorize & Execute Containment</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
