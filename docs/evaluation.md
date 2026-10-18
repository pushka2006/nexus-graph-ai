# NEXUS GRAPH AI - Evaluation Suite & Benchmarks

## Benchmark Methodology
The evaluation suite (`scripts/evaluate.py`) tests 12 critical enterprise scenarios spanning Graph Reasoning (Track 01), Memory & Coordination (Track 02), and Company Brain (Track 03):

| Scenario | Objective | Ground Truth / Expected Output |
| :--- | :--- | :--- |
| **1. Multi-hop Ownership** | Traverse Person -> Team -> Department -> Project | Minimum 1 valid path discovered in <= 3 hops |
| **2. Dependency Reasoning** | Identify blockers for Project Atlas | Discovers Architecture Decision `AD-104` |
| **3. Security Graph Correlation** | Correlate `SEC-014` with incidents and tickets | Connects `SEC-014` -> `INC-08` -> `TIK-204` -> `Project Atlas` |
| **4. Source Traceability** | Verify source document citations for answer | At least 2 citations with document IDs and timestamps |
| **5. Document Freshness** | Confirm active document is marked current | `doc_sec_pol_v20` marked `current` |
| **6. Conflict Detection** | Identify superseded conflicting policies | Flags `doc_sec_pol_v20` superseding `v1.2` (KMS mandate) |
| **7. Persistent Memory** | Store and recall semantic/episodic facts | Memory retrieved accurately across sessions |
| **8. Agent Coordination** | Prevent concurrent duplicate task executions | Lease lock acquired exclusively; second agent rejected |
| **9. Company Brain QA** | Answer natural language enterprise questions | Grounded synthesis with citations and confidence >= 0.9 |
| **10. Authorized Tool Execution** | Execute state-changing action with approval | Task created and recorded in audit log |
| **11. Authorization Gate** | Enforce human-in-the-loop gate on sensitive tools | Unapproved state-changing action returns `waiting_approval` |
| **12. Multi-Tenant Isolation** | Ensure zero cross-tenant memory leakage | Tenant B cannot search or retrieve Tenant A's memories |

## Measured Results
- **Pass Rate**: 12/12 (100.0%)
- **Retrieval Recall @ 5**: 100.0%
- **Evidence Citation Precision**: 100.0%
- **Multi-Hop Success Rate**: 100.0%
- **Tool Selection Accuracy**: 100.0%
- **Unsupported Claim Rate**: 0.0%
- **Concurrency Duplicate Task Rate**: 0.0%
- **Average Graph Query Latency**: 25.59 ms
- **Knowledge Graph Scale**: 309 nodes, 369 edges
