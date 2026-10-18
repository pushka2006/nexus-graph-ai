import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.models.schemas import MemoryItem, MemoryType
from app.config import get_settings

logger = logging.getLogger("nexus.memory.service")

class MemoryService:
    """
    Tiered memory service managing Episodic, Semantic, and Procedural memory
    with strict tenant isolation, confidence scoring, provenance tracking,
    and concurrent lease-lock coordination.
    """
    def __init__(self):
        # In-memory fast tier + persistent table backing
        self._memories: Dict[str, MemoryItem] = {}
        self._locks: Dict[str, Dict[str, Any]] = {}  # resource_id -> {holder, expires_at}
        self._seed_default_memories()

    def _seed_default_memories(self):
        defaults = [
            MemoryItem(
                id="mem_init_01",
                tenant_id="tenant_nexus_main",
                memory_type=MemoryType.EPISODIC,
                summary="Prior Investigation of Project Atlas Blocker",
                details={
                    "investigator": "Graph Reasoning Agent",
                    "target_project": "proj_atlas",
                    "discovered_blocker": "AD-104 (Cloud KMS compliance gate)",
                    "decider": "Elena Vance (CPO) and Aris Thorne (VP Eng)",
                    "findings": "Project Atlas launch v1.0 blocked pending formal review of KMS key encryption."
                },
                confidence=0.99,
                source_ref="meet_01",
                related_entities=["proj_atlas", "dec_104", "emp_02", "emp_01"],
                verified=True
            ),
            MemoryItem(
                id="mem_init_02",
                tenant_id="tenant_nexus_main",
                memory_type=MemoryType.SEMANTIC,
                summary="Entity Ownership: Project Atlas Sponsoring & Engineering",
                details={
                    "project_owner": "emp_11 (Maya Lin, Principal PM)",
                    "sponsor": "emp_02 (Elena Vance, CPO)",
                    "lead_architect": "emp_07 (Marcus Chen, Principal Infrastructure Architect)",
                    "lead_graph_eng": "emp_08 (Aria Song, Lead AI Graph Engineer)"
                },
                confidence=1.0,
                source_ref="doc_atlas_prd",
                related_entities=["proj_atlas", "emp_11", "emp_02", "emp_07", "emp_08"],
                verified=True
            ),
            MemoryItem(
                id="mem_init_03",
                tenant_id="tenant_nexus_main",
                memory_type=MemoryType.PROCEDURAL,
                summary="SecOps P1 Anomaly Investigation Playbook",
                details={
                    "playbook_id": "PB-SEC-01",
                    "steps": [
                        "1. Identify compromised security event ID in FalkorDB",
                        "2. Traverse 2-hop neighborhood to identify connected tickets and projects",
                        "3. Verify if affected asset has active customer-facing dependencies",
                        "4. Formulate containment plan and request explicit human authorization before token revoke"
                    ]
                },
                confidence=1.0,
                source_ref="doc_incident_runbook",
                related_entities=["sec_014", "inc_08", "agent_security"],
                verified=True
            )
        ]
        for m in defaults:
            self._memories[m.id] = m

    def add_memory(
        self,
        memory_type: MemoryType,
        summary: str,
        details: Dict[str, Any],
        confidence: float = 1.0,
        source_ref: Optional[str] = None,
        related_entities: List[str] = None,
        tenant_id: str = "tenant_nexus_main",
        user_id: Optional[str] = None,
        verified: bool = True
    ) -> MemoryItem:
        mem_id = f"mem_{uuid.uuid4().hex[:8]}"
        item = MemoryItem(
            id=mem_id,
            tenant_id=tenant_id,
            user_id=user_id,
            memory_type=memory_type,
            summary=summary,
            details=details,
            confidence=confidence,
            source_ref=source_ref,
            related_entities=related_entities or [],
            verified=verified,
            created_at=datetime.utcnow(),
            access_count=0
        )
        self._memories[mem_id] = item
        logger.info(f"Recorded {memory_type.value} memory {mem_id}: {summary} [Tenant: {tenant_id}]")
        return item

    def search_memories(
        self,
        query: str = "",
        memory_type: Optional[MemoryType] = None,
        tenant_id: str = "tenant_nexus_main",
        limit: int = 20
    ) -> List[MemoryItem]:
        results = []
        q = query.lower().strip()
        for m in self._memories.values():
            # Tenant isolation
            if m.tenant_id != tenant_id and tenant_id != "all":
                continue
            if memory_type and m.memory_type != memory_type:
                continue
            if q:
                combined = (m.summary + " " + str(m.details) + " " + " ".join(m.related_entities)).lower()
                if q not in combined:
                    continue
            m.access_count += 1
            results.append(m)
            if len(results) >= limit:
                break
        return results

    def get_memory(self, memory_id: str, tenant_id: str = "tenant_nexus_main") -> Optional[MemoryItem]:
        item = self._memories.get(memory_id)
        if item and (item.tenant_id == tenant_id or tenant_id == "all"):
            item.access_count += 1
            return item
        return None

    def acquire_task_lease(self, resource_id: str, agent_id: str, ttl_seconds: int = 60) -> bool:
        """
        Concurrency protection: Acquires an exclusive lease for an agent on a task/investigation.
        Prevents multiple agents from duplicate executions.
        """
        now = datetime.utcnow().timestamp()
        current_lock = self._locks.get(resource_id)
        if current_lock:
            if current_lock["expires_at"] > now and current_lock["holder"] != agent_id:
                # Still locked by another agent
                return False
        # Grant lease
        self._locks[resource_id] = {
            "holder": agent_id,
            "expires_at": now + ttl_seconds
        }
        return True

    def release_task_lease(self, resource_id: str, agent_id: str):
        current_lock = self._locks.get(resource_id)
        if current_lock and current_lock["holder"] == agent_id:
            del self._locks[resource_id]

    def get_stats(self, tenant_id: str = "tenant_nexus_main") -> Dict[str, Any]:
        counts = {"episodic": 0, "semantic": 0, "procedural": 0}
        total = 0
        for m in self._memories.values():
            if m.tenant_id == tenant_id or tenant_id == "all":
                counts[m.memory_type.value] = counts.get(m.memory_type.value, 0) + 1
                total += 1
        return {
            "total_memories": total,
            "counts_by_type": counts,
            "active_leases": len(self._locks)
        }

_memory_service_instance = None

def get_memory_service() -> MemoryService:
    global _memory_service_instance
    if _memory_service_instance is None:
        _memory_service_instance = MemoryService()
    return _memory_service_instance
