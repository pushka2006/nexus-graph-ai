'use client';

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  MarkerType
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import {
  Search,
  Filter,
  Maximize2,
  Share2,
  Layers,
  ArrowRight,
  ShieldAlert,
  FileText,
  User,
  Briefcase,
  AlertCircle,
  CheckCircle,
  HelpCircle,
  Sparkles
} from 'lucide-react';
import { api } from '@/lib/api';
import { GraphNodeData } from '@/types';

const NODE_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  Person: { bg: 'rgba(6, 182, 212, 0.15)', border: '#06b6d4', text: '#22d3ee' },
  Project: { bg: 'rgba(99, 102, 241, 0.2)', border: '#6366f1', text: '#818cf8' },
  Document: { bg: 'rgba(59, 130, 246, 0.15)', border: '#3b82f6', text: '#60a5fa' },
  Ticket: { bg: 'rgba(245, 158, 11, 0.15)', border: '#f59e0b', text: '#fbbf24' },
  Decision: { bg: 'rgba(139, 92, 246, 0.2)', border: '#8b5cf6', text: '#a78bfa' },
  SecurityEvent: { bg: 'rgba(244, 63, 94, 0.2)', border: '#f43f5e', text: '#fb7185' },
  Incident: { bg: 'rgba(239, 68, 68, 0.25)', border: '#ef4444', text: '#f87171' },
  Task: { bg: 'rgba(16, 185, 129, 0.15)', border: '#10b981', text: '#34d399' },
  Department: { bg: 'rgba(14, 165, 233, 0.15)', border: '#0ea5e9', text: '#38bdf8' },
  Team: { bg: 'rgba(168, 85, 247, 0.15)', border: '#a855f7', text: '#c084fc' }
};

