'use client';

import React, { useState } from 'react';
import {
  Send,
  BrainCircuit,
  FileText,
  AlertTriangle,
  CheckCircle,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Bot,
  User,
  ShieldAlert,
  Loader2,
  Check
} from 'lucide-react';
import { api } from '@/lib/api';
import { ChatResponse, Citation, SuggestedAction } from '@/types';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  responseMeta?: ChatResponse;
  timestamp: string;
}

export function CompanyBrainView() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init_msg',
      sender: 'assistant',
      content:
        'Welcome to **NEXUS GRAPH AI: Company Brain**. I am grounded in the complete FalkorDB knowledge graph. Ask me about employees, projects, blockers, architecture decisions, security incidents, or policy supersession.',
      timestamp: '10:45 AM'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeCitation, setActiveCitation] = useState<Citation | null>(null);
  const [approvedActionIds, setApprovedActionIds] = useState<Set<string>>(new Set());

  const quickPrompts = [
    'Who owns Project Atlas, and what is preventing its release?',
    'Investigate the security event linked to Project Atlas and identify the related ticket and affected service.',
    'Recall our previous findings about the Project Atlas blocker.',
    'Explain the conflict between Information Security Policy v2.0 and v1.2.'
  ];

  const handleSend = async (textToSend?: string) => {
    const text = (textToSend || input).trim();
    if (!text || loading) return;

    const userMsg: Message = {
      id: `user_${Date.now()}`,
      sender: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.sendChat(text);
      const assistantMsg: Message = {
        id: `asst_${Date.now()}`,
        sender: 'assistant',
        content: res.answer,
        responseMeta: res,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errMsg: Message = {
        id: `err_${Date.now()}`,
        sender: 'assistant',
        content: `**Error connecting to Master Orchestrator:** ${err.message || 'Check backend status.'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (action: SuggestedAction) => {
    try {
      await api.createTask({
        title: action.title,
        description: action.dry_run_summary,
        priority: 'critical',
        project_id: 'proj_atlas'
      });
      setApprovedActionIds((prev) => new Set(prev).add(action.action_id));
    } catch (e: any) {
      alert(`Approval error: ${e.message}`);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-100px)] space-y-4">
      {/* Header bar */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-cyan-950/80 border border-cyan-500/40 text-cyan-400">
            <BrainCircuit className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white flex items-center gap-2">
              <span>Company Brain Intelligent Chat</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-700">
                Track 03
              </span>
            </h1>
            <p className="text-xs text-slate-400">Source-grounded question answering with FalkorDB Cypher traversals</p>
          </div>
        </div>

        {/* Quick Prompts */}
        <div className="hidden xl:flex items-center gap-2">
          {quickPrompts.slice(0, 2).map((qp, i) => (
            <button
              key={i}
              onClick={() => handleSend(qp)}
              className="px-2.5 py-1 text-[11px] rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 cursor-pointer transition-all truncate max-w-[280px]"
              title={qp}
            >
              {qp}
            </button>
          ))}
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          const meta = msg.responseMeta;

          return (
            <div key={msg.id} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
              {!isUser && (
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-600 to-purple-600 flex items-center justify-center text-slate-950 shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div className={`max-w-3xl space-y-3 ${isUser ? 'text-right' : 'text-left'}`}>
                <div
                  className={`p-4 rounded-2xl text-xs leading-relaxed ${
                    isUser
                      ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-md'
                      : 'bg-slate-900/90 border border-slate-800 text-slate-200 shadow-sm'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{msg.content}</div>

                  {meta && (
                    <div className="mt-2 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                      <span>Model: {meta.model_used}</span>
                      <span>Latency: {meta.latency_ms}ms | Confidence: {(meta.confidence * 100).toFixed(0)}%</span>
                    </div>
                  )}
                </div>

                {/* Grounding & Evidence Pack (Assistant only) */}
                {meta && (
                  <div className="space-y-2 text-xs">
                    {/* Conflicting Evidence Alert */}
                    {meta.conflicting_evidence && meta.conflicting_evidence.length > 0 && (
                      <div className="p-3 rounded-xl bg-amber-950/40 border border-amber-500/40 text-amber-200 text-xs flex items-start gap-2">
                        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                        <div>
                          <div className="font-semibold text-amber-300">Document Supersession & Policy Conflict Detected</div>
                          {meta.conflicting_evidence.map((conf, ci) => (
                            <p key={ci} className="text-[11px] text-amber-200/90 mt-0.5">{conf}</p>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Multi-Hop Evidence Graph Path */}
                    {meta.evidence_paths && meta.evidence_paths.length > 0 && (
                      <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
                        <div className="text-[11px] font-semibold text-cyan-300 flex items-center gap-1.5">
                          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                          <span>FalkorDB Graph Traversal Path</span>
                        </div>
                        {meta.evidence_paths.map((ep, ei) => (
                          <div key={ei} className="p-2 rounded bg-slate-900 border border-slate-800 font-mono text-[11px] text-slate-300">
                            {ep.path_description}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Source Citations */}
                    {meta.citations && meta.citations.length > 0 && (
                      <div className="space-y-1.5">
                        <div className="text-[11px] font-semibold text-slate-400">Supporting Source Citations:</div>
                        <div className="flex flex-wrap gap-2">
                          {meta.citations.map((c, ci) => (
                            <button
                              key={ci}
                              onClick={() => setActiveCitation(c)}
                              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] border cursor-pointer transition-all ${
                                c.freshness_status === 'superseded'
                                  ? 'bg-rose-950/60 border-rose-600/50 text-rose-300'
                                  : 'bg-slate-950 hover:bg-slate-900 border-slate-700 text-cyan-300'
                              }`}
                            >
                              <FileText className="w-3 h-3" />
                              <span className="font-medium truncate max-w-[200px]">{c.source_title}</span>
                              {c.freshness_status === 'superseded' && (
                                <span className="text-[9px] px-1 rounded bg-rose-900 text-rose-200">Superseded</span>
                              )}
                              <ExternalLink className="w-3 h-3 text-slate-400" />
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Suggested Actions with Human Approval Gate */}
                    {meta.suggested_actions && meta.suggested_actions.length > 0 && (
                      <div className="p-3.5 rounded-xl bg-gradient-to-r from-purple-950/40 to-slate-900 border border-purple-500/40 space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-semibold text-purple-300 flex items-center gap-1.5">
                            <ShieldAlert className="w-4 h-4 text-purple-400" />
                            <span>Action Agent Recommendation (Approval Gate Required)</span>
                          </span>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-900/80 text-purple-200 border border-purple-600">
                            HUMAN-IN-THE-LOOP
                          </span>
                        </div>
                        {meta.suggested_actions.map((act) => {
                          const isApproved = approvedActionIds.has(act.action_id);
                          return (
                            <div key={act.action_id} className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 flex items-center justify-between">
                              <div className="space-y-0.5">
                                <div className="text-xs font-semibold text-white">{act.title}</div>
                                <div className="text-[11px] text-slate-400">{act.dry_run_summary}</div>
                              </div>
                              <button
                                onClick={() => handleApprove(act)}
                                disabled={isApproved}
                                className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                                  isApproved
                                    ? 'bg-emerald-950 text-emerald-300 border border-emerald-600'
                                    : 'bg-purple-600 hover:bg-purple-500 text-white shadow-md'
                                }`}
                              >
                                {isApproved ? (
                                  <>
                                    <Check className="w-3.5 h-3.5" />
                                    <span>Authorized</span>
                                  </>
                                ) : (
                                  <span>Authorize Action</span>
                                )}
                              </button>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {isUser && (
                <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center text-slate-300 shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div className="flex items-center gap-3 p-4 rounded-xl bg-slate-900/70 border border-slate-800 max-w-md">
            <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />
            <div className="text-xs text-slate-300">
              <span className="font-semibold text-cyan-400">Master Orchestrator:</span> Traversing FalkorDB graph and synthesizing grounded response...
            </div>
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="pt-2 border-t border-slate-800 space-y-2">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything about projects, blockers, decisions, tickets, or security incidents..."
            className="flex-1 px-4 py-3 rounded-xl bg-slate-900/90 border border-slate-700 text-slate-100 placeholder:text-slate-500 text-xs focus:outline-none focus:border-cyan-500 transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-5 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-semibold text-xs transition-all shadow-[0_0_15px_rgba(6,182,212,0.4)] disabled:opacity-50 cursor-pointer flex items-center gap-1.5"
          >
            <Send className="w-4 h-4" />
            <span>Send</span>
          </button>
        </form>

        {/* Quick Prompts Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-[11px] text-slate-400">
          <span className="font-semibold text-slate-500 shrink-0">Try Demo Queries:</span>
          {quickPrompts.map((qp, i) => (
            <button
              key={i}
              onClick={() => handleSend(qp)}
              className="px-2.5 py-1 rounded-lg bg-slate-950 hover:bg-slate-900 text-slate-300 border border-slate-800 cursor-pointer whitespace-nowrap transition-all"
            >
              {qp}
            </button>
          ))}
        </div>
      </div>

      {/* Citation Detail Modal */}
      {activeCitation && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
                <FileText className="w-4 h-4" />
                <span>{activeCitation.source_title}</span>
              </div>
              <button
                onClick={() => setActiveCitation(null)}
                className="text-slate-400 hover:text-white text-xs cursor-pointer"
              >
                ✕ Close
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-serif leading-relaxed text-slate-300">
                "{activeCitation.passage}"
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                <div className="p-2 rounded bg-slate-950 border border-slate-800">
                  <span className="text-slate-500">Record ID:</span>{' '}
                  <span className="text-slate-200">{activeCitation.record_id || activeCitation.source_id}</span>
                </div>
                <div className="p-2 rounded bg-slate-950 border border-slate-800">
                  <span className="text-slate-500">Timestamp:</span>{' '}
                  <span className="text-slate-200">{activeCitation.timestamp || '2026-10'}</span>
                </div>
                <div className="p-2 rounded bg-slate-950 border border-slate-800">
                  <span className="text-slate-500">Confidence:</span>{' '}
                  <span className="text-emerald-400">{(activeCitation.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="p-2 rounded bg-slate-950 border border-slate-800">
                  <span className="text-slate-500">Status:</span>{' '}
                  <span className={activeCitation.freshness_status === 'superseded' ? 'text-rose-400' : 'text-cyan-400'}>
                    {activeCitation.freshness_status.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
