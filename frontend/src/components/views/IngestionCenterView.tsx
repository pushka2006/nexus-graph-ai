'use client';

import React, { useState, useEffect } from 'react';
import { FileUp, CheckCircle, Database, RefreshCw, Upload, AlertCircle, FileText, Check } from 'lucide-react';
import { api } from '@/lib/api';

export function IngestionCenterView() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const [docName, setDocName] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const loadData = async () => {
    try {
      const docs = await api.getDocuments();
      const jList = await api.getIngestionJobs();
      setDocuments(docs);
      setJobs(jList);
    } catch (err: any) {
      console.error('Failed to load ingestion data:', err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSimulatedUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!docName.trim()) return;
    setUploading(true);
    setSuccessMsg('');
    try {
      await api.triggerIngestionJob(docName);
      setSuccessMsg(`Successfully ingested and indexed '${docName}' into FalkorDB graph!`);
      setDocName('');
      loadData();
    } catch (err: any) {
      alert(`Ingestion failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-base font-bold text-white flex items-center gap-2">
            <span>Documents & Knowledge Ingestion Pipeline</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-700">
              Track 03
            </span>
          </h1>
          <p className="text-xs text-slate-400">Extract entities, detect conflicts, and generate FalkorDB nodes and embeddings</p>
        </div>
      </div>

      {/* Upload & Ingestion Box */}
      <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <FileUp className="w-4 h-4 text-cyan-400" />
          <span>Upload New Knowledge Source</span>
        </h2>

        <form onSubmit={handleSimulatedUpload} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={docName}
            onChange={(e) => setDocName(e.target.value)}
            placeholder="Document title or specification name (e.g. Atlas Cloud KMS Architecture v2.5)..."
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500"
            required
          />
          <button
            type="submit"
            disabled={uploading}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-slate-950 font-semibold text-xs cursor-pointer shadow-md disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {uploading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                <span>Ingesting into Graph...</span>
              </>
            ) : (
              <>
                <Upload className="w-4 h-4" />
                <span>Ingest Document</span>
              </>
            )}
          </button>
        </form>

        {successMsg && (
          <div className="p-3 rounded-xl bg-emerald-950/60 border border-emerald-600 text-emerald-300 text-xs flex items-center gap-2">
            <Check className="w-4 h-4 text-emerald-400" />
            <span>{successMsg}</span>
          </div>
        )}
      </div>

      {/* Ingestion Jobs & Indexed Documents */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Ingestion Jobs */}
        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="text-sm font-semibold text-white">Ingestion Job History</h3>
            <span className="text-[10px] font-mono text-slate-400">{jobs.length} Jobs Processed</span>
          </div>

          <div className="space-y-2 max-h-80 overflow-y-auto">
            {jobs.map((j) => (
              <div key={j.job_id} className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white">{j.dataset_name}</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                    {j.status.toUpperCase()}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400 font-mono flex items-center justify-between">
                  <span>Records: {j.records_ingested}</span>
                  <span>Conflicts Detected: {j.conflicts_found}</span>
                  <span>{j.created_at.slice(0, 10)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Currently Indexed Documents */}
        <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="text-sm font-semibold text-white">Indexed Policy & Spec Documents</h3>
            <span className="text-[10px] font-mono text-cyan-400">{documents.length} In FalkorDB</span>
          </div>

          <div className="space-y-2 max-h-80 overflow-y-auto">
            {documents.slice(0, 10).map((d) => (
              <div key={d.id} className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-200 truncate max-w-[280px]">{d.label}</span>
                  <span
                    className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${
                      d.properties?.status === 'superseded'
                        ? 'bg-rose-950 text-rose-300 border border-rose-800'
                        : 'bg-slate-800 text-slate-300'
                    }`}
                  >
                    {d.properties?.version || 'v1.0'}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 line-clamp-1">{d.properties?.content_summary}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
