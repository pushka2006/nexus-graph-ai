# NEXUS GRAPH AI - Hackathon Demo Script & Walkthrough

This demo script walks through all 6 required scenes satisfying Track 01, Track 02, and Track 03.

---

## 1-Click Demo Reset
Before starting, click **"Reset Demo Graph"** in the **System Settings** page or execute:
```bash
python scripts/seed_demo.py
```
This restores all 309 nodes and 369 relationships deterministically in FalkorDB.

---

## Scene 1: Company Brain (Track 03)
**Objective**: Demonstrate multi-hop entity reasoning, blocker detection, and grounded document citations.

1. Navigate to **Company Brain Chat** (`/chat` or select from sidebar).
2. Ask:
   > *"Who owns Project Atlas, and what is preventing its release?"*
3. **Observe the Results**:
   - **Direct Answer**: Project Atlas is owned by Maya Lin (Principal PM) and sponsored by Elena Vance (CPO). It is blocked by Architecture Decision **AD-104**.
   - **Explainable Blocker**: AD-104 requires customer-managed KMS key encryption on cloud storage.
   - **Citations**: Click the clickable citations to expand `doc_atlas_prd` and `doc_sec_pol_v20`.
   - **Freshness & Conflicts**: Notice the warning highlighting that **Information Security Policy v2.0** strictly supersedes **v1.2**.

---

## Scene 2: Connected Data & Security Graph (Track 01)
**Objective**: Demonstrate security event correlation across tickets, incidents, and multi-hop paths.

1. In **Company Brain Chat** or **Security Center**, ask:
   > *"Investigate the security event linked to Project Atlas and identify the related ticket and affected service."*
2. **Observe the Graph Traversal**:
   - The **Security Investigation Agent** identifies anomaly **SEC-014** (*Abnormal Token Generation with Admin Privilege Escalation*).
   - Traversal Path:
     `(SEC-014: Security Event) -> (INC-08: Incident) -> (TIK-204: Ticket) -> (Project Atlas)`
   - The affected worker is `svc-atlas-worker` at `10.0.4.152`.
   - The primary responder is Zack Brody (SecOps Incident Handler).

---

## Scene 3: Agent Memory & Continuity (Track 02)
**Objective**: Demonstrate that autonomous agents remember prior discoveries and recover context in a new conversation without repeating queries.

1. Open a new chat session or navigate to the **Memory Inspector**.
2. Ask:
   > *"Recall our previous findings about the Project Atlas blocker."*
3. **Observe the Results**:
   - The **Memory Agent** retrieves episodic memory `mem_init_01` and semantic memory `mem_init_02`.
   - Confirms that Elena Vance is the required signatory for AD-104 and that Procedural Playbook `PB-SEC-01` governs the escalation.

---

## Scene 4: Multi-Agent Coordination (Track 02)
**Objective**: Show the Master Orchestrator assigning subtasks, managing leases, and preventing duplicate executions.

1. Navigate to the **Agent Orchestration Center** (`/agents`).
2. Inspect the live execution cards for all 7 specialized agents:
   - **Master Orchestrator**: Workflow routing & delegation.
   - **Graph Reasoning Agent**: FalkorDB Cypher traversal planning.
   - **Company Knowledge Agent**: Document chunk retrieval and freshness checks.
   - **Memory Agent**: Episodic, Semantic, and Procedural memory recall.
   - **Coordination Agent**: Lease acquisition preventing duplicate tasks.
   - **Security Investigation Agent**: Incident graph correlation.
   - **Action Agent**: Bounded tool execution with approval gates.
   - **Quality & Verification Agent**: Hallucination check & source groundings.

---

## Scene 5: Safe Action & Human Approval Gate (Track 01 & MCP)
**Objective**: Show authorized action execution protected by human-in-the-loop authorization and tamper-evident audit logs.

1. Review the suggested action generated in Scene 2:
   > *"Revoke Compromised Service Token & Quarantine IP"*
2. Click **"Review Action"**.
3. Inspect the dry-run summary:
   - Tool: `prepare_incident_report` & `create_task`
   - Parameters: Target worker `svc-atlas-worker`, Incident `INC-08`
4. Click **"Authorize Execution"**.
5. Switch to the **Audit Log** page (`/audit`) to inspect the immutable execution receipt signed with timestamp, approver ID, and action ID.

---

## Scene 6: Interactive Knowledge Graph Explorer (React Flow)
**Objective**: Visually interact with FalkorDB nodes and relationships.

1. Navigate to **Knowledge Graph Explorer** (`/graph`).
2. Search for `Project Atlas` or filter by `Project`.
3. Click on the `Project Atlas` node:
   - Expand 1-hop or 2-hop neighborhood.
   - View relationships: `OWNS`, `WORKS_ON`, `BLOCKED_BY`, `RELATED_TO`.
4. Click **Find Path** between `SEC-014` and `Project Atlas` to highlight the 3-hop attack correlation chain in neon cyan/purple.
