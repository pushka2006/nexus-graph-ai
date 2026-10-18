import hashlib
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta

def generate_nexusworks_data() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generates deterministic synthetic enterprise data for NexusWorks.
    Guarantees:
    - >= 30 Employees (Person)
    - >= 6 Departments
    - >= 10 Projects
    - >= 50 Documents
    - >= 40 Tickets
    - >= 20 Meetings
    - >= 25 Decisions
    - >= 20 Tasks
    - >= 15 Security / Operational Events
    - Plus Company, Teams, Agents, Memories, Sources
    """
    nodes = []
    edges = []

    def add_node(node_id: str, node_type: str, label: str, properties: Dict[str, Any], tenant_id: str = "tenant_nexus_main"):
        nodes.append({
            "id": node_id,
            "type": node_type,
            "label": label,
            "properties": properties,
            "tenant_id": tenant_id
        })

    def add_edge(edge_id: str, source_id: str, target_id: str, relation_type: str, properties: Dict[str, Any] = None, tenant_id: str = "tenant_nexus_main"):
        edges.append({
            "id": edge_id,
            "source": source_id,
            "target": target_id,
            "type": relation_type,
            "properties": properties or {},
            "tenant_id": tenant_id
        })

    # 1. Company
    add_node("comp_nexus", "Company", "NexusWorks Technologies Inc.", {
        "name": "NexusWorks Technologies Inc.",
        "domain": "nexusworks.ai",
        "headquarters": "San Francisco, CA",
        "founded": 2022,
        "is_synthetic": True
    })

    # 2. Departments (6 departments)
    departments = [
        ("dept_eng", "Engineering", "ENG", "Dr. Aris Thorne", 12000000),
        ("dept_prod", "Product Management", "PROD", "Elena Vance", 4500000),
        ("dept_sec", "Cybersecurity & Governance", "SEC", "Kaelen Voss", 3800000),
        ("dept_ops", "Cloud Infrastructure & Ops", "OPS", "Siddharth Rao", 5200000),
        ("dept_legal", "Legal & Compliance", "LEGAL", "Nadia Al-Mansoor", 2100000),
        ("dept_cs", "Customer Success & Support", "CS", "Claire Sterling", 3100000)
    ]
    for d_id, name, code, head, budget in departments:
        add_node(d_id, "Department", name, {
            "name": name,
            "code": code,
            "head": head,
            "budget": budget,
            "is_synthetic": True
        })
        add_edge(f"rel_{d_id}_comp", d_id, "comp_nexus", "MEMBER_OF")

    # 3. Teams (8 teams)
    teams = [
        ("team_core_eng", "Core Platform Team", "dept_eng"),
        ("team_ai_ml", "Applied AI & Graph Systems", "dept_eng"),
        ("team_secops", "Security Operations (SecOps)", "dept_sec"),
        ("team_cloud_infra", "Kubernetes & Cloud Infra", "dept_ops"),
        ("team_app_sec", "Application Security & IAM", "dept_sec"),
        ("team_prod_atlas", "Project Atlas Product Guild", "dept_prod"),
        ("team_legal_audit", "Risk & Policy Audit", "dept_legal"),
        ("team_tier2_support", "Tier 2 Technical Support", "dept_cs")
    ]
    for t_id, name, dept_id in teams:
        add_node(t_id, "Team", name, {
            "name": name,
            "department_id": dept_id,
            "charter": f"Drive execution and operations for {name}",
            "is_synthetic": True
        })
        add_edge(f"rel_{t_id}_{dept_id}", t_id, dept_id, "MEMBER_OF")

    # 4. Employees (32 Employees)
    employees = [
        ("emp_01", "Dr. Aris Thorne", "aris.thorne@nexusworks.ai", "VP of Engineering", "dept_eng", "team_core_eng", "top_secret"),
        ("emp_02", "Elena Vance", "elena.vance@nexusworks.ai", "Chief Product Officer", "dept_prod", "team_prod_atlas", "top_secret"),
        ("emp_03", "Kaelen Voss", "kaelen.voss@nexusworks.ai", "Chief Information Security Officer", "dept_sec", "team_secops", "top_secret"),
        ("emp_04", "Siddharth Rao", "siddharth.rao@nexusworks.ai", "Director of Cloud Operations", "dept_ops", "team_cloud_infra", "secret"),
        ("emp_05", "Nadia Al-Mansoor", "nadia.mansoor@nexusworks.ai", "General Counsel", "dept_legal", "team_legal_audit", "secret"),
        ("emp_06", "Claire Sterling", "claire.sterling@nexusworks.ai", "VP Customer Success", "dept_cs", "team_tier2_support", "confidential"),
        ("emp_07", "Marcus Chen", "marcus.chen@nexusworks.ai", "Principal Infrastructure Architect", "dept_eng", "team_core_eng", "secret"),
        ("emp_08", "Aria Song", "aria.song@nexusworks.ai", "Lead AI Graph Engineer", "dept_eng", "team_ai_ml", "secret"),
        ("emp_09", "Zack Brody", "zack.brody@nexusworks.ai", "Senior SecOps Incident Handler", "dept_sec", "team_secops", "secret"),
        ("emp_10", "Devon Park", "devon.park@nexusworks.ai", "Staff Backend Developer", "dept_eng", "team_core_eng", "confidential"),
        ("emp_11", "Maya Lin", "maya.lin@nexusworks.ai", "Principal Product Manager - Atlas", "dept_prod", "team_prod_atlas", "secret"),
        ("emp_12", "Tobias Wolfe", "tobias.wolfe@nexusworks.ai", "Senior DevOps Engineer", "dept_ops", "team_cloud_infra", "secret"),
        ("emp_13", "Leila Hosseini", "leila.hosseini@nexusworks.ai", "Compliance Officer", "dept_legal", "team_legal_audit", "confidential"),
        ("emp_14", "Rajesh Patel", "rajesh.patel@nexusworks.ai", "Senior Security Engineer (IAM)", "dept_sec", "team_app_sec", "secret"),
        ("emp_15", "Samantha Grey", "samantha.grey@nexusworks.ai", "Tier 2 Support Lead", "dept_cs", "team_tier2_support", "confidential"),
        ("emp_16", "Liam O'Connor", "liam.oconnor@nexusworks.ai", "Senior Frontend Engineer", "dept_eng", "team_core_eng", "confidential"),
        ("emp_17", "Fiona Gallagher", "fiona.gallagher@nexusworks.ai", "ML Evaluation Engineer", "dept_eng", "team_ai_ml", "confidential"),
        ("emp_18", "Tariq Mansour", "tariq.mansour@nexusworks.ai", "Site Reliability Engineer", "dept_ops", "team_cloud_infra", "secret"),
        ("emp_19", "Chloe Bennett", "chloe.bennett@nexusworks.ai", "Associate Product Manager", "dept_prod", "team_prod_atlas", "confidential"),
        ("emp_20", "Julian Hayes", "julian.hayes@nexusworks.ai", "Penetration Tester", "dept_sec", "team_secops", "secret"),
        ("emp_21", "Nina Rodriguez", "nina.rodriguez@nexusworks.ai", "Data Engineer", "dept_eng", "team_ai_ml", "confidential"),
        ("emp_22", "Victor Vance", "victor.vance@nexusworks.ai", "Database Administrator (FalkorDB/PG)", "dept_ops", "team_cloud_infra", "secret"),
        ("emp_23", "Ananya Sharma", "ananya.sharma@nexusworks.ai", "Privacy Counsel", "dept_legal", "team_legal_audit", "secret"),
        ("emp_24", "Lucas Scott", "lucas.scott@nexusworks.ai", "Customer Escalation Specialist", "dept_cs", "team_tier2_support", "confidential"),
        ("emp_25", "Hanna Lindqvist", "hanna.lindqvist@nexusworks.ai", "Full Stack Developer", "dept_eng", "team_core_eng", "confidential"),
        ("emp_26", "Owen Cooper", "owen.cooper@nexusworks.ai", "Platform Security Analyst", "dept_sec", "team_app_sec", "secret"),
        ("emp_27", "Priya Nair", "priya.nair@nexusworks.ai", "Technical Technical Writer", "dept_prod", "team_prod_atlas", "confidential"),
        ("emp_28", "Dmitri Volkov", "dmitri.volkov@nexusworks.ai", "Distributed Systems Engineer", "dept_eng", "team_core_eng", "secret"),
        ("emp_29", "Sarah Jenkins", "sarah.jenkins@nexusworks.ai", "Support Engineer", "dept_cs", "team_tier2_support", "confidential"),
        ("emp_30", "Gwen Stacy", "gwen.stacy@nexusworks.ai", "Quality Assurance Lead", "dept_eng", "team_core_eng", "confidential"),
        ("emp_31", "Kenneth Clarke", "kenneth.clarke@nexusworks.ai", "SOC Analyst Tier 1", "dept_sec", "team_secops", "confidential"),
        ("emp_32", "Jessica Taylor", "jessica.taylor@nexusworks.ai", "Infrastructure Automation Engineer", "dept_ops", "team_cloud_infra", "secret")
    ]
    for e_id, name, email, role, dept_id, team_id, clearance in employees:
        add_node(e_id, "Person", name, {
            "name": name,
            "email": email,
            "role": role,
            "department_id": dept_id,
            "team_id": team_id,
            "security_clearance": clearance,
            "is_synthetic": True
        })
        add_edge(f"rel_{e_id}_{team_id}", e_id, team_id, "MEMBER_OF")
        add_edge(f"rel_{e_id}_{dept_id}", e_id, dept_id, "MEMBER_OF")

    # Management hierarchy
    add_edge("man_01_07", "emp_01", "emp_07", "MANAGES")
    add_edge("man_01_08", "emp_01", "emp_08", "MANAGES")
    add_edge("man_01_10", "emp_01", "emp_10", "MANAGES")
    add_edge("man_02_11", "emp_02", "emp_11", "MANAGES")
    add_edge("man_03_09", "emp_03", "emp_09", "MANAGES")
    add_edge("man_03_14", "emp_03", "emp_14", "MANAGES")
    add_edge("man_04_12", "emp_04", "emp_12", "MANAGES")

    # 5. Projects (10 projects)
    projects = [
        ("proj_atlas", "Project Atlas", "ATLAS", "in_progress", "critical", "emp_11", "team_prod_atlas", "2026-11-15"),
        ("proj_beacon", "Project Beacon", "BEACON", "completed", "low", "emp_07", "team_core_eng", "2026-08-01"),
        ("proj_cipher", "Project Cipher", "CIPHER", "in_progress", "high", "emp_03", "team_secops", "2026-12-01"),
        ("proj_dynasty", "Project Dynasty", "DYNASTY", "planning", "medium", "emp_08", "team_ai_ml", "2027-02-15"),
        ("proj_echo", "Project Echo", "ECHO", "in_progress", "medium", "emp_04", "team_cloud_infra", "2026-10-30"),
        ("proj_falcon", "Project Falcon", "FALCON", "completed", "low", "emp_10", "team_core_eng", "2026-07-15"),
        ("proj_genesis", "Project Genesis", "GENESIS", "in_progress", "high", "emp_01", "team_core_eng", "2026-12-31"),
        ("proj_horizon", "Project Horizon", "HORIZON", "planning", "low", "emp_06", "team_tier2_support", "2027-03-01"),
        ("proj_iris", "Project Iris", "IRIS", "in_progress", "critical", "emp_14", "team_app_sec", "2026-11-30"),
        ("proj_jupiter", "Project Jupiter", "JUPITER", "paused", "high", "emp_12", "team_cloud_infra", "2027-01-20")
    ]
    for p_id, name, code, status, risk, owner_id, team_id, target in projects:
        add_node(p_id, "Project", name, {
            "name": name,
            "code": code,
            "status": status,
            "risk_level": risk,
            "owner_id": owner_id,
            "team_id": team_id,
            "target_date": target,
            "description": f"Strategic corporate initiative: {name} ({code})",
            "is_synthetic": True
        })
        add_edge(f"own_{owner_id}_{p_id}", owner_id, p_id, "OWNS")
        add_edge(f"rel_{team_id}_{p_id}", team_id, p_id, "WORKS_ON")

    # Project Atlas specific relations: Marcus Chen and Aria Song work on Atlas
    add_edge("work_07_atlas", "emp_07", "proj_atlas", "WORKS_ON")
    add_edge("work_08_atlas", "emp_08", "proj_atlas", "WORKS_ON")

    # 6. Key Decisions (26 Decisions)
    # Scenario: Project Atlas is BLOCKED by architecture decision AD-104 awaiting approval from Elena Vance and Aris Thorne
    decisions = [
        ("dec_101", "AD-101: Graph Database Selection for Enterprise Mesh", "approved", "2026-03-10", "Select FalkorDB as primary graph database for low-latency Cypher queries.", "emp_07", "proj_beacon"),
        ("dec_102", "AD-102: Token Security and mTLS Protocol", "approved", "2026-04-12", "Enforce SPIFFE/SPIRE for inter-service communication.", "emp_14", "proj_cipher"),
        ("dec_103", "AD-103: Multi-Region Kubernetes Failover", "approved", "2026-05-18", "Deploy active-passive cluster across us-east and us-west.", "emp_04", "proj_echo"),
        ("dec_104", "AD-104: Project Atlas Production Gate and Cloud Storage Migration", "pending_approval", "2026-10-05", "Pending sign-off from VP Engineering and CPO. Blocks Project Atlas release v1.0 due to unverified S3 bucket encryption compliance.", "emp_07", "proj_atlas"),
        ("dec_105", "AD-105: Deprecation of Legacy JWT Secret Rotation", "approved", "2026-06-20", "Deprecate static HMAC secrets in favor of RS256 JWKS.", "emp_03", "proj_cipher"),
        ("dec_106", "AD-106: Vector Retrival Pipeline Framework", "approved", "2026-07-02", "Adopt sentence-transformers/all-MiniLM-L6-v2 for semantic text embeddings.", "emp_08", "proj_atlas"),
        ("dec_107", "AD-107: Incident Response Escalation SLA", "approved", "2026-01-15", "All P1 security incidents require triage within 15 minutes.", "emp_09", "proj_cipher"),
        ("dec_108", "AD-108: Customer Data Retention Policy", "approved", "2026-02-10", "Enforce 90-day retention on debug logs containing PII.", "emp_13", "proj_beacon"),
        ("dec_109", "AD-109: External Tool Execution Guardrails", "approved", "2026-08-11", "Autonomous agents require human authorization before state-changing side effects.", "emp_02", "proj_atlas"),
        ("dec_110", "AD-110: Cross-Tenant Isolation Protocol", "approved", "2026-08-25", "Mandatory tenant_id scoping on every Cypher query and SQL statement.", "emp_01", "proj_genesis"),
    ]
    # Add 16 more decisions to reach 26 decisions
    for i in range(11, 27):
        dec_id = f"dec_{100+i}"
        decisions.append((dec_id, f"AD-{100+i}: System Architecture Evolution Step {i}", "approved" if i % 4 != 0 else "in_review", f"2026-0{min(9, i % 9 + 1)}-15", f"Documented architecture rationale for subsystem {i}", "emp_07", "proj_genesis"))

    for d_id, title, status, date, rationale, decider, p_id in decisions:
        add_node(d_id, "Decision", title, {
            "title": title,
            "status": status,
            "decided_at": date,
            "rationale": rationale,
            "decider_id": decider,
            "project_id": p_id,
            "is_synthetic": True
        })
        add_edge(f"rel_{d_id}_{p_id}", d_id, p_id, "SUPPORTED_BY")
        add_edge(f"own_{decider}_{d_id}", decider, d_id, "OWNS")

    # CRITICAL TRACK SCENARIO: Project Atlas is BLOCKED_BY dec_104
    add_edge("block_atlas_dec104", "proj_atlas", "dec_104", "BLOCKED_BY", {
        "reason": "Unapproved cloud storage encryption architecture",
        "severity": "critical"
    })

    # 7. Documents & Policies (52 Documents)
    # Scenario: doc_sec_pol_v12 is SUPERSEDED by doc_sec_pol_v20
    docs = [
        ("doc_sec_pol_v12", "Information Security Policy v1.2", "v1.2", "superseded", "internal", "2024-06-15", "Allows standard S3 buckets for non-confidential project artifacts without server-side KMS keys."),
        ("doc_sec_pol_v20", "Information Security Policy v2.0 (Mandatory Cloud Encryption)", "v2.0", "current", "confidential", "2026-09-01", "SUPERSEDES v1.2. Strictly requires customer-managed KMS keys (CMK) on all S3 buckets and data stores. Prohibits any deployment with unencrypted storage."),
        ("doc_atlas_prd", "Project Atlas Product Requirements Document (PRD)", "v3.1", "current", "internal", "2026-09-20", "Defines the core goals of Project Atlas: Unified multi-tenant AI graph engine with real-time enterprise intelligence."),
        ("doc_atlas_arch", "Project Atlas Technical Architecture & Data Pipeline", "v2.4", "current", "internal", "2026-10-01", "Architecture blueprint specifying FalkorDB graph clusters, FastAPI microservices, and Qwen2.5-3B model routing."),
        ("doc_incident_runbook", "SecOps Incident Response Runbook P1/P2", "v4.0", "current", "restricted", "2026-08-10", "Step-by-step procedures for isolating rogue service tokens, rotating API keys, and initiating graph audit investigations."),
        ("doc_emp_handbook", "NexusWorks Employee Guidelines and Code of Conduct", "v1.0", "current", "public", "2025-01-10", "NexusWorks corporate culture, remote work policies, and ethical AI principles."),
        ("doc_gdpr_compliance", "GDPR & CCPA Data Subject Access Request Framework", "v2.1", "current", "confidential", "2026-04-14", "Legal obligations for handling customer privacy and memory purging across multi-agent systems.")
    ]
    # Add 45 more documents to reach 52 documents
    for i in range(8, 53):
        doc_id = f"doc_spec_{i}"
        docs.append((doc_id, f"Engineering Specification {i}: Subsystem Design Document", "v1.0", "current", "internal", f"2026-0{min(9, (i%9)+1)}-10", f"Detailed technical guidelines and interface specifications for module {i}."))

    for doc_id, title, ver, status, classif, date, passage in docs:
        add_node(doc_id, "Document", title, {
            "title": title,
            "version": ver,
            "status": status,
            "classification": classif,
            "last_updated": date,
            "content_summary": passage,
            "is_synthetic": True
        })
        # Link source evidence
        src_id = f"src_{doc_id}"
        add_node(src_id, "Source", f"Source: {title}", {
            "name": f"{title}.pdf",
            "uri": f"s3://nexusworks-docs/{doc_id}.pdf",
            "hash": hashlib.sha256(title.encode()).hexdigest()[:16],
            "ingested_at": date,
            "is_synthetic": True
        })
        add_edge(f"der_{doc_id}_{src_id}", doc_id, src_id, "DERIVED_FROM")

    # Document supersession relationship
    add_edge("sup_sec_pol_20_12", "doc_sec_pol_v20", "doc_sec_pol_v12", "SUPERSEDES", {
        "rationale": "Updated compliance requirements for cloud encryption and KMS mandates."
    })
    add_edge("rel_atlas_prd_proj", "doc_atlas_prd", "proj_atlas", "MENTIONS")
    add_edge("rel_atlas_arch_proj", "doc_atlas_arch", "proj_atlas", "MENTIONS")
    add_edge("sup_dec104_pol20", "dec_104", "doc_sec_pol_v20", "SUPPORTED_BY")

    # 8. Support & Engineering Tickets (42 Tickets)
    # Scenario: Ticket TIK-204 is connected to Security Event SEC-014 and Project Atlas
    tickets = [
        ("tik_201", "TIK-201: Atlas Graph Query Latency Degradation in Staging", "open", "high", "emp_07", "proj_atlas", "2026-10-12"),
        ("tik_202", "TIK-202: FalkorDB Cypher Multi-Hop Timeout on Deep Neighborhoods", "in_progress", "medium", "emp_08", "proj_atlas", "2026-10-14"),
        ("tik_203", "TIK-203: Vector Index Memory Consumption Spike during Ingestion", "closed", "low", "emp_21", "proj_dynasty", "2026-09-28"),
        ("tik_204", "TIK-204: Unauthorized Internal Service Token Generation on Atlas Microservice", "open", "critical", "emp_09", "proj_atlas", "2026-10-17"),
        ("tik_205", "TIK-205: S3 Bucket ACL Misconfiguration Flagged by SecOps Scanner", "open", "high", "emp_14", "proj_atlas", "2026-10-16"),
        ("tik_206", "TIK-206: Memory Leak in Background Task Worker Lease Manager", "resolved", "medium", "emp_10", "proj_genesis", "2026-10-02")
    ]
    for i in range(7, 43):
        tik_id = f"tik_{200+i}"
        tickets.append((tik_id, f"TIK-{200+i}: Routine Maintenance and Bugfix Item {i}", "closed" if i % 2 == 0 else "open", "medium", "emp_10", "proj_beacon", f"2026-09-{min(28, (i%28)+1)}"))

    for t_id, title, status, sev, assignee, p_id, date in tickets:
        add_node(t_id, "Ticket", title, {
            "key": t_id.upper(),
            "title": title,
            "status": status,
            "severity": sev,
            "assignee_id": assignee,
            "project_id": p_id,
            "created_at": date,
            "is_synthetic": True
        })
        add_edge(f"rel_{t_id}_{p_id}", t_id, p_id, "RELATED_TO")
        add_edge(f"asg_{t_id}_{assignee}", t_id, assignee, "ASSIGNED_TO")

    # 9. Incidents (6 Incidents)
    incidents = [
        ("inc_08", "INC-08: Suspicious Service Account Impersonation on Atlas Internal Bus", "active", "critical", "emp_09", "2026-10-17T08:30:00Z"),
        ("inc_07", "INC-07: Ingestion Queue Backlog Failure during Large Batch", "resolved", "medium", "emp_12", "2026-09-15T14:00:00Z"),
        ("inc_06", "INC-06: FalkorDB Node Failover and Reconnection", "resolved", "low", "emp_22", "2026-08-20T10:15:00Z"),
        ("inc_05", "INC-05: Staging Redis Cluster Eviction Spike", "resolved", "medium", "emp_04", "2026-07-11T12:00:00Z"),
        ("inc_04", "INC-04: API Gateway Rate Limiter Flapping", "resolved", "low", "emp_18", "2026-06-05T09:00:00Z"),
        ("inc_03", "INC-03: OAuth Token Refresh Disruption", "resolved", "medium", "emp_14", "2026-05-19T16:20:00Z")
    ]
    for inc_id, title, status, sev, reporter, date in incidents:
        add_node(inc_id, "Incident", title, {
            "title": title,
            "status": status,
            "severity": sev,
            "reporter_id": reporter,
            "detected_at": date,
            "is_synthetic": True
        })
        add_edge(f"rep_{inc_id}_{reporter}", inc_id, reporter, "REPORTED_BY")

    # Link Ticket TIK-204 to Incident INC-08
    add_edge("rel_tik204_inc08", "tik_204", "inc_08", "RELATED_TO")

    # 10. Security Events (16 Security Events)
    # Scenario: SEC-014 represents unauthorized token generation and bulk exfiltration attempt on Atlas
    sec_events = [
        ("sec_014", "SEC-014: Abnormal Token Generation with Admin Privilege Escalation", "privilege_escalation", "critical", "2026-10-17T08:14:22Z", "10.0.4.152", "svc-atlas-worker"),
        ("sec_015", "SEC-015: Excessive Bulk Data Download Request from Internal Subnet", "data_exfiltration_attempt", "high", "2026-10-17T08:21:05Z", "10.0.4.152", "falkordb-graph-endpoint"),
        ("sec_016", "SEC-016: Multiple Failed SSH Auth Attempts on Bastion-02", "brute_force", "medium", "2026-10-16T22:45:10Z", "192.168.1.44", "bastion-host-02")
    ]
    for i in range(1, 14):
        s_id = f"sec_{str(i).zfill(3)}"
        sec_events.append((s_id, f"SEC-{str(i).zfill(3)}: Routine Security Telemetry Audit Log {i}", "audit_scan", "low", f"2026-10-0{min(9, i)}T12:00:00Z", f"10.0.1.{i+10}", f"internal-service-{i}"))

    for s_id, title, ev_type, sev, date, ip, res in sec_events:
        add_node(s_id, "SecurityEvent", title, {
            "event_type": ev_type,
            "severity": sev,
            "timestamp": date,
            "ip_address": ip,
            "resource": res,
            "is_synthetic": True
        })

    # Link SEC-014 to Incident INC-08, Ticket TIK-204, and Project Atlas!
    add_edge("link_sec14_inc08", "sec_014", "inc_08", "LINKED_TO")
    add_edge("link_sec14_tik204", "sec_014", "tik_204", "LINKED_TO")
    add_edge("link_sec14_atlas", "sec_014", "proj_atlas", "LINKED_TO")
    add_edge("link_sec15_atlas", "sec_015", "proj_atlas", "LINKED_TO")

    # 11. Meetings (22 Meetings)
    meetings = [
        ("meet_01", "Project Atlas Architecture Review & Blocker Triage", "2026-10-14", "Discussed S3 encryption roadblock, AD-104 status, and FalkorDB query optimization."),
        ("meet_02", "SecOps Emergency Incident Briefing: INC-08", "2026-10-17", "Immediate review of token escalation anomaly SEC-014 on Atlas worker node."),
        ("meet_03", "NexusWorks Executive Strategy & Q4 Roadmap", "2026-10-01", "Quarterly alignment on AI graph reasoning product release."),
        ("meet_04", "Weekly Platform Infrastructure Sync", "2026-10-12", "Review of cloud operational costs and Redis cache latency.")
    ]
    for i in range(5, 23):
        meet_id = f"meet_{str(i).zfill(2)}"
        meetings.append((meet_id, f"Bi-weekly Team Sync {i}", f"2026-09-{min(28, i)}", f"Standard standup and operational alignment notes for team {i}."))

    for m_id, title, date, summary in meetings:
        add_node(m_id, "Meeting", title, {
            "title": title,
            "date": date,
            "summary": summary,
            "is_synthetic": True
        })

    # Link meetings
    add_edge("meet_01_atlas", "meet_01", "proj_atlas", "MENTIONS")
    add_edge("meet_01_dec104", "dec_104", "meet_01", "DISCUSSED_IN")
    add_edge("meet_02_inc08", "inc_08", "meet_02", "DISCUSSED_IN")

    # 12. Tasks (24 Tasks)
    # Scenario: Marcus Chen owns critical infrastructure migration tasks
    tasks = [
        ("task_501", "Audit S3 Bucket Encryption for Project Atlas Storage", "in_progress", "critical", "emp_07", "proj_atlas", "2026-10-25"),
        ("task_502", "Implement FalkorDB Parameterized Multi-Hop Indexing", "completed", "high", "emp_08", "proj_atlas", "2026-10-10"),
        ("task_503", "Rotate Compromised Service Token for Atlas Worker", "pending", "critical", "emp_09", "proj_atlas", "2026-10-18"),
        ("task_504", "Update SecOps Policy Document v2.0 Sign-off", "completed", "medium", "emp_13", "proj_cipher", "2026-09-30"),
        ("task_505", "Deploy Qwen 2.5 3B Lazy Loading Pipeline", "in_progress", "high", "emp_10", "proj_genesis", "2026-10-22")
    ]
    for i in range(6, 25):
        t_id = f"task_{500+i}"
        tasks.append((t_id, f"Infrastructure Automation Deliverable {i}", "completed" if i % 2 == 0 else "in_progress", "medium", "emp_07", "proj_beacon", f"2026-10-{min(28, i)}"))

    for t_id, title, status, priority, assignee, p_id, due in tasks:
        add_node(t_id, "Task", title, {
            "title": title,
            "status": status,
            "priority": priority,
            "assignee_id": assignee,
            "project_id": p_id,
            "due_date": due,
            "is_synthetic": True
        })
        add_edge(f"asg_{t_id}_{assignee}", t_id, assignee, "ASSIGNED_TO")
        add_edge(f"rel_{t_id}_{p_id}", t_id, p_id, "RELATED_TO")

    # Task dependencies: task_503 depends on task_501
    add_edge("dep_task503_501", "task_503", "task_501", "DEPENDS_ON")

    # 13. Autonomous Agents (8 Agents)
    agents = [
        ("agent_orchestrator", "Master Orchestrator", "Multi-Agent Coordination & Workflow Management"),
        ("agent_graph", "Graph Reasoning Agent", "FalkorDB Cypher Multi-Hop Query & Path Verification"),
        ("agent_knowledge", "Company Knowledge Agent", "Document Retrieval, Provenance & Conflict Checking"),
        ("agent_memory", "Memory Agent", "Episodic, Semantic & Procedural Memory Maintenance"),
        ("agent_coord", "Coordination Agent", "Task Leasing, Handoffs & Concurrency Locks"),
        ("agent_security", "Security Investigation Agent", "Anomaly Correlation, Attack Graph & Risk Scoring"),
        ("agent_action", "Action Agent", "Authorized Tool Execution & Audit Stamping"),
        ("agent_quality", "Quality & Verification Agent", "Factual Grounding & Hallucination Defense")
    ]
    for ag_id, name, desc in agents:
        add_node(ag_id, "Agent", name, {
            "name": name,
            "role": name,
            "description": desc,
            "status": "ready",
            "is_synthetic": True
        })

    # Handoff relationships among agents
    add_edge("handoff_orch_graph", "agent_orchestrator", "agent_graph", "HANDOFF_TO")
    add_edge("handoff_orch_sec", "agent_orchestrator", "agent_security", "HANDOFF_TO")
    add_edge("handoff_sec_action", "agent_security", "agent_action", "HANDOFF_TO")

    # 14. Memories (Initial Episodic & Procedural Memories)
    memories = [
        ("mem_001", "episodic", "Prior Investigation of Project Atlas Dependency Chain", "Discovered AD-104 is blocking release due to S3 encryption policy supersession.", 0.98, "tenant_nexus_main"),
        ("mem_002", "procedural", "P1 Security Escalation Standard Playbook", "Steps: 1. Identify affected resource. 2. Correlate with related tickets. 3. Propose token revocation. 4. Request Human Authorization.", 1.0, "tenant_nexus_main"),
        ("mem_003", "semantic", "Ownership Mapping: Project Atlas Lead", "Maya Lin is the Principal Product Manager and Elena Vance is the CPO sponsoring Atlas.", 0.99, "tenant_nexus_main")
    ]
    for mem_id, m_type, title, desc, conf, tenant in memories:
        add_node(mem_id, "Memory", title, {
            "type": m_type,
            "summary": title,
            "details": {"narrative": desc},
            "confidence": conf,
            "tenant_id": tenant,
            "is_synthetic": True
        })
        add_edge(f"rem_ag_mem_{mem_id}", "agent_memory", mem_id, "REMEMBERS")

    return nodes, edges
