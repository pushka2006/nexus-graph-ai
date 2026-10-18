# NEXUS GRAPH AI - Graph Data Model & Schema

## Authoritative Store: FalkorDB

The knowledge graph models the connected enterprise across 15 Node types and 19 Relationship types.

### Node Types
1. `Company`: Top-level corporate entity (`id`, `name`, `domain`, `industry`).
2. `Department`: Organizational business unit (`id`, `name`, `code`, `budget`).
3. `Team`: Cross-functional group (`id`, `name`, `charter`).
4. `Person`: Employee, contractor, or stakeholder (`id`, `name`, `email`, `role`, `department_id`, `security_clearance`).
5. `Project`: Business or technical initiative (`id`, `name`, `code`, `status`, `target_date`, `risk_level`).
6. `Document`: Policies, architecture specifications, memos (`id`, `title`, `version`, `status`, `classification`, `url`, `last_updated`).
7. `Ticket`: Customer or engineering issue (`id`, `key`, `title`, `severity`, `status`, `created_at`).
8. `Meeting`: Sync, review, or architecture committee (`id`, `title`, `date`, `summary`).
9. `Decision`: Key architectural or executive choice (`id`, `title`, `status`, `decided_at`, `rationale`).
10. `Task`: Action item or engineering deliverable (`id`, `title`, `status`, `priority`, `due_date`).
11. `Incident`: Operational outage or breach (`id`, `title`, `severity`, `status`, `detected_at`).
12. `SecurityEvent`: Telemetry anomaly, suspicious access (`id`, `event_type`, `severity`, `timestamp`, `ip_address`, `resource`).
13. `Agent`: Autonomous worker profile (`id`, `name`, `role`, `capabilities`, `status`).
14. `Memory`: Episodic, semantic, or procedural memory entry (`id`, `type`, `summary`, `confidence`, `tenant_id`, `created_at`).
15. `Source`: Ingested file, external link, or audit provenance (`id`, `name`, `uri`, `hash`, `ingested_at`).

### Relationship Types
- `MEMBER_OF`: Person -> Team / Team -> Department / Department -> Company
- `MANAGES`: Person -> Person / Person -> Team
- `OWNS`: Person -> Project / Team -> Project / Person -> Document
- `ASSIGNED_TO`: Task -> Person / Ticket -> Person
- `WORKS_ON`: Person -> Project
- `DEPENDS_ON`: Project -> Project / Task -> Task / Decision -> Decision
- `BLOCKED_BY`: Project -> Decision / Task -> Ticket
- `MENTIONS`: Document -> Person / Meeting -> Project
- `DISCUSSED_IN`: Decision -> Meeting / Ticket -> Meeting
- `DECIDED_IN`: Decision -> Meeting
- `SUPPORTED_BY`: Decision -> Document / Answer -> Evidence
- `SUPERSEDES`: Document -> Document (Policy v2 supersedes v1)
- `RELATED_TO`: Ticket -> Incident / Project -> Ticket
- `REPORTED_BY`: Incident -> Person / SecurityEvent -> Agent
- `LINKED_TO`: SecurityEvent -> Project / SecurityEvent -> Ticket
- `CREATED_BY`: Task -> Agent / Document -> Person
- `DERIVED_FROM`: Memory -> Document / Fact -> Source
- `REMEMBERS`: Agent -> Memory
- `HANDOFF_TO`: Agent -> Agent (Coordination task delegation)
