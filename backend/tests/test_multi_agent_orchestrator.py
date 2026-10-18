import pytest
from app.agents.orchestrator import MultiAgentOrchestrator
from app.mcp.tools import MCPToolRegistry

def test_company_brain_question_answering_scene1():
    orch = MultiAgentOrchestrator()
    resp = orch.run_workflow("Who owns Project Atlas, and what is preventing its release?")

    assert "Maya Lin" in resp.answer or "Elena Vance" in resp.answer
    assert "AD-104" in resp.answer or "blocked" in resp.answer.lower()
    assert len(resp.citations) > 0, "Expected source citations"
    assert len(resp.evidence_paths) > 0, "Expected evidence graph paths"
    assert resp.confidence >= 0.9

def test_security_investigation_scene2():
    orch = MultiAgentOrchestrator()
    resp = orch.run_workflow("Investigate the security event SEC-014 linked to Project Atlas")

    assert "SEC-014" in resp.answer
    assert "TIK-204" in resp.answer or "INC-08" in resp.answer
    assert len(resp.suggested_actions) > 0, "Expected recommended containment actions"
    assert resp.suggested_actions[0].requires_approval is True

def test_mcp_tool_execution_and_approval_gate():
    mcp = MCPToolRegistry()

    # Readonly tool runs immediately without approval
    res_readonly = mcp.execute_tool("get_entity_details", {"entity_id": "proj_atlas"})
    assert res_readonly["status"] == "success"

    # State-changing tool requires human approval gate
    res_action = mcp.execute_tool("create_task", {
        "title": "Test Follow-up Task",
        "description": "Verify containment action",
        "priority": "high"
    })
    assert res_action["status"] == "waiting_approval"
    assert "approval_id" in res_action

    # Approve action
    appr_id = res_action["approval_id"]
    receipt = mcp.approve_action(appr_id, approver_id="user_admin", comments="Approved by CISO")
    assert receipt.status == "executed"
    assert receipt.action_id == appr_id
    assert len(mcp.audit_log) > 0, "Audit log must record approved execution"
