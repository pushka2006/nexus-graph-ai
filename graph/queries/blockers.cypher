// ==============================================================================
// Parameterized Cypher Query: Project Blocker & Dependency Traversal
// Track 03: Company Brain Scene 1
// ==============================================================================

MATCH (proj:Project {id: $project_id})-[r:BLOCKED_BY]->(blocker:Decision)
OPTIONAL MATCH (decider:Person)-[:OWNS]->(blocker)
OPTIONAL MATCH (blocker)-[:SUPPORTED_BY]->(doc:Document)
OPTIONAL MATCH (doc)-[:SUPERSEDES]->(superseded_doc:Document)
WHERE proj.tenant_id = $tenant_id
RETURN 
  proj.name AS project_name,
  proj.status AS project_status,
  blocker.id AS blocker_id,
  blocker.title AS blocker_title,
  blocker.rationale AS blocker_rationale,
  decider.name AS decider_name,
  decider.email AS decider_email,
  doc.title AS policy_title,
  doc.version AS policy_version,
  superseded_doc.title AS superseded_policy_title;
