import subprocess
import json
from falkordb import FalkorDB

def get_wsl_ip():
    try:
        out = subprocess.check_output(["wsl", "hostname", "-I"], text=True)
        return out.strip().split()[0]
    except Exception:
        return "127.0.0.1"

def main():
    host = get_wsl_ip()
    print(f"Connecting to FalkorDB on {host}:6379...")
    db = FalkorDB(host=host, port=6379)
    g = db.select_graph("nexus_company_graph")
    
    # Clean test
    g.query("MATCH (n:TestPerson) DETACH DELETE n")
    
    # Create test nodes and relation
    create_res = g.query("CREATE (p:TestPerson {id: 'p1', name: 'Alice', role: 'Engineer'})-[:OWNS {since: '2025'}]->(pr:TestProject {id: 'proj1', name: 'Atlas'})")
    print("Created test entities:", create_res.result_set)
    
    # Query back
    q_res = g.query("MATCH (p:TestPerson)-[r:OWNS]->(pr:TestProject) RETURN p, r, pr")
    row = q_res.result_set[0]
    p_node, edge, pr_node = row[0], row[1], row[2]
    
    print("Node class:", type(p_node))
    print("Node labels:", p_node.labels)
    print("Node properties:", p_node.properties)
    print("Edge relation:", edge.relation)
    print("Edge properties:", edge.properties)
    
    # Clean up test nodes
    g.query("MATCH (n:TestPerson) DETACH DELETE n")
    g.query("MATCH (n:TestProject) DETACH DELETE n")
    print("Cleaned up test nodes. REAL FALKORDB TEST PASSED COMPLETELY!")

if __name__ == "__main__":
    main()
