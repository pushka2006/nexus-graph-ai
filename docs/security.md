# NEXUS GRAPH AI - Security & Trust Architecture

## 1. Cypher & Query Injection Defense
Model-generated Cypher queries can be weaponized if directly executed against graph stores. NEXUS GRAPH AI enforces a strict multi-layer defense:
- **Parameterized Query Execution**: User inputs and entity IDs are passed strictly as Cypher parameters (`$id`, `$tenant_id`), never string-concatenated.
- **Allowlisted Template Planning**: The Graph Reasoning Agent selects from pre-validated structural query templates (e.g. neighborhood expansion, shortest path, dependency lookup) rather than emitting raw unconstrained Cypher.
- **Read-Only Enclave for Browser**: The frontend never has direct Cypher execution privileges. All graph interactions flow through typed FastAPI endpoints with schema validation.

## 2. Multi-Tenant Cryptographic Isolation
- Every FalkorDB node, edge, and memory record is stamped with an immutable `tenant_id`.
- Graph traversals include `WHERE n.tenant_id = $tenant_id` clauses to prevent cross-tenant information leakage.
- Automated tests (`test_memory_types_and_tenant_isolation`) verify that queries from `tenant_alpha` cannot observe or infer assets belonging to `tenant_beta`.

## 3. Human-in-the-Loop Action Authorization Gates
Autonomous agents have bounded permissions:
- **Read-Only Tools** (`search_entities`, `find_paths`, `get_neighbors`) execute automatically to facilitate swift intelligence retrieval.
- **State-Changing Tools** (`create_task`, `assign_task`, `prepare_incident_report`, `revoke_token`):
  1. The Action Agent creates a pending approval record with a dry-run parameter summary.
  2. The action is held in state `waiting_approval`.
  3. A human operator must explicitly authorize execution via `/api/v1/tasks/{approval_id}/approve`.
  4. An immutable audit entry is stamped with the approver ID, timestamp, and signed receipt.

## 4. Prompt Injection & Source Trust Boundaries
Retrieved document passages, meeting transcripts, and support tickets are treated as **untrusted user data**, not system instructions.
- Document chunks are injected into fenced context blocks.
- The Quality & Verification Agent checks whether LLM outputs derive exclusively from grounded graph facts rather than prompt-injected instructions.

## 5. Audit Logging & Non-Repudiation
Every tool invocation, human approval, and agent handoff produces an entry in the centralized audit log with:
- `actor` (user or agent name)
- `actor_type` (`user`, `agent`, `system`)
- `action` (`execute:tool_name`, `approve:tool_name`)
- `target_resource`
- `timestamp`
- `status` (`authorized`, `denied`, `executed`, `failed`)
- `tenant_id`
