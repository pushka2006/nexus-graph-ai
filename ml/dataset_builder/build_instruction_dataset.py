#!/usr/bin/env python3
"""
Converts FalkorDB graph relationships and enterprise Q&A into a Hugging Face
instruction dataset formatted with the Qwen2.5 chat template.
"""
import json
import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.graph.service import get_graph_service

def build_dataset():
    service = get_graph_service()
    out_dir = Path(__file__).resolve().parent
    out_file = out_dir / "qwen_graph_instruction_data.jsonl"

    qa_pairs = [
        {
            "messages": [
                {"role": "system", "content": "You are NEXUS GRAPH AI, an enterprise intelligence assistant grounded in the company knowledge graph."},
                {"role": "user", "content": "Who owns Project Atlas, and what is preventing its release?"},
                {"role": "assistant", "content": "Project Atlas is owned by Maya Lin (Principal Product Manager) and sponsored by Elena Vance (CPO). It is currently BLOCKED by Architecture Decision AD-104 ('Project Atlas Production Gate and Cloud Storage Migration') pending formal sign-off from VP Engineering Dr. Aris Thorne. AD-104 requires customer-managed KMS key encryption on cloud storage buckets under Information Security Policy v2.0."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You are NEXUS GRAPH AI, an enterprise intelligence assistant grounded in the company knowledge graph."},
                {"role": "user", "content": "Investigate the security event linked to Project Atlas and identify the related ticket and affected service."},
                {"role": "assistant", "content": "Security investigation for SEC-014 ('Abnormal Token Generation with Admin Privilege Escalation') connects directly to Ticket TIK-204 and active Incident INC-08. The affected subsystem is Project Atlas running on worker svc-atlas-worker (IP 10.0.4.152). Zack Brody (SecOps Incident Handler) is the assigned responder."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You are NEXUS GRAPH AI, an enterprise intelligence assistant grounded in the company knowledge graph."},
                {"role": "user", "content": "Explain the conflict between Information Security Policy v2.0 and v1.2."},
                {"role": "assistant", "content": "Information Security Policy v2.0 explicitly SUPERSEDES v1.2. Policy v2.0 strictly requires customer-managed KMS keys (CMK) on all S3 buckets and data stores, whereas legacy v1.2 permitted standard buckets for non-confidential project artifacts without server-side KMS keys."}
            ]
        }
    ]

    with open(out_file, "w", encoding="utf-8") as f:
        for pair in qa_pairs:
            f.write(json.dumps(pair) + "\n")

    print(f"[SUCCESS] Built instruction dataset with {len(qa_pairs)} samples at {out_file}")

if __name__ == "__main__":
    build_dataset()
