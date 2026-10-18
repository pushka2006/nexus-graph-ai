# NEXUS GRAPH AI - System Architecture

## Overview
**NEXUS GRAPH AI** is an enterprise-grade Autonomous Company Intelligence, Graph Reasoning, Persistent Memory, and Multi-Agent Coordination platform designed to satisfy all three hackathon tracks:
- **Track 01: Agents That Act on Connected Data** (Graph Reasoning Agent, multi-hop traversals, tool authorization, MCP protocol)
- **Track 02: Agent Memory and Coordination** (Episodic, Semantic, and Procedural memory, tenant isolation, concurrency protection, task lease tracking)
- **Track 03: Company Brain** (Grounded enterprise question answering, provenance citations, conflict detection, freshness tracking)

```mermaid
graph TD
    User([Enterprise User / Browser]) <--> FE[Next.js 15+ Enterprise Dashboard]
    FE <-->|REST & SSE Stream| API[FastAPI Gateway]
    
    subgraph Multi-Agent Orchestration Layer
        API --> Orchestrator[Master Orchestrator]
        Orchestrator --> GraphAgent[Graph Reasoning Agent]
        Orchestrator --> KnowledgeAgent[Company Knowledge Agent]
        Orchestrator --> MemoryAgent[Memory Agent]
        Orchestrator --> SecurityAgent[Security Investigation Agent]
        Orchestrator --> CoordAgent[Coordination Agent]
        Orchestrator --> ActionAgent[Action Agent (Approval Gated)]
        Orchestrator --> QualityAgent[Quality & Verification Agent]
    end

    subgraph Dual-Mode Storage & Graph Engine
        GraphAgent <-->|Cypher Queries| FalkorDB[(FalkorDB / Graph Engine)]
        MemoryAgent <-->|Episodic/Semantic/Procedural| MemStore[(PostgreSQL / SQLite + FalkorDB)]
        CoordAgent <-->|Task Leases & Locks| RedisStore[(Redis / Ephemeral Cache)]
        KnowledgeAgent <-->|Semantic Retrieval| VecStore[(Vector Store / MiniLM)]
    end

    subgraph AI Model Inference
        KnowledgeAgent <--> LLM[Qwen 2.5 3B / Hugging Face / vLLM / Mock Adapter]
        GraphAgent <--> LLM
    end
```

## Key Modules
1. **Frontend (`frontend/`)**: Next.js 15 App Router, React 19, TypeScript, Tailwind CSS, React Flow for dynamic graph exploration, Recharts for analytics, and Lucide icons.
2. **Backend Gateway (`backend/app/api/`)**: REST APIs, SSE endpoints for live agent streaming, Pydantic v2 schemas, role-based access control, tenant isolation.
3. **Graph Engine (`backend/app/graph/`)**: Dual-mode FalkorDB client with full Cypher parser, parameterization, and multi-hop traversal engine.
4. **Agent Mesh (`backend/app/agents/`)**: 7 specialized autonomous agents coordinated by the Master Orchestrator.
5. **Memory Tier (`backend/app/memory/`)**:
   - *Episodic*: Session history, execution traces, handoff receipts.
   - *Semantic*: Validated entity facts and relationships.
   - *Procedural*: Runbooks, task templates, approved workflows.
6. **Action & MCP Protocol (`backend/app/mcp/`)**: Model Context Protocol tool declarations with human-in-the-loop approval gates.
