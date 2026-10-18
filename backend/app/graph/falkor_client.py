import logging
import re
import json
import time
import socket
import subprocess
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime

logger = logging.getLogger("nexus.graph.falkordb")

try:
    from falkordb import FalkorDB as FalkorDBDriver
    from falkordb.node import Node as FalkorNode
    from falkordb.edge import Edge as FalkorEdge
    FALKORDB_AVAILABLE = True
except ImportError:
    FALKORDB_AVAILABLE = False
    FalkorNode = None
    FalkorEdge = None
    logger.error("falkordb Python package is not installed. FalkorDB driver unavailable.")


def serialize_property_value(val: Any) -> Any:
    """Ensure property values are FalkorDB Cypher-compatible scalars or lists."""
    if val is None or isinstance(val, (int, float, bool, str)):
        return val
    if isinstance(val, list):
        # List of scalars or serialize items
        return [str(x) if isinstance(x, (dict, list)) else x for x in val]
    if isinstance(val, dict):
        return json.dumps(val)
    return str(val)


def normalize_falkor_node(node: Any) -> Dict[str, Any]:
    """Convert a FalkorDB Node object or dictionary to a standardized dictionary."""
    if isinstance(node, dict):
        return node
    if FalkorNode and isinstance(node, FalkorNode):
        props = dict(node.properties)
        node_id = props.get("id", str(node.id))
        label = props.get("label", node.labels[0] if node.labels else "Entity")
        node_type = node.labels[0] if node.labels else props.get("type", "Unknown")
        tenant_id = props.get("tenant_id", "tenant_nexus_main")
        return {
            "id": str(node_id),
            "type": node_type,
            "label": label,
            "properties": props,
            "tenant_id": tenant_id,
            "labels": list(node.labels) if hasattr(node, "labels") else [node_type]
        }
    if hasattr(node, "properties"):
        props = dict(node.properties)
        return {
            "id": str(props.get("id", getattr(node, "id", "unknown"))),
            "type": props.get("type", "Unknown"),
            "label": str(props.get("label", "")),
            "properties": props,
            "tenant_id": props.get("tenant_id", "tenant_nexus_main")
        }
    return {"raw": str(node)}


def normalize_falkor_edge(edge: Any) -> Dict[str, Any]:
    """Convert a FalkorDB Edge object or dictionary to a standardized dictionary."""
    if isinstance(edge, dict):
        return edge
    if FalkorEdge and isinstance(edge, FalkorEdge):
        props = dict(edge.properties)
        edge_id = props.get("id", str(edge.id))
        relation_type = edge.relation if hasattr(edge, "relation") else "RELATED_TO"
        return {
            "id": str(edge_id),
            "source": str(props.get("source_id", getattr(edge, "src_node", ""))),
            "target": str(props.get("target_id", getattr(edge, "dest_node", ""))),
            "type": relation_type,
            "properties": props,
            "tenant_id": props.get("tenant_id", "tenant_nexus_main")
        }
    if hasattr(edge, "properties"):
        props = dict(edge.properties)
        return {
            "id": str(props.get("id", getattr(edge, "id", "unknown"))),
            "source": str(props.get("source_id", "")),
            "target": str(props.get("target_id", "")),
            "type": getattr(edge, "relation", props.get("type", "RELATED_TO")),
            "properties": props,
            "tenant_id": props.get("tenant_id", "tenant_nexus_main")
        }
    return {"raw": str(edge)}


