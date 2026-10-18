import pytest
from app.memory.service import MemoryService
from app.models.schemas import MemoryType

def test_memory_types_and_tenant_isolation():
    mem_svc = MemoryService()

    # Add memory for tenant A
    item_a = mem_svc.add_memory(
        memory_type=MemoryType.EPISODIC,
        summary="Tenant A Atlas Investigation",
        details={"finding": "Secret Atlas info"},
        tenant_id="tenant_alpha"
    )

    # Add memory for tenant B
    item_b = mem_svc.add_memory(
        memory_type=MemoryType.SEMANTIC,
        summary="Tenant B Secret Strategy",
        details={"finding": "Secret Beta info"},
        tenant_id="tenant_beta"
    )

    # Search as tenant A - tenant B records must NOT appear!
    res_a = mem_svc.search_memories(query="Secret", tenant_id="tenant_alpha")
    assert any(m.id == item_a.id for m in res_a)
    assert not any(m.id == item_b.id for m in res_a), "Cross-tenant leakage detected!"

    # Search as tenant B
    res_b = mem_svc.search_memories(query="Secret", tenant_id="tenant_beta")
    assert any(m.id == item_b.id for m in res_b)
    assert not any(m.id == item_a.id for m in res_b), "Cross-tenant leakage detected!"

def test_concurrency_lease_locks():
    mem_svc = MemoryService()
    resource_id = "task_critical_sec_014"

    # Agent A acquires lease
    granted_a = mem_svc.acquire_task_lease(resource_id, agent_id="agent_security", ttl_seconds=60)
    assert granted_a is True

    # Agent B attempts to acquire same lease - should be DENIED
    granted_b = mem_svc.acquire_task_lease(resource_id, agent_id="agent_action", ttl_seconds=60)
    assert granted_b is False, "Concurrent duplicate execution was not prevented!"

    # Release lease
    mem_svc.release_task_lease(resource_id, agent_id="agent_security")

    # Now Agent B should be able to acquire
    granted_b_after = mem_svc.acquire_task_lease(resource_id, agent_id="agent_action", ttl_seconds=60)
    assert granted_b_after is True
