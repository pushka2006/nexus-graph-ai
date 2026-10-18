import httpx
import json

def test_chat():
    payload = {
        "message": "Who owns Project Atlas, why is its release blocked, which ticket and security event are related, and what should we do next?",
        "tenant_id": "tenant_nexus_main",
        "user_id": "user_admin"
    }
    print("Sending multi-agent chat request to http://127.0.0.1:8080/api/v1/chat...")
    r = httpx.post("http://127.0.0.1:8080/api/v1/chat", json=payload, timeout=120.0)
    print("HTTP STATUS:", r.status_code)
    assert r.status_code == 200, f"Chat failed with status {r.status_code}: {r.text}"
    
    data = r.json()
    print("\n--- AGENT GENERATED RESPONSE (Real Model) ---")
    print(data.get("answer"))
    print(f"\nModel Used: {data.get('model_used')} | Latency: {data.get('latency_ms')}ms | Confidence: {data.get('confidence')}")
    
    print("\n--- GROUNDED CITATIONS (Company Brain) ---")
    for c in data.get("citations", []):
        print(f"[{c.get('source_id')}] {c.get('source_title')} (Freshness: {c.get('freshness_status', 'current')}): {c.get('passage')}")
    
    print("\n--- FALKORDB EVIDENCE GRAPH PATHS (Track 01) ---")
    for ep in data.get("evidence_paths", []):
        print(f"- {ep.get('path_description')}")
        
    print("\n--- HUMAN-IN-THE-LOOP ACTIONS (Track 02) ---")
    for a in data.get("suggested_actions", []):
        print(f"- {a.get('title')} [Tool: {a.get('tool_name')}, Approval Required: {a.get('requires_approval')}]")
        
    print("\n--- AGENT REASONING STEPS & HANDOFFS ---")
    for s in data.get("reasoning_steps", []):
        print(f"Step {s.get('step_number')} [{s.get('agent_name')}]: {s.get('action_taken')} -> {s.get('result_summary')}")

if __name__ == "__main__":
    test_chat()