class FalkorDBClient:
    """
    Authoritative FalkorDB Client connected to a real, live FalkorDB server.
    Executes native parameterized Cypher queries, graph analytics, multi-hop traversals,
    schema introspection, and relationship mutations.
    """
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        graph_name: str = "nexus_company_graph",
        password: str = ""
    ):
        self.configured_host = host
        self.port = port
        self.graph_name = graph_name
        self.password = password
        self.active_host = host
        self.is_connected = False
        self._driver = None
        self._graph = None
        self.last_health_check = None
        self.last_error = None
        self.connect()

    def _resolve_connection_host(self) -> str:
        """
        Verify if configured host:port is reachable. If localhost fails on Windows WSL2,
        resolve the active WSL IP address.
        """
        # 1. Test configured host
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        if s.connect_ex((self.configured_host, self.port)) == 0:
            s.close()
            return self.configured_host
        s.close()

        # 2. If configured host is localhost / 127.0.0.1, try default WSL2 IP
        for fallback_ip in ["172.17.109.154", "127.0.0.1"]:
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.settimeout(0.5)
            if s2.connect_ex((fallback_ip, self.port)) == 0:
                s2.close()
                logger.info(f"FalkorDB host auto-resolved from {self.configured_host} to live interface {fallback_ip}:{self.port}")
                return fallback_ip
            s2.close()

        # 3. Dynamic lookup via wsl hostname -I if available
        try:
            out = subprocess.check_output(["wsl", "hostname", "-I"], timeout=1.5).decode().strip()
            dynamic_wsl_ip = out.split()[0]
            s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s3.settimeout(0.5)
            if s3.connect_ex((dynamic_wsl_ip, self.port)) == 0:
                s3.close()
                return dynamic_wsl_ip
            s3.close()
        except Exception:
            pass

        return self.configured_host

    def connect(self) -> bool:
        """Establish connection to live FalkorDB graph database."""
        if not FALKORDB_AVAILABLE:
            self.is_connected = False
            self.last_error = "falkordb Python package is missing from environment"
            logger.error(self.last_error)
            return False

        try:
            self.active_host = self._resolve_connection_host()
            self._driver = FalkorDBDriver(
                host=self.active_host,
                port=self.port,
                password=self.password if self.password else None
            )
            self._graph = self._driver.select_graph(self.graph_name)
            # Verify connectivity with real query
            res = self._graph.query("RETURN 1 AS ping")
            if res and res.result_set:
                self.is_connected = True
                self.last_health_check = datetime.utcnow().isoformat()
                self.last_error = None
                logger.info(f"Connected to live FalkorDB server at {self.active_host}:{self.port}, graph: '{self.graph_name}'.")
                return True
        except Exception as e:
            self.is_connected = False
            self.last_error = f"Failed to connect to FalkorDB at {self.active_host}:{self.port}: {str(e)}"
            logger.error(self.last_error)
            return False
        return False

    def check_connection(self) -> bool:
        """Re-verify connection status and reconnect if dropped."""
        if not self.is_connected or not self._graph:
            return self.connect()
        try:
            res = self._graph.query("RETURN 1 AS ping")
            if res and res.result_set:
                self.last_health_check = datetime.utcnow().isoformat()
                return True
        except Exception as e:
            self.is_connected = False
            self.last_error = str(e)
            return self.connect()
        return False

    def query(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Execute an authoritative Cypher query against FalkorDB.
        Raises ConnectionError if the database is unreachable.
        """
        if not self.check_connection():
            raise ConnectionError(f"FalkorDB is offline or disconnected: {self.last_error}")

        # Clean params by serializing complex dicts or None values
        clean_params = None
        if params:
            clean_params = {}
            for k, v in params.items():
                if v is not None:
                    clean_params[str(k)] = serialize_property_value(v)

        try:
            res = self._graph.query(cypher, clean_params)
            return res.result_set if res else []
        except Exception as e:
            logger.error(f"Cypher execution failed on FalkorDB: {e} | Query: {cypher} | Params: {clean_params}")
            raise

    def upsert_node(
        self,
        node_id: str,
        node_type: str,
        label: str,
        properties: Dict[str, Any],
        tenant_id: str = "tenant_nexus_main"
    ) -> Dict[str, Any]:
        """
        Merge/create a node in the live FalkorDB graph.
        """
        if not self.check_connection():
            raise ConnectionError(f"Cannot upsert node; FalkorDB is offline: {self.last_error}")

        # Sanitize node_type as safe Cypher label (alphanumeric only)
        safe_type = re.sub(r'[^a-zA-Z0-9_]', '', node_type) or "Entity"
        str_id = str(node_id)
        clean_props = {k: serialize_property_value(v) for k, v in properties.items()}

        # Build dynamic SET clause for properties
        set_clauses = [
            "n.label = $label",
            "n.tenant_id = $tenant_id",
            "n.type = $node_type",
            "n.updated_at = $updated_at"
        ]
        query_params = {
            "id": str_id,
            "label": str(label),
            "tenant_id": str(tenant_id),
            "node_type": safe_type,
            "updated_at": datetime.utcnow().isoformat()
        }

        for idx, (k, v) in enumerate(clean_props.items()):
            param_key = f"p_{idx}"
            set_clauses.append(f"n.`{k}` = ${param_key}")
            query_params[param_key] = v

        set_stmt = ", ".join(set_clauses)
        cypher = f"MERGE (n:{safe_type} {{id: $id}}) SET {set_stmt} RETURN n"

        res = self.query(cypher, query_params)
        if res and len(res) > 0 and len(res[0]) > 0:
            return normalize_falkor_node(res[0][0])
        return {
            "id": str_id,
            "type": safe_type,
            "label": label,
            "properties": properties,
            "tenant_id": tenant_id
        }

    def upsert_edge(
        self,
        edge_id: str,
        source_id: str,
        target_id: str,
        relation_type: str,
        properties: Optional[Dict[str, Any]] = None,
        tenant_id: str = "tenant_nexus_main"
    ) -> Optional[Dict[str, Any]]:
        """
        Merge/create a relationship edge between two nodes in FalkorDB.
        """
        if not self.check_connection():
            raise ConnectionError(f"Cannot upsert edge; FalkorDB is offline: {self.last_error}")

        safe_rel = re.sub(r'[^a-zA-Z0-9_]', '', relation_type) or "RELATED_TO"
        str_edge_id = str(edge_id)
        props = properties or {}
        clean_props = {k: serialize_property_value(v) for k, v in props.items()}

        set_clauses = [
            "r.tenant_id = $tenant_id",
            "r.type = $rel_type",
            "r.source_id = $source_id",
            "r.target_id = $target_id",
            "r.created_at = $created_at"
        ]
        query_params = {
            "edge_id": str_edge_id,
            "source_id": str(source_id),
            "target_id": str(target_id),
            "rel_type": safe_rel,
            "tenant_id": str(tenant_id),
            "created_at": datetime.utcnow().isoformat()
        }

        for idx, (k, v) in enumerate(clean_props.items()):
            param_key = f"ep_{idx}"
            set_clauses.append(f"r.`{k}` = ${param_key}")
            query_params[param_key] = v

        set_stmt = ", ".join(set_clauses)
        cypher = f"""
        MATCH (a {{id: $source_id}}), (b {{id: $target_id}})
        MERGE (a)-[r:{safe_rel} {{id: $edge_id}}]->(b)
        SET {set_stmt}
        RETURN r
        """
        res = self.query(cypher, query_params)
        if res and len(res) > 0 and len(res[0]) > 0:
            return normalize_falkor_edge(res[0][0])
        return {
            "id": str_edge_id,
            "source": str(source_id),
            "target": str(target_id),
            "type": safe_rel,
            "properties": props,
            "tenant_id": tenant_id
        }

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Fetch entity details by ID directly from FalkorDB."""
        cypher = "MATCH (n {id: $id}) RETURN n LIMIT 1"
        rows = self.query(cypher, {"id": str(node_id)})
        if rows and len(rows) > 0 and len(rows[0]) > 0:
            return normalize_falkor_node(rows[0][0])
        return None

    def get_neighbors(self, node_id: str, depth: int = 1, tenant_id: str = "tenant_nexus_main") -> Dict[str, Any]:
        """
        Retrieve 1-hop or 2-hop graph neighborhood from FalkorDB.
        """
        cypher = """
        MATCH (a {id: $id})-[r]-(b)
        WHERE ($tenant_id = 'all' OR a.tenant_id = $tenant_id)
        RETURN a, r, b
        LIMIT 200
        """
        rows = self.query(cypher, {"id": str(node_id), "tenant_id": tenant_id})
        nodes_dict = {}
        edges_list = []

        # Ensure root node is included
        root_node = self.get_node(node_id)
        if root_node:
            nodes_dict[root_node["id"]] = root_node

        for row in rows:
            if len(row) >= 3:
                a_norm = normalize_falkor_node(row[0])
                r_norm = normalize_falkor_edge(row[1])
                b_norm = normalize_falkor_node(row[2])

                nodes_dict[a_norm["id"]] = a_norm
                nodes_dict[b_norm["id"]] = b_norm
                edges_list.append(r_norm)

        # Deduplicate edges
        seen_edge_ids = set()
        unique_edges = []
        for e in edges_list:
            eid = e.get("id")
            if eid and eid not in seen_edge_ids:
                seen_edge_ids.add(eid)
                unique_edges.append(e)

        return {
            "nodes": list(nodes_dict.values()),
            "edges": unique_edges
        }

    def find_paths(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 4,
        tenant_id: str = "tenant_nexus_main"
    ) -> List[Dict[str, Any]]:
        """
        Find traversal paths between two entities in FalkorDB.
        """
        safe_depth = min(max(1, max_depth), 5)
        cypher = f"""
        MATCH p = (a {{id: $src}})-[*1..{safe_depth}]-(b {{id: $tgt}})
        WHERE ($tenant_id = 'all' OR a.tenant_id = $tenant_id)
        RETURN p
        LIMIT 10
        """
        rows = self.query(cypher, {"src": str(source_id), "tgt": str(target_id), "tenant_id": tenant_id})
        paths = []
        for row in rows:
            path_obj = row[0]
            if hasattr(path_obj, "nodes") and hasattr(path_obj, "edges"):
                raw_nodes = path_obj.nodes() if callable(path_obj.nodes) else path_obj.nodes
                raw_edges = path_obj.edges() if callable(path_obj.edges) else path_obj.edges
                p_nodes = [normalize_falkor_node(n) for n in raw_nodes]
                p_edges = [normalize_falkor_edge(e) for e in raw_edges]
                paths.append({
                    "hop_count": len(p_edges),
                    "nodes": p_nodes,
                    "edges": p_edges,
                    "path_description": " -> ".join([n.get("label", n.get("id")) for n in p_nodes])
                })
        return paths

    def get_stats(self) -> Dict[str, Any]:
        """
        Query FalkorDB directly for exact entity and relationship statistics.
        """
        if not self.check_connection():
            return {
                "is_connected_to_live_falkordb": False,
                "engine_mode": "disconnected",
                "graph_name": self.graph_name,
                "total_nodes": 0,
                "total_edges": 0,
                "node_counts_by_type": {},
                "edge_counts_by_type": {},
                "error": self.last_error
            }

        try:
            # 1. Total nodes
            n_res = self.query("MATCH (n) RETURN count(n) AS cnt")
            total_nodes = n_res[0][0] if n_res and n_res[0] else 0

            # 2. Total edges
            e_res = self.query("MATCH ()-[r]->() RETURN count(r) AS cnt")
            total_edges = e_res[0][0] if e_res and e_res[0] else 0

            # 3. Node distribution by label
            node_counts = {}
            nl_res = self.query("MATCH (n) RETURN labels(n)[0] AS lbl, count(n) AS cnt")
            for row in nl_res:
                if len(row) >= 2 and row[0]:
                    node_counts[str(row[0])] = int(row[1])

            # 4. Edge distribution by relation type
            edge_counts = {}
            el_res = self.query("MATCH ()-[r]->() RETURN type(r) AS rel, count(r) AS cnt")
            for row in el_res:
                if len(row) >= 2 and row[0]:
                    edge_counts[str(row[0])] = int(row[1])

            return {
                "is_connected_to_live_falkordb": True,
                "engine_mode": "live_falkordb",
                "graph_name": self.graph_name,
                "host": self.active_host,
                "port": self.port,
                "total_nodes": total_nodes,
                "total_edges": total_edges,
                "node_counts_by_type": node_counts,
                "edge_counts_by_type": edge_counts,
                "last_health_check": self.last_health_check
            }
        except Exception as e:
            logger.error(f"Error fetching stats from live FalkorDB: {e}")
            return {
                "is_connected_to_live_falkordb": False,
                "engine_mode": "live_falkordb_error",
                "graph_name": self.graph_name,
                "total_nodes": 0,
                "total_edges": 0,
                "node_counts_by_type": {},
                "edge_counts_by_type": {},
                "error": str(e)
            }

    def health(self) -> Dict[str, Any]:
        """
        Execute real diagnostic health check against FalkorDB.
        """
        start_t = time.time()
        try:
            is_conn = self.check_connection()
            if not is_conn:
                return {
                    "status": "unavailable",
                    "connected": False,
                    "host": self.active_host,
                    "port": self.port,
                    "graph_name": self.graph_name,
                    "error": self.last_error or "Could not connect to FalkorDB server",
                    "timestamp": datetime.utcnow().isoformat()
                }

            res = self.query("RETURN 1 AS ping")
            latency_ms = round((time.time() - start_t) * 1000, 2)
            stats = self.get_stats()

            return {
                "status": "connected",
                "connected": True,
                "host": self.active_host,
                "port": self.port,
                "graph_name": self.graph_name,
                "query_success": True,
                "latency_ms": latency_ms,
                "total_nodes": stats["total_nodes"],
                "total_edges": stats["total_edges"],
                "node_distribution": stats["node_counts_by_type"],
                "edge_distribution": stats["edge_counts_by_type"],
                "last_health_check": datetime.utcnow().isoformat()
            }
        except Exception as e:
            latency_ms = round((time.time() - start_t) * 1000, 2)
            return {
                "status": "error",
                "connected": False,
                "host": self.active_host,
                "port": self.port,
                "graph_name": self.graph_name,
                "query_success": False,
                "latency_ms": latency_ms,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def clear(self):
        """Delete all nodes and edges in the live FalkorDB graph."""
        if not self.check_connection():
            raise ConnectionError(f"Cannot clear graph; FalkorDB is offline: {self.last_error}")
        self.query("MATCH (n) DETACH DELETE n")
        logger.info(f"Cleared all entities and relationships in live FalkorDB graph '{self.graph_name}'.")
