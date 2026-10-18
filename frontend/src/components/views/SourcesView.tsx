'use client';

import React, { useState, useEffect } from 'react';
import { FileSearch, Hash, ShieldCheck, AlertTriangle, ArrowRight, ExternalLink } from 'lucide-react';
import { api } from '@/lib/api';

export function SourcesView() {
  const [conflicts, setConflicts] = useState<any[]>([]);

  useEffect(() => {
    api.getConflicts().then(setConflicts).catch(console.error);
  }, []);

  const sampleSources = [
    {
      id: 'src_doc_sec_pol_v20',
      name: 'Information Security Policy v2.0 (Mandatory Cloud Encryption).pdf',
      uri: 's3://nexusworks-docs/doc_sec_pol_v20.pdf',
      hash: '3e4f7a19c8d50b2e',
      date: '2026-09-01',
      status: 'Current'
    },
    {
      id: 'src_doc_sec_pol_v12',
      name: 'Information Security Policy v1.2.pdf',
      uri: 's3://nexusworks-docs/doc_sec_pol_v12.pdf',
      hash: '8f2a1b94c0e37d51',
      date: '2024-06-15',
      status: 'Superseded'
    },
    {
      id: 'src_doc_atlas_prd',
      name: 'Project Atlas Product Requirements Document (PRD v3.1).pdf',
      uri: 's3://nexusworks-docs/doc_atlas_prd.pdf',
      hash: 'b1c7849e02d8f5aa',
      date: '2026-09-20',
      status: 'Current'
    },
    {
      id: 'src_doc_incident_runbook',
      name: 'SecOps Incident Response Runbook P1/P2.pdf',
      uri: 's3://nexusworks-docs/doc_incident_runbook.pdf',
      hash: 'fa56d819c4e0b329',
      date: '2026-08-10',
      status: 'Current'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>Sources & Evidence Provenance Explorer</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-700">
              Track 03
            </span>
          </h1>
          <p className="text-xs text-slate-400">Cryptographic hashes, timestamps, and policy supersession reconciliation</p>
        </div>
      </div>

      {/* Supersession Conflicts Callout */}
      {conflicts.length > 0 && (
        <div className="p-5 rounded-2xl bg-amber-950/40 border border-amber-500/40 space-y-3">
          <div className="flex items-center gap-2 text-amber-300 text-sm font-semibold">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>Document Supersession Conflict Flagged in Graph</span>
          </div>

          {conflicts.map((c, i) => (
            <div key={i} className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center gap-2 font-mono text-[11px]">
                <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                  ACTIVE: {c.active_document?.label}
                </span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
                <span className="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                  SUPERSEDES: {c.superseded_document?.label}
                </span>
              </div>
              <p className="text-slate-300 font-medium">{c.conflict_detail}</p>
              <div className="text-[11px] text-slate-400 font-mono">
                Rationale: {c.rationale}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Provenance Table */}
      <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-3">
        <h3 className="text-sm font-semibold text-white">Immutable Provenance Hashes & Source URIs</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
              <tr>
                <th className="p-3">Source Name</th>
                <th className="p-3">URI</th>
                <th className="p-3">SHA-256 Hash</th>
                <th className="p-3">Ingested At</th>
                <th className="p-3">Freshness</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {sampleSources.map((s) => (
                <tr key={s.id} className="hover:bg-slate-800/40">
                  <td className="p-3 font-semibold text-white">{s.name}</td>
                  <td className="p-3 font-mono text-[11px] text-cyan-400">{s.uri}</td>
                  <td className="p-3 font-mono text-[11px] text-purple-400">{s.hash}</td>
                  <td className="p-3 font-mono text-[11px] text-slate-400">{s.date}</td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        s.status === 'Current'
                          ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                          : 'bg-rose-950 text-rose-300 border border-rose-800'
                      }`}
                    >
                      {s.status.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
