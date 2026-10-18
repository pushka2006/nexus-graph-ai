// ==============================================================================
// NEXUS GRAPH AI - STANDALONE FALKORDB SEED STATEMENTS
// Direct Cypher initialization for NexusWorks synthetic knowledge graph
// ==============================================================================

// 1. Company
MERGE (c:Company {id: 'comp_nexus'})
SET c.name = 'NexusWorks Technologies Inc.',
    c.domain = 'nexusworks.ai',
    c.headquarters = 'San Francisco, CA',
    c.founded = 2022,
    c.tenant_id = 'tenant_nexus_main';

// 2. Departments
MERGE (d1:Department {id: 'dept_eng'})
SET d1.name = 'Engineering', d1.code = 'ENG', d1.head = 'Dr. Aris Thorne', d1.budget = 12000000, d1.tenant_id = 'tenant_nexus_main';
MERGE (d2:Department {id: 'dept_prod'})
SET d2.name = 'Product Management', d2.code = 'PROD', d2.head = 'Elena Vance', d2.budget = 4500000, d2.tenant_id = 'tenant_nexus_main';
MERGE (d3:Department {id: 'dept_sec'})
SET d3.name = 'Cybersecurity & Governance', d3.code = 'SEC', d3.head = 'Kaelen Voss', d3.budget = 3800000, d3.tenant_id = 'tenant_nexus_main';
MERGE (d4:Department {id: 'dept_ops'})
SET d4.name = 'Cloud Infrastructure & Ops', d4.code = 'OPS', d4.head = 'Siddharth Rao', d4.budget = 5200000, d4.tenant_id = 'tenant_nexus_main';
MERGE (d5:Department {id: 'dept_legal'})
SET d5.name = 'Legal & Compliance', d5.code = 'LEGAL', d5.head = 'Nadia Al-Mansoor', d5.budget = 2100000, d5.tenant_id = 'tenant_nexus_main';
MERGE (d6:Department {id: 'dept_cs'})
SET d6.name = 'Customer Success & Support', d6.code = 'CS', d6.head = 'Claire Sterling', d6.budget = 3100000, d6.tenant_id = 'tenant_nexus_main';

// 3. Key Projects
MERGE (p1:Project {id: 'proj_atlas'})
SET p1.name = 'Project Atlas', p1.code = 'ATLAS', p1.status = 'in_progress', p1.risk_level = 'critical', p1.target_date = '2026-11-15', p1.tenant_id = 'tenant_nexus_main';

MERGE (p2:Project {id: 'proj_beacon'})
SET p2.name = 'Project Beacon', p2.code = 'BEACON', p2.status = 'completed', p2.risk_level = 'low', p2.target_date = '2026-08-01', p2.tenant_id = 'tenant_nexus_main';

// 4. Key Decisions & Blockers
MERGE (dec:Decision {id: 'dec_104'})
SET dec.title = 'AD-104: Project Atlas Production Gate and Cloud Storage Migration',
    dec.status = 'pending_approval',
    dec.decided_at = '2026-10-05',
    dec.rationale = 'Blocks Project Atlas release v1.0 due to unverified S3 bucket encryption compliance.',
    dec.tenant_id = 'tenant_nexus_main';

MERGE (p1)-[:BLOCKED_BY {reason: 'Unapproved cloud storage encryption architecture', severity: 'critical', tenant_id: 'tenant_nexus_main'}]->(dec);

// 5. Conflicting Policies (Supersession)
MERGE (doc1:Document {id: 'doc_sec_pol_v20'})
SET doc1.title = 'Information Security Policy v2.0 (Mandatory Cloud Encryption)',
    doc1.version = 'v2.0',
    doc1.status = 'current',
    doc1.tenant_id = 'tenant_nexus_main';

MERGE (doc2:Document {id: 'doc_sec_pol_v12'})
SET doc2.title = 'Information Security Policy v1.2',
    doc2.version = 'v1.2',
    doc2.status = 'superseded',
    doc2.tenant_id = 'tenant_nexus_main';

MERGE (doc1)-[:SUPERSEDES {rationale: 'Updated compliance requirements for cloud encryption and KMS mandates.', tenant_id: 'tenant_nexus_main'}]->(doc2);
MERGE (dec)-[:SUPPORTED_BY {tenant_id: 'tenant_nexus_main'}]->(doc1);

// 6. Security Event & Correlation
MERGE (sec:SecurityEvent {id: 'sec_014'})
SET sec.title = 'SEC-014: Abnormal Token Generation with Admin Privilege Escalation',
    sec.event_type = 'privilege_escalation',
    sec.severity = 'critical',
    sec.timestamp = '2026-10-17T08:14:22Z',
    sec.ip_address = '10.0.4.152',
    sec.resource = 'svc-atlas-worker',
    sec.tenant_id = 'tenant_nexus_main';

MERGE (inc:Incident {id: 'inc_08'})
SET inc.title = 'INC-08: Suspicious Service Account Impersonation on Atlas Internal Bus',
    inc.status = 'active',
    inc.severity = 'critical',
    inc.tenant_id = 'tenant_nexus_main';

MERGE (tik:Ticket {id: 'tik_204'})
SET tik.key = 'TIK-204',
    tik.title = 'TIK-204: Unauthorized Internal Service Token Generation on Atlas Microservice',
    tik.status = 'open',
    tik.severity = 'critical',
    tik.tenant_id = 'tenant_nexus_main';

MERGE (sec)-[:LINKED_TO {tenant_id: 'tenant_nexus_main'}]->(inc);
MERGE (sec)-[:LINKED_TO {tenant_id: 'tenant_nexus_main'}]->(tik);
MERGE (sec)-[:LINKED_TO {tenant_id: 'tenant_nexus_main'}]->(p1);
MERGE (tik)-[:RELATED_TO {tenant_id: 'tenant_nexus_main'}]->(inc);
MERGE (tik)-[:RELATED_TO {tenant_id: 'tenant_nexus_main'}]->(p1);
