# Audit & Compliance Trail

| Field | Value |
|---|---|
| Module | FND |
| Sub-module | AUD |
| Status | Draft — pending verification |
| Source | §9 Audit trail |

## 1. Scope
Provide immutable, timestamped, user-tagged audit records for every regulated transaction across all modules.

## 2. Exclusions
External SIEM product integration beyond export APIs in Phase 1.

## 3. Actors and Permissions
- Compliance Officer — search/export audits
- All modules — write audit records via shared SDK
- Security Admin — configure retention categories

## 4. Functional Requirements
| ID | Requirement |
|---|---|
| FND-AUD-FR-001 | Every state-changing business operation shall write an audit record. |
| FND-AUD-FR-002 | Audit records shall include actor, facility, correlationId, entity type/id, action, before/after (or diff), timestamp (UTC), and source module. |
| FND-AUD-FR-003 | Audit records shall be append-only; updates/deletes are not permitted via application APIs. |
| FND-AUD-FR-004 | System shall support filtered search and legal export. |
| FND-AUD-FR-005 | High-sensitivity entities (drug dispense, financial postings, credential overrides) shall be marked with compliance category tags. |

## 5. Workflow and State Transitions
Audit records have no editable lifecycle; operational index states: `Writable(hot) -> Warm -> ArchivedCold` for storage tiering only.

## 6. Data / Entities and Validation
- `AuditEvent` — immutable
- Optional `AuditExportJob`
- PII in audit payloads minimized/redacted per policy

## 7. Business Rules
| ID | Rule |
|---|---|
| FND-AUD-BR-001 | Application modules cannot bypass audit SDK for marked command types. |
| FND-AUD-BR-002 | Clock skew tolerance recorded; server UTC is authoritative. |

## 8. Approvals
Retention policy changes require Compliance Officer approval.

## 9. APIs and Module Ownership
**Owner:** FND

### APIs
- `GET /api/fnd/audit`
- `POST /api/fnd/audit/exports`
- `GET /api/fnd/audit/exports/{id}`

### Events Published
- `AuditExportCompleted`

### Events Consumed
- None

## 10. Notifications
- Notify requester when export ready

## 11. Reports
- Audit activity by module
- Sensitive action report

## 12. Audit, Retention, and Privacy
Audit store is the compliance system of record. Default retention 7–10 years configurable by category. Patient-identifiable audit access is itself audited.

## 13. Failure, Idempotency, and Concurrency
- Audit write failures fail the business transaction or enqueue guaranteed write per policy (at-least-once with dedupe key).
- Export jobs restartable/idempotent.

## 14. Non-Functional Requirements
- Audit write overhead budgeted < 15ms P95 amortized.
- Search over 90 days hot data P95 < 2s for common filters.

## 15. Dependencies
- FND IAM
- FND Data Governance

## 16. Acceptance Criteria
| ID | Criterion |
|---|---|
| FND-AUD-AC-001 | Creating a clinical order produces an audit record with actor and entity ids. |
| FND-AUD-AC-002 | Attempt to update audit record via API is rejected. |
| FND-AUD-AC-003 | Export contains expected filtered subset. |

## 17. Open Assumptions
- Exact regulatory regime (HIPAA/GDPR/local) selected per deployment configuration.

## 18. Source Traceability
Mapped from `§9 Audit trail` in `Healthcare-ERP-Pathway-and-Workflow.md`.
