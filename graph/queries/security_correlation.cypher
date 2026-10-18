// ==============================================================================
// Parameterized Cypher Query: Security Anomaly Incident Correlation
// Track 01: Connected Data Scene 2
// ==============================================================================

MATCH (sec:SecurityEvent {id: $event_id})-[r1:LINKED_TO]->(inc:Incident)
OPTIONAL MATCH (tik:Ticket)-[r2:RELATED_TO]->(inc)
OPTIONAL MATCH (tik)-[r3:RELATED_TO]->(proj:Project)
OPTIONAL MATCH (inc)-[:REPORTED_BY]->(reporter:Person)
OPTIONAL MATCH (tik)-[:ASSIGNED_TO]->(assignee:Person)
WHERE sec.tenant_id = $tenant_id
RETURN 
  sec.id AS event_id,
  sec.event_type AS event_type,
  sec.severity AS severity,
  sec.resource AS affected_resource,
  inc.id AS incident_id,
  inc.title AS incident_title,
  tik.key AS ticket_key,
  tik.title AS ticket_title,
  proj.name AS affected_project,
  assignee.name AS responder_name,
  assignee.email AS responder_email;
