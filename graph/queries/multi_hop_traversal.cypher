// ==============================================================================
// Allowlisted Parameterized Cypher Queries: Multi-Hop Traversals & Paths
// ==============================================================================

// 1. Multi-Hop Shortest Path between Source and Target Entity
MATCH p = shortestPath((a {id: $source_id})-[*..5]-(b {id: $target_id}))
WHERE a.tenant_id = $tenant_id AND b.tenant_id = $tenant_id
RETURN p;

// 2. Expand Entity Neighborhood by 1 Hop
MATCH (n {id: $entity_id})-[r]-(neighbor)
WHERE n.tenant_id = $tenant_id
RETURN n, r, neighbor;

// 3. Expand Entity Neighborhood by 2 Hops
MATCH (n {id: $entity_id})-[r1]-(mid)-[r2]-(outer)
WHERE n.tenant_id = $tenant_id
RETURN n, r1, mid, r2, outer;

// 4. Entity Lookup with Scoped Properties
MATCH (n)
WHERE n.id = $entity_id AND (n.tenant_id = $tenant_id OR $tenant_id = 'all')
RETURN n;
