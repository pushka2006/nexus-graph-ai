'use client';

import React, { useState, useEffect } from 'react';
import { ClipboardList, ShieldCheck, Filter, Search, Terminal, CheckCircle2, Clock } from 'lucide-react';
import { api } from '@/lib/api';
import { AuditLogEntry } from '@/types';

export function AuditLogView() {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [filterType, setFilterType] = useState('all');
  const [search, setSearch] = useState('');
  const [selectedLog, setSelectedLog] = useState<AuditLogEntry | null>(null);

  useEffect(() => {
    api.getAuditLogs().then(setLogs).catch(console.error);
  }, []);

  const filteredLogs = logs.filter((l) => {
    if (filterType !== 'all' && l.actor_type !== filterType) return false;
    if (search && !JSON.stringify(l).toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>Tamper-Evident Immutable Audit Log</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-700">
              Compliance Ready
            </span>
          </h1>
          <p className="text-xs text-slate-400">Chronological verification of agent actions, user approvals, and tool executions</p>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <Search className="w-3.5 h-3.5 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search audit trail..."
            className="px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 w-56"
          />
        </div>

        <div className="flex items-center gap-1.5">
          <span className="text-slate-500 font-mono text-[11px]">Actor:</span>
          {['all', 'user', 'agent', 'system'].map((t) => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`px-3 py-1 rounded-md text-[11px] font-medium cursor-pointer transition-all ${
                filterType === t
                  ? 'bg-cyan-950 text-cyan-300 border border-cyan-500/60 font-semibold'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {t.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-3">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
              <tr>
                <th className="p-3">Audit ID</th>
                <th className="p-3">Timestamp</th>
                <th className="p-3">Actor</th>
                <th className="p-3">Type</th>
                <th className="p-3">Action</th>
                <th className="p-3">Target Resource</th>
                <th className="p-3">Status</th>
                <th className="p-3">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80 font-mono text-[11px]">
              {filteredLogs.map((l) => (
                <tr key={l.id} className="hover:bg-slate-800/40 cursor-pointer" onClick={() => setSelectedLog(l)}>
                  <td className="p-3 text-cyan-400 font-bold">{l.id}</td>
                  <td className="p-3 text-slate-400">{l.timestamp?.slice(11, 19) || '10:45:00'}</td>
                  <td className="p-3 text-white font-sans font-medium">{l.actor}</td>
                  <td className="p-3">
                    <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">
                      {l.actor_type}
                    </span>
                  </td>
                  <td className="p-3 text-purple-300 font-bold">{l.action}</td>
                  <td className="p-3 text-slate-400">{l.target_resource}</td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        l.status === 'executed' || l.status === 'authorized'
                          ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                          : 'bg-amber-950 text-amber-300 border border-amber-800'
                      }`}
                    >
                      {l.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-3 text-slate-500 underline text-[10px]">Inspect</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Log Parameter Drawer Modal */}
      {selectedLog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <Terminal className="w-4 h-4 text-cyan-400" />
                <span>Audit Receipt: {selectedLog.id}</span>
              </h2>
              <button
                onClick={() => setSelectedLog(null)}
                className="text-slate-400 hover:text-white text-xs cursor-pointer"
              >
                ✕ Close
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-2 font-mono text-[11px]">
                <div className="p-2 rounded bg-slate-950 border border-slate-800">
                  <span className="text-slate-500">Actor:</span> <span className="text-white">{selectedLog.actor}</span>
                </div>
                <div className="p-2 rounded bg-slate-950 border border-slate-800">
                  <span className="text-slate-500">Action:</span> <span className="text-purple-300">{selectedLog.action}</span>
                </div>
              </div>

              <div>
                <span className="text-slate-400 block mb-1 font-mono text-[11px]">Parameters:</span>
                <pre className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-slate-200 overflow-x-auto max-h-48">
                  {JSON.stringify(selectedLog.parameters, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
