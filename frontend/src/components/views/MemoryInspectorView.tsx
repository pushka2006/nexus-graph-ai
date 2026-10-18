'use client';

import React, { useState, useEffect } from 'react';
import { Layers, Search, Plus, ShieldCheck, Zap, BookOpen, Clock, Tag, ExternalLink } from 'lucide-react';
import { api } from '@/lib/api';
import { MemoryItem } from '@/types';

export function MemoryInspectorView() {
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [selectedType, setSelectedType] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form states
  const [newSummary, setNewSummary] = useState('');
  const [newType, setNewType] = useState<'episodic' | 'semantic' | 'procedural'>('semantic');
  const [newDetails, setNewDetails] = useState('');

  const loadMemories = async () => {
    setLoading(true);
    try {
      const data = await api.searchMemories(
        searchQuery,
        selectedType === 'all' ? undefined : selectedType
      );
      setMemories(data);
    } catch (err: any) {
      console.error('Failed to load memories:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMemories();
  }, [selectedType, searchQuery]);

  const handleAddMemory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSummary.trim()) return;
    try {
      await api.createMemory({
        summary: newSummary,
        memory_type: newType,
        details: { note: newDetails },
        confidence: 1.0,
        tenant_id: 'tenant_nexus_main',
        verified: true
      });
      setShowAddModal(false);
      setNewSummary('');
      setNewDetails('');
      loadMemories();
    } catch (err: any) {
      alert(`Failed to save memory: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>Persistent Agent Memory Inspector</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-700">
              Track 02
            </span>
          </h1>
          <p className="text-xs text-slate-400">Episodic, Semantic, and Procedural memory tiers with tenant isolation</p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 text-slate-950 font-semibold text-xs transition-all cursor-pointer flex items-center gap-1.5 shadow-sm"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Record Memory</span>
        </button>
      </div>

      {/* Controls Bar */}
      <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search persistent memories..."
              className="pl-8 pr-3 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 w-56"
            />
          </div>
        </div>

        {/* Tiers Tabs */}
        <div className="flex items-center gap-1.5">
          <span className="text-slate-500 font-mono text-[11px]">Tiers:</span>
          {['all', 'episodic', 'semantic', 'procedural'].map((t) => (
            <button
              key={t}
              onClick={() => setSelectedType(t)}
              className={`px-3 py-1 rounded-md text-[11px] font-medium cursor-pointer transition-all ${
                selectedType === t
                  ? 'bg-purple-950 text-purple-300 border border-purple-500/60 font-semibold'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {t.toUpperCase()}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 text-xs font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/60 px-3 py-1 rounded-lg">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Tenant Scope: tenant_nexus_main</span>
        </div>
      </div>

      {/* Memories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {memories.map((m) => {
          const typeBadge =
            m.memory_type === 'episodic'
              ? 'bg-cyan-950 text-cyan-300 border-cyan-800'
              : m.memory_type === 'semantic'
              ? 'bg-purple-950 text-purple-300 border-purple-800'
              : 'bg-emerald-950 text-emerald-300 border-emerald-800';

          return (
            <div
              key={m.id}
              className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition-all space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded border uppercase font-semibold ${typeBadge}`}>
                  {m.memory_type}
                </span>
                <span className="text-[10px] font-mono text-emerald-400">
                  Confidence: {(m.confidence * 100).toFixed(0)}%
                </span>
              </div>

              <div>
                <h3 className="font-semibold text-xs text-white leading-snug">{m.summary}</h3>
                <span className="text-[10px] font-mono text-slate-500">ID: {m.id}</span>
              </div>

              {/* Details JSON */}
              <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/80 font-mono text-[11px] text-slate-300 space-y-1">
                {Object.entries(m.details || {}).map(([k, v]) => (
                  <div key={k} className="truncate">
                    <span className="text-slate-500">{k}:</span>{' '}
                    <span className="text-slate-200">{typeof v === 'object' ? JSON.stringify(v) : String(v)}</span>
                  </div>
                ))}
              </div>

              {/* Related entities */}
              {m.related_entities && m.related_entities.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {m.related_entities.map((tag, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono"
                    >
                      <Tag className="w-2.5 h-2.5 text-cyan-400" />
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                <span>Access Count: {m.access_count}</span>
                <span>Source: {m.source_ref || 'Graph Ingest'}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Add Memory Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <form
            onSubmit={handleAddMemory}
            className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-cyan-400" />
                <span>Record New Knowledge Memory</span>
              </h2>
              <button
                type="button"
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-white text-xs cursor-pointer"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="text-slate-400 block mb-1">Memory Tier</label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value as any)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
                >
                  <option value="semantic">Semantic (Verified Business Fact)</option>
                  <option value="episodic">Episodic (Task or Investigation Trace)</option>
                  <option value="procedural">Procedural (Investigation Playbook)</option>
                </select>
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Summary / Title</label>
                <input
                  type="text"
                  value={newSummary}
                  onChange={(e) => setNewSummary(e.target.value)}
                  placeholder="e.g. S3 KMS encryption policy sign-off owner"
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
                  required
                />
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Details / Findings</label>
                <textarea
                  value={newDetails}
                  onChange={(e) => setNewDetails(e.target.value)}
                  rows={3}
                  placeholder="Detailed context recorded for other agents..."
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 rounded-lg text-xs text-slate-300 hover:bg-slate-800 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-semibold text-xs cursor-pointer"
              >
                Save Memory
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
