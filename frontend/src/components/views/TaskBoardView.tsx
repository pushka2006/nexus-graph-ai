'use client';

import React, { useState, useEffect } from 'react';
import { CheckSquare, Clock, AlertCircle, Plus, Check, User, ShieldAlert, Bot } from 'lucide-react';
import { api } from '@/lib/api';
import { TaskItem } from '@/types';

export function TaskBoardView() {
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form states
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high' | 'critical'>('high');
  const [assignedTo, setAssignedTo] = useState('emp_07');

  const loadTasks = async () => {
    setLoading(true);
    try {
      const data = await api.getTasks();
      setTasks(data);
    } catch (err: any) {
      console.error('Failed to load tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await api.createTask({
        title,
        description,
        priority,
        assigned_to: assignedTo,
        project_id: 'proj_atlas'
      });
      setShowAddModal(false);
      setTitle('');
      setDescription('');
      loadTasks();
    } catch (err: any) {
      alert(`Failed to create task: ${err.message}`);
    }
  };

  const columns = [
    { id: 'pending', title: 'Pending Triage', color: 'border-slate-700 bg-slate-900/40' },
    { id: 'in_progress', title: 'In Progress', color: 'border-cyan-500/40 bg-cyan-950/20' },
    { id: 'waiting_approval', title: 'Waiting Approval (Gate)', color: 'border-purple-500/40 bg-purple-950/20' },
    { id: 'completed', title: 'Completed', color: 'border-emerald-500/40 bg-emerald-950/20' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>Task Coordination & Agent Handoff Board</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-700">
              Track 02
            </span>
          </h1>
          <p className="text-xs text-slate-400">Concurrency-protected task leases and agent assignment</p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 text-slate-950 font-semibold text-xs transition-all cursor-pointer flex items-center gap-1.5 shadow-sm"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Task</span>
        </button>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {columns.map((col) => {
          const colTasks = tasks.filter((t) => t.status === col.id);

          return (
            <div key={col.id} className={`p-4 rounded-xl border ${col.color} flex flex-col space-y-3 min-h-[450px]`}>
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="font-semibold text-xs text-white">{col.title}</span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-950 border border-slate-800 text-slate-400">
                  {colTasks.length}
                </span>
              </div>

              <div className="space-y-2.5 flex-1 overflow-y-auto">
                {colTasks.map((t) => (
                  <div
                    key={t.id}
                    className="p-3 rounded-lg bg-slate-950/90 border border-slate-800 hover:border-slate-700 transition-all space-y-2 text-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span
                        className={`text-[9px] font-mono px-1.5 py-0.5 rounded font-bold uppercase ${
                          t.priority === 'critical'
                            ? 'bg-rose-950 text-rose-300 border border-rose-800'
                            : t.priority === 'high'
                            ? 'bg-amber-950 text-amber-300 border border-amber-800'
                            : 'bg-slate-800 text-slate-300'
                        }`}
                      >
                        {t.priority}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500">{t.id}</span>
                    </div>

                    <h4 className="font-semibold text-white leading-snug">{t.title}</h4>
                    <p className="text-[11px] text-slate-400 leading-normal line-clamp-2">{t.description}</p>

                    <div className="pt-2 border-t border-slate-900 flex items-center justify-between text-[10px] text-slate-400">
                      <span className="flex items-center gap-1">
                        <User className="w-3 h-3 text-cyan-400" />
                        <span>{t.assigned_to || 'Unassigned'}</span>
                      </span>
                      {t.assigned_agent && (
                        <span className="flex items-center gap-1 font-mono text-purple-300">
                          <Bot className="w-3 h-3" />
                          <span>{t.assigned_agent}</span>
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Add Task Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <form
            onSubmit={handleCreateTask}
            className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <CheckSquare className="w-4 h-4 text-cyan-400" />
                <span>Create New Task</span>
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
                <label className="text-slate-400 block mb-1">Task Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Audit S3 bucket KMS key policies"
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
                  required
                />
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                  placeholder="Actionable steps or investigation objectives..."
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1">Priority</label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value as any)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                </div>
                <div>
                  <label className="text-slate-400 block mb-1">Assigned Employee</label>
                  <select
                    value={assignedTo}
                    onChange={(e) => setAssignedTo(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-xs"
                  >
                    <option value="emp_07">Marcus Chen (Principal Architect)</option>
                    <option value="emp_08">Aria Song (Lead AI Engineer)</option>
                    <option value="emp_09">Zack Brody (SecOps Incident Handler)</option>
                    <option value="emp_11">Maya Lin (Principal PM - Atlas)</option>
                  </select>
                </div>
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
                Create Task
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