export function KnowledgeGraphView() {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [selectedNode, setSelectedNode] = useState<GraphNodeData | null>(null);
  const [depth, setDepth] = useState<number>(1);
  const [pathSource, setPathSource] = useState('sec_014');
  const [pathTarget, setPathTarget] = useState('proj_atlas');
  const [pathResults, setPathResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Load initial neighborhood around Project Atlas
  const loadNeighborhood = useCallback(async (centerId: string, d = 1) => {
    setLoading(true);
    try {
      const data = await api.getNeighbors(centerId, d);
      const angleStep = (2 * Math.PI) / (data.nodes.length || 1);
      const radius = d === 1 ? 220 : 380;

      const flowNodes: Node[] = data.nodes.map((n, idx) => {
        const isCenter = n.id === centerId;
        const color = NODE_COLORS[n.type] || { bg: 'rgba(51, 65, 85, 0.5)', border: '#64748b', text: '#94a3b8' };
        const x = isCenter ? 400 : 400 + radius * Math.cos(idx * angleStep);
        const y = isCenter ? 300 : 300 + radius * Math.sin(idx * angleStep);

        return {
          id: n.id,
          position: { x, y },
          data: {
            label: (
              <div className="p-2 space-y-1">
                <div className="flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-wider text-slate-400">
                  <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: color.border }} />
                  <span>{n.type}</span>
                </div>
                <div className="font-semibold text-xs text-white truncate max-w-[150px]">{n.label}</div>
              </div>
            ),
            raw: n
          },
          style: {
            background: color.bg,
            border: `1px solid ${color.border}`,
            borderRadius: '12px',
            boxShadow: isCenter ? `0 0 20px ${color.border}66` : '0 4px 12px rgba(0,0,0,0.5)',
            width: 170,
            cursor: 'pointer'
          }
        };
      });

      const flowEdges: Edge[] = data.edges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.type,
        labelStyle: { fill: '#94a3b8', fontSize: 10, fontFamily: 'monospace' },
        labelBgStyle: { fill: '#0f172a', fillOpacity: 0.8 },
        labelBgPadding: [4, 2],
        labelBgBorderRadius: 4,
        animated: e.type === 'BLOCKED_BY' || e.type === 'LINKED_TO',
        style: {
          stroke: e.type === 'BLOCKED_BY' ? '#f43f5e' : e.type === 'LINKED_TO' ? '#f59e0b' : '#38bdf8',
          strokeWidth: 2
        },
        markerEnd: { type: MarkerType.ArrowClosed, color: '#38bdf8' }
      }));

      setNodes(flowNodes);
      setEdges(flowEdges);

      const target = data.nodes.find((n) => n.id === centerId);
      if (target) setSelectedNode(target);
    } catch (err: any) {
      console.error('Failed to load neighborhood:', err);
    } finally {
      setLoading(false);
    }
  }, [setNodes, setEdges]);

  useEffect(() => {
    loadNeighborhood('proj_atlas', depth);
  }, [loadNeighborhood, depth]);

  const handleNodeClick = (_: any, node: Node) => {
    setSelectedNode(node.data.raw as GraphNodeData);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    try {
      const results = await api.searchGraph(searchQuery, selectedType === 'all' ? undefined : selectedType);
      if (results.length > 0) {
        loadNeighborhood(results[0].id, depth);
      } else {
        alert('No matching graph entity found.');
      }
    } catch (err: any) {
      alert(`Search failed: ${err.message}`);
    }
  };

  const handleFindPath = async () => {
    try {
      const paths = await api.findPaths(pathSource, pathTarget, 4);
      setPathResults(paths);
      if (paths.length > 0) {
        // Highlight path nodes and edges in graph
        loadNeighborhood(pathTarget, 2);
      } else {
        alert('No direct path found within 4 hops.');
      }
    } catch (err: any) {
      alert(`Pathfinding error: ${err.message}`);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-100px)] space-y-3">
      {/* Top Controls Toolbar */}
      <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
        {/* Search */}
        <form onSubmit={handleSearch} className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search entity in FalkorDB..."
              className="pl-8 pr-3 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 w-48"
            />
          </div>
          <button
            type="submit"
            className="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-semibold cursor-pointer"
          >
            Locate
          </button>
        </form>

        {/* Node Type Filter */}
        <div className="flex items-center gap-1.5 overflow-x-auto">
          <span className="text-slate-500 font-mono text-[11px]">Filter:</span>
          {['all', 'Project', 'Person', 'Decision', 'Ticket', 'SecurityEvent', 'Document'].map((t) => (
            <button
              key={t}
              onClick={() => setSelectedType(t)}
              className={`px-2 py-1 rounded-md text-[11px] cursor-pointer transition-all ${
                selectedType === t
                  ? 'bg-cyan-950 text-cyan-300 border border-cyan-500/50 font-semibold'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Neighborhood Depth Control */}
        <div className="flex items-center gap-2 font-mono text-slate-300">
          <span className="text-slate-500">Hops:</span>
          {[1, 2].map((d) => (
            <button
              key={d}
              onClick={() => setDepth(d)}
              className={`px-2 py-0.5 rounded text-xs cursor-pointer ${
                depth === d
                  ? 'bg-purple-900/80 text-purple-200 border border-purple-500 font-bold'
                  : 'bg-slate-950 text-slate-400 border border-slate-800'
              }`}
            >
              {d}
            </button>
          ))}
        </div>

        {/* Multi-Hop Path Finder Controls */}
        <div className="flex items-center gap-2">
          <span className="text-slate-500 font-mono text-[11px]">Path:</span>
          <input
            type="text"
            value={pathSource}
            onChange={(e) => setPathSource(e.target.value)}
            className="px-2 py-1 rounded bg-slate-950 border border-slate-800 text-[11px] font-mono text-cyan-300 w-20"
            title="Source entity ID"
          />
          <ArrowRight className="w-3 h-3 text-slate-500" />
          <input
            type="text"
            value={pathTarget}
            onChange={(e) => setPathTarget(e.target.value)}
            className="px-2 py-1 rounded bg-slate-950 border border-slate-800 text-[11px] font-mono text-purple-300 w-24"
            title="Target entity ID"
          />
          <button
            onClick={handleFindPath}
            className="px-2.5 py-1 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-[11px] cursor-pointer shadow-sm"
          >
            Find Path
          </button>
        </div>
      </div>

      {/* Main Canvas & Details Drawer */}
      <div className="flex-1 flex gap-3 overflow-hidden">
        {/* React Flow Graph Area */}
        <div className="flex-1 rounded-2xl overflow-hidden border border-slate-800 bg-[#080c14] relative">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={handleNodeClick}
            fitView
          >
            <Background color="#1e293b" gap={20} size={1} />
            <Controls className="bg-slate-900 border-slate-700 text-white fill-white" />
            <MiniMap
              nodeColor={(n) => {
                const rawType = (n.data as any)?.raw?.type;
                const color = rawType ? NODE_COLORS[rawType] : undefined;
                return color ? color.border : '#64748b';
              }}
              style={{ backgroundColor: '#090d16', border: '1px solid #1e293b' }}
            />
          </ReactFlow>

          {loading && (
            <div className="absolute top-4 left-4 z-10 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-700 text-xs text-cyan-400 font-mono shadow-lg flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
              <span>Querying FalkorDB Graph...</span>
            </div>
          )}
        </div>

        {/* Selected Node Details Drawer */}
        <div className="w-80 rounded-2xl bg-slate-900/90 border border-slate-800 p-4 flex flex-col justify-between overflow-y-auto space-y-4">
          {selectedNode ? (
            <div className="space-y-4 text-xs">
              <div className="border-b border-slate-800 pb-3">
                <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 uppercase">
                  <span>Type: {selectedNode.type}</span>
                  <span className="text-cyan-400">{selectedNode.tenant_id}</span>
                </div>
                <h3 className="text-base font-bold text-white mt-1">{selectedNode.label}</h3>
                <span className="text-[10px] font-mono text-slate-500">ID: {selectedNode.id}</span>
              </div>

              {/* Properties */}
              <div className="space-y-2">
                <span className="font-semibold text-slate-400 text-[11px]">Properties:</span>
                <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] space-y-1 text-slate-300">
                  {Object.entries(selectedNode.properties || {}).map(([k, v]) => (
                    <div key={k} className="flex justify-between border-b border-slate-900 pb-1">
                      <span className="text-slate-500">{k}:</span>
                      <span className="text-slate-200 text-right truncate max-w-[150px]">{String(v)}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-2 pt-2">
                <button
                  onClick={() => loadNeighborhood(selectedNode.id, 1)}
                  className="w-full py-2 rounded-xl bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/40 text-xs font-semibold cursor-pointer transition-all"
                >
                  Expand 1-Hop Neighborhood
                </button>
                <button
                  onClick={() => loadNeighborhood(selectedNode.id, 2)}
                  className="w-full py-2 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/40 text-xs font-semibold cursor-pointer transition-all"
                >
                  Expand 2-Hop Deep Neighborhood
                </button>
              </div>

              {/* Multi-Hop Path Results */}
              {pathResults.length > 0 && (
                <div className="p-3 rounded-xl bg-slate-950 border border-purple-500/40 space-y-1">
                  <div className="text-[11px] font-bold text-purple-300 flex items-center gap-1">
                    <Sparkles className="w-3 h-3" />
                    <span>Discovered Path ({pathResults[0].hop_count} Hops):</span>
                  </div>
                  <div className="text-[10px] font-mono text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {pathResults[0].path_description}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center text-slate-500 space-y-2">
              <Share2 className="w-8 h-8 text-slate-600" />
              <p className="text-xs">Click any node on the graph canvas to inspect properties, dependencies, and owners.</p>
            </div>
          )}

          <div className="text-[10px] font-mono text-slate-500 border-t border-slate-800 pt-2 text-center">
            Powered by FalkorDB Graph Engine
          </div>
        </div>
      </div>
    </div>
  );
}
