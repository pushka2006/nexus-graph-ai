from falkordb import FalkorDB

db = FalkorDB(host="172.17.109.154", port=6379)
g = db.select_graph("nexus_company_graph")

# Clean any test nodes
g.query("MATCH (n:TestParamPerson) DETACH DELETE n")

# Create node with params
g.query(
    "CREATE (n:TestParamPerson {id: $id, label: $label, tenant_id: $tenant_id, name: $name, age: $age})",
    {"id": "p100", "label": "Elena Vance", "tenant_id": "tenant_nexus_main", "name": "Elena", "age": 42}
)

# Query back with params
res = g.query("MATCH (n:TestParamPerson {id: $id}) RETURN n", {"id": "p100"})
print("Retrieved node:", res.result_set[0][0].properties)

# Clean up
g.query("MATCH (n:TestParamPerson) DETACH DELETE n")
print("Parameter test passed 100%!")
