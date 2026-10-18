// ==============================================================================
// NEXUS GRAPH AI - FALKORDB CYPHER SCHEMA DEFINITIONS
// Graph Name: nexus_company_graph
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. INDEX DEFINITIONS FOR LOW-LATENCY LOOKUPS
// ------------------------------------------------------------------------------

CREATE INDEX FOR (c:Company) ON (c.id);
CREATE INDEX FOR (d:Department) ON (d.id);
CREATE INDEX FOR (t:Team) ON (t.id);
CREATE INDEX FOR (p:Person) ON (p.id);
CREATE INDEX FOR (p:Person) ON (p.email);
CREATE INDEX FOR (pr:Project) ON (pr.id);
CREATE INDEX FOR (pr:Project) ON (pr.code);
CREATE INDEX FOR (doc:Document) ON (doc.id);
CREATE INDEX FOR (tik:Ticket) ON (tik.id);
CREATE INDEX FOR (tik:Ticket) ON (tik.key);
CREATE INDEX FOR (m:Meeting) ON (m.id);
CREATE INDEX FOR (dec:Decision) ON (dec.id);
CREATE INDEX FOR (tsk:Task) ON (tsk.id);
CREATE INDEX FOR (inc:Incident) ON (inc.id);
CREATE INDEX FOR (sec:SecurityEvent) ON (sec.id);
CREATE INDEX FOR (ag:Agent) ON (ag.id);
CREATE INDEX FOR (mem:Memory) ON (mem.id);
CREATE INDEX FOR (s:Source) ON (s.id);

// ------------------------------------------------------------------------------
// 2. TENANT ISOLATION INDEXES
// ------------------------------------------------------------------------------

CREATE INDEX FOR (n:Person) ON (n.tenant_id);
CREATE INDEX FOR (n:Project) ON (n.tenant_id);
CREATE INDEX FOR (n:Document) ON (n.tenant_id);
CREATE INDEX FOR (n:Memory) ON (n.tenant_id);
CREATE INDEX FOR (n:Task) ON (n.tenant_id);

// ------------------------------------------------------------------------------
// 3. NODE LABELS AND MANDATORY PROPERTIES
// ------------------------------------------------------------------------------
// (:Company {id, name, domain, headquarters, founded, tenant_id})
// (:Department {id, name, code, head, budget, tenant_id})
// (:Team {id, name, department_id, charter, tenant_id})
// (:Person {id, name, email, role, department_id, security_clearance, tenant_id})
// (:Project {id, name, code, status, risk_level, target_date, tenant_id})
// (:Document {id, title, version, status, classification, last_updated, tenant_id})
// (:Ticket {id, key, title, status, severity, created_at, tenant_id})
// (:Meeting {id, title, date, summary, tenant_id})
// (:Decision {id, title, status, decided_at, rationale, tenant_id})
// (:Task {id, title, status, priority, due_date, tenant_id})
// (:Incident {id, title, status, severity, detected_at, tenant_id})
// (:SecurityEvent {id, event_type, severity, timestamp, ip_address, resource, tenant_id})
// (:Agent {id, name, role, description, status, tenant_id})
// (:Memory {id, type, summary, confidence, verified, tenant_id})
// (:Source {id, name, uri, hash, ingested_at, tenant_id})

// ------------------------------------------------------------------------------
// 4. RELATIONSHIP TYPES
// ------------------------------------------------------------------------------
// (:Person)-[:MEMBER_OF]->(:Team)
// (:Team)-[:MEMBER_OF]->(:Department)
// (:Department)-[:MEMBER_OF]->(:Company)
// (:Person)-[:MANAGES]->(:Person)
// (:Person)-[:OWNS]->(:Project)
// (:Person)-[:WORKS_ON]->(:Project)
// (:Project)-[:BLOCKED_BY]->(:Decision)
// (:Project)-[:DEPENDS_ON]->(:Project)
// (:Decision)-[:SUPPORTED_BY]->(:Document)
// (:Decision)-[:DISCUSSED_IN]->(:Meeting)
// (:Document)-[:SUPERSEDES]->(:Document)
// (:Document)-[:DERIVED_FROM]->(:Source)
// (:Ticket)-[:RELATED_TO]->(:Project)
// (:Ticket)-[:RELATED_TO]->(:Incident)
// (:Ticket)-[:ASSIGNED_TO]->(:Person)
// (:SecurityEvent)-[:LINKED_TO]->(:Incident)
// (:SecurityEvent)-[:LINKED_TO]->(:Ticket)
// (:SecurityEvent)-[:LINKED_TO]->(:Project)
// (:Task)-[:ASSIGNED_TO]->(:Person)
// (:Task)-[:DEPENDS_ON]->(:Task)
// (:Agent)-[:REMEMBERS]->(:Memory)
// (:Agent)-[:HANDOFF_TO]->(:Agent)
