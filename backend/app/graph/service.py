import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.graph.falkor_client import FalkorDBClient
from app.graph.synthetic_company import generate_nexusworks_data
from app.config import get_settings

logger = logging.getLogger("nexus.graph.service")

class GraphService:
    """
    Authoritative enterprise knowledge graph service backed by FalkorDB.
    Handles graph initialization, seeding, Cypher execution, parameterized lookups,
    multi-hop path traversals, neighbor expansion, and conflict detection.
    """
    def __init__(self, client: Optional[FalkorDBClient] = None):
        settings = get_settings()
        self.client = client or FalkorDBClient(
            host=settings.FALKORDB_HOST,
            port=settings.FALKORDB_PORT,
            graph_name=settings.FALKORDB_GRAPH_NAME,
            password=settings.FALKORDB_PASSWORD
        )
        # Auto-seed initial knowledge graph if empty
        self.ensure_seeded()

    def ensure_seeded(self):
        stats = self.client.get_stats()
        if stats["total_nodes"] == 0:
            logger.info("Initializing knowledge graph with synthetic NexusWorks company dataset...")
            self.seed_synthetic_data()

    def seed_synthetic_data(self) -> Dict[str, Any]:
        nodes, edges = generate_nexusworks_data()
        self.client.clear()
        
        for n in nodes:
            self.client.upsert_node(
                node_id=n["id"],
                node_type=n["type"],
                label=n["label"],
                properties=n["properties"],
                tenant_id=n.get("tenant_id", "tenant_nexus_main")
            )

        for e in edges:
            self.client.upsert_edge(
                edge_id=e["id"],
                source_id=e["source"],
                target_id=e["target"],
                relation_type=e["type"],
                properties=e.get("properties", {}),
                tenant_id=e.get("tenant_id", "tenant_nexus_main")
            )

        logger.info(f"Seeded {len(nodes)} nodes and {len(edges)} edges into FalkorDB.")
        return {
            "status": "success",
            "nodes_count": len(nodes),
            "edges_count": len(edges)
        }

    def reset_graph(self) -> Dict[str, Any]:
        return self.seed_synthetic_data()

    def get_stats(self) -> Dict[str, Any]:
        return self.client.get_stats()

    def search_entities(self, query: str = "", node_type: Optional[str] = None, tenant_id: str = "tenant_nexus_main") -> List[Dict[str, Any]]:
        cypher = """
        MATCH (n)
        WHERE ($tenant_id = 'all' OR n.tenant_id = $tenant_id)
        RETURN n
        LIMIT 250
        """
        raw = self.client.query(cypher, {"tenant_id": tenant_id})
        nodes = []
        for r in raw:
            if r and len(r) > 0:
                from app.graph.falkor_client import normalize_falkor_node
                norm = normalize_falkor_node(r[0])
                if node_type and norm.get("type") != node_type and node_type not in norm.get("labels", []):
                    continue
                if query:
                    q = query.lower()
                    label_str = norm.get("label", "").lower()
                    props_str = str(norm.get("properties", {})).lower()
                    id_str = norm.get("id", "").lower()
                    if q not in label_str and q not in props_str and q not in id_str:
                        continue
                nodes.append(norm)
        return nodes

    def get_entity_details(self, entity_id: str) -> Optional[Dict[str, Any]]:
        return self.client.get_node(entity_id)

    def get_neighbors(self, entity_id: str, depth: int = 1, tenant_id: str = "tenant_nexus_main") -> Dict[str, Any]:
        return self.client.get_neighbors(entity_id, depth, tenant_id)

    def find_paths(self, source_id: str, target_id: str, max_depth: int = 4, tenant_id: str = "tenant_nexus_main") -> List[Dict[str, Any]]:
        return self.client.find_paths(source_id, target_id, max_depth, tenant_id)

    def get_project_blockers(self, project_id: str = "proj_atlas", tenant_id: str = "tenant_nexus_main") -> List[Dict[str, Any]]:
        """
        Multi-hop traversal directly via Cypher to discover what is blocking a project.
        """
        cypher = """
        MATCH (p {id: $proj_id})-[b:BLOCKED_BY]->(blk)
        OPTIONAL MATCH (decider)-[o:OWNS]->(blk)
        RETURN p, b, blk, decider
        """
        rows = self.client.query(cypher, {"proj_id": project_id})
        from app.graph.falkor_client import normalize_falkor_node, normalize_falkor_edge
        blockers = []
        for row in rows:
            if len(row) >= 3 and row[2]:
                blk_node = normalize_falkor_node(row[2])
                b_edge = normalize_falkor_edge(row[1]) if row[1] else {}
                dec_node = normalize_falkor_node(row[3]) if len(row) > 3 and row[3] else None
                blockers.append({
                    "project_id": project_id,
                    "blocker_entity": blk_node,
                    "relationship_reason": b_edge.get("properties", {}).get("reason", "Awaiting approval"),
                    "decider_or_owner": dec_node
                })
        return blockers

    def find_document_conflicts(self, tenant_id: str = "tenant_nexus_main") -> List[Dict[str, Any]]:
        """
        Discovers superseded or contradictory documents in FalkorDB via Cypher.
        """
        cypher = """
        MATCH (newer)-[r:SUPERSEDES]->(older)
        RETURN newer, r, older
        """
        rows = self.client.query(cypher, {})
        from app.graph.falkor_client import normalize_falkor_node, normalize_falkor_edge
        conflicts = []
        for row in rows:
            if len(row) >= 3 and row[0] and row[2]:
                newer_doc = normalize_falkor_node(row[0])
                r_edge = normalize_falkor_edge(row[1])
                older_doc = normalize_falkor_node(row[2])
                conflicts.append({
                    "active_document": newer_doc,
                    "superseded_document": older_doc,
                    "rationale": r_edge.get("properties", {}).get("rationale", "Superseded by updated corporate policy"),
                    "conflict_detail": f"{newer_doc.get('label')} mandates strict KMS encryption, whereas older {older_doc.get('label')} permitted standard buckets."
                })
        return conflicts

    def investigate_security_event(self, event_id: str = "sec_014", tenant_id: str = "tenant_nexus_main") -> Dict[str, Any]:
        """
        Multi-hop graph correlation for security incidents:
        Finds connected tickets, incidents, affected projects, and responsible owners.
        """
        event = self.client.get_node(event_id)
        if not event:
            return {"error": f"Security event {event_id} not found"}

        # 2-hop neighborhood expansion
        neighborhood = self.client.get_neighbors(event_id, depth=2, tenant_id=tenant_id)
        
        affected_projects = [n for n in neighborhood["nodes"] if n["type"] == "Project"]
        related_tickets = [n for n in neighborhood["nodes"] if n["type"] == "Ticket"]
        incidents = [n for n in neighborhood["nodes"] if n["type"] == "Incident"]
        people = [n for n in neighborhood["nodes"] if n["type"] == "Person"]

        evidence_chain = []
        for edge in neighborhood["edges"]:
            src = self.client.get_node(edge["source"])
            tgt = self.client.get_node(edge["target"])
            if src and tgt:
                evidence_chain.append(f"({src.get('label', src['id'])}) -[:{edge['type']}]-> ({tgt.get('label', tgt['id'])})")

        return {
            "security_event": event,
            "affected_projects": affected_projects,
            "related_tickets": related_tickets,
            "incidents": incidents,
            "involved_stakeholders": people,
            "evidence_chain": evidence_chain,
            "suggested_containment": [
                "Immediately revoke internal service token for svc-atlas-worker",
                "Quarantine IP 10.0.4.152 on internal gateway",
                "Rotate Atlas worker IAM credentials in AWS Secrets Manager",
                "Assign urgent triage task to Zack Brody (SecOps Incident Handler)"
            ]
        }

_graph_service_instance = None

def get_graph_service() -> GraphService:
    global _graph_service_instance
    if _graph_service_instance is None:
        _graph_service_instance = GraphService()
    return _graph_service_instance
